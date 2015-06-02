from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from datetime import datetime


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):    #the cookie that should contain the access token!
            budgeteer = Budgeteer.getBudgeteerById(self.request.cookies.get('budgeteerIdToken'))
            if budgeteer:
                self.redirect('/Budgets')

        template_params = dict()
        html = template.render("web/templates/registration.html", template_params)
        self.response.write(html)

class RegistrationCheckHandler(webapp2.RequestHandler):

    def get(self):


        Email = self.request.get('email')
        UserName = self.request.get('username')

        if Budgeteer.budgeteerUserNameExist(UserName):
            self.response.write('UserName already exists')
        if Budgeteer.budgeteerEmailExist(Email):
            self.response.write('Email already exists')
        BudgeteerObj = Budgeteer()
        BudgeteerObj.firstName = self.request.get('FirstName')
        BudgeteerObj.lastName = self.request.get('LastName')
        BudgeteerObj.password = self.request.get('password')
        BirthMonth = self.requst.get("BirthMonth")
        BirthDay = self.requst.get("BirthDay")
        BirthYear = self.requst.get("BirthYear")
        #BudgeteerObj.birthday = datetime.strptime('' + BirthDay + ' ' + BirthMonth + ' ' + BirthYear, '%d %b %Y')
        BudgeteerObj.birthday = datetime.datetime(day =  BirthDay , month = BirthMonth ,yeat =  BirthYear)
        BudgeteerObj.gender = self.requst.get("gender")


        budgeteerId = Budgeteer.registerBudgeteer(BudgeteerObj)

        if not budgeteerId :
            self.error(403)
            self.response.write('Wrong Username Or Password')
            return

        self.response.set_cookie('budgeteerIdToken', str(budgeteerId))


app = webapp2.WSGIApplication([('/Registration', IndexHandler), ('/RegistrationCheck', RegistrationCheckHandler)], debug=True)
