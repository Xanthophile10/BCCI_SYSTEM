from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
import sys
from BCCI_SYSTEM_GUI import Ui_MainWindow
from BCCI_SYSTEM_DATABASE_GUI import Ui_otherWindow
from tkinter import *
from tkinter import messagebox
import mysql.connector
import urllib.request
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

class my_app(QtWidgets.QMainWindow):
    def __init__(self):
        super(my_app,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Calculate.clicked.connect(self.INCOME_TAX)
        self.ui.Calculate.clicked.connect(self.SSS_CONTRIBUTION)
        self.ui.Calculate.clicked.connect(self.PAG_IBIG)
        self.ui.Calculate.clicked.connect(self.PHILHEALTH)
        self.ui.Calculate.clicked.connect(self.ISEMPTY)
        self.ui.Calculate.clicked.connect(self.HASNUMBERS)
        self.ui.Add_to_Database.clicked.connect(self.ADD_TO_DATABASE)
        self.ui.Add_to_Firebase.clicked.connect(self.ADD_TO_FIREBASE)
        self.ui.Show_Database.clicked.connect(self.SHOW_DATABASE)

        self.ui.Yes.clicked.connect(self.YES)
        self.ui.No.clicked.connect(self.NO)

    def SHOW_DATABASE(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_otherWindow()
        self.ui.setupUi(self.window)
        
        try:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="bcci_system")
                self.window.show()
            except:
                messagebox.showerror("Error", "MySQL Database is not available")
        except:
                self.window.close()

    def ADD_TO_FIREBASE(self):
        if (len(self.ui.Monthly_Salary.text()) & len(self.ui.Name_of_Company.text())):
            try:
                urllib.request.urlopen('http://google.com', timeout=1)
                cred = credentials.Certificate('bcci-system-firebase-adminsdk-hvbn4-9c9669a9e3.json')
                firebase_admin.initialize_app(cred)

                # Access Firestore database
                db = firestore.client()

                if db:
                    #print("Connected to Firestore")
                    try:
                        app = firebase_admin.get_app()
                    except ValueError as e:
                        cred = credentials.Certificate('bcci-system-firebase-adminsdk-hvbn4-9c9669a9e3.json')
                        firebase_admin.initialize_app(cred)
                    db = firestore.client()
                    Obj1 = {
                        "Name_of_Employee": self.ui.Name_of_Employee.text(),
                        "Name_of_Company": self.ui.Name_of_Company.text(),
                        "Monthly_Salary": self.ui.Monthly_Salary.text(),
                        "Income_Tax": self.ui.Income_Tax.text(),
                        "SSS_Contribution": self.ui.SSS_Contribution.text(),
                        "Pag_Ibig": self.ui.Pag_Ibig.text(),
                        "Philhealth": self.ui.PhilHealth.text(),
                        }   
                    data = [Obj1]

                    for record in data:
                        doc_ref = db.collection(u'Users').document(record['Name_of_Employee'])
                        doc_ref.set(record)

                    users_ref = db.collection(u'Users')
                    docs = users_ref.stream()
                    messagebox.showinfo("Info", "Data Inserted")
                else:
                    #print("Could not connect to Firestore")
                    messagebox.showerror("Error", "Data not inserted")
                    return True
            except urllib.request.URLError as error:
                messagebox.showinfo("Info", "No internet connection {error}")
                return False
        else:
            messagebox.showerror("Error", "Empty")
            
    def ADD_TO_DATABASE(self):
        try:
            #print("Database is active!")
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="bcci_system")
            cursor = mydb.cursor()
            sql = "INSERT INTO employee (Name_of_Employee, Name_of_Company, Monthly_Salary, Income_Tax, SSS_Contribution, Pag_Ibig, Philhealth) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (self.ui.Name_of_Employee.text(), self.ui.Name_of_Company.text(), self.ui.Monthly_Salary.text(), self.ui.Income_Tax.text(), self.ui.SSS_Contribution.text(), self.ui.Pag_Ibig.text(), self.ui.PhilHealth.text())    
            cursor.execute(sql, value)
            mydb.commit()
            mydb.close()
            messagebox.showinfo("Info", "Data Inserted")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showwarning("Warning", "Data not inserted")

    def HASNUMBERS(self):
        testNameofCompany = self.ui.Name_of_Employee.text()

        res = any(chr.isdigit() for chr in testNameofCompany)

        if res == True:
            messagebox.showerror("Error", "Field contains Number")
            self.ui.Name_of_Employee.clear()
            self.ui.Name_of_Company.clear()
            self.ui.Income_Tax.clear()
            self.ui.SSS_Contribution.clear()
            self.ui.Pag_Ibig.clear()
            self.ui.PhilHealth.clear()
            self.ui.Monthly_Salary.clear()
        else:
            messagebox.showinfo("Info","Clear")


    def ISEMPTY(self):
        emptyEmployee = self.ui.Name_of_Employee.text()
        emptyCompany = self.ui.Name_of_Company.text()

        if  (len(emptyEmployee) & len(emptyCompany)):
            messagebox.showinfo("Would you like to continue?", "Engr. Gerald Anthony Cabansag")
        else:
            
            messagebox.showerror("Warning!", "Empty field detected!")
            self.ui.Name_of_Employee.clear()
            self.ui.Name_of_Company.clear()
            self.ui.Income_Tax.clear()
            self.ui.SSS_Contribution.clear()
            self.ui.Pag_Ibig.clear()
            self.ui.PhilHealth.clear()
            self.ui.Monthly_Salary.clear()

    def INCOME_TAX(self):

        checknumbers = self.ui.Monthly_Salary.text()

        if checknumbers.isnumeric():
            if len(self.ui.Monthly_Salary.text()):
                mTax = 0

                aSalary = float(self.ui.Monthly_Salary.text())

                aSalary = (aSalary * 12)

                if (aSalary < 250000):
                    mTax = 0
                elif (aSalary >= 250000) & (aSalary <= 400000):
                    mTax = (0.2 * (aSalary - 250000)) / 12
                elif (aSalary >= 400000) & (aSalary <= 800000):
                    mTax = (30000 + (0.25 * (aSalary - 400000))) / 12
                elif (aSalary >= 800000) & (aSalary <= 2000000):
                    mTax = (130000 + (0.3 * (aSalary - 800000))) / 12
                elif (aSalary >= 2000000) & (aSalary <= 8000000):
                    mTax = (490000 + (0.32 * (aSalary - 2000000)))
                elif (aSalary > 8000000):
                    mTax = (2410000 + (0.35 * (aSalary - 8000000)))

                self.ui.Income_Tax.setText(str(mTax))
                self.ui.SSS_Contribution.setText(str(self.ui.SSS_Contribution.text()))
                self.ui.Pag_Ibig.setText(str(self.ui.Pag_Ibig.text()))
                self.ui.PhilHealth.setText(str(self.ui.PhilHealth.text()))
                #messagebox.showinfo("Gerald", "gerald")
            else:
                #messagebox.showerror("showerror", "Empty Field")
                self.ui.Name_of_Employee.clear()
                self.ui.Name_of_Company.clear()
                self.ui.Income_Tax.clear()
                self.ui.SSS_Contribution.clear()
                self.ui.Pag_Ibig.clear()
                self.ui.PhilHealth.clear()
                self.ui.Monthly_Salary.clear()
        else:
            messagebox.showerror("Warning", "Numbers and Letters can't combined")

    def SSS_CONTRIBUTION(self):

        checknumbers = self.ui.Monthly_Salary.text()

        if checknumbers.isnumeric():
            if len(self.ui.Monthly_Salary.text()):
                ssl = 0

                mSalary = float(self.ui.Monthly_Salary.text())

                if (mSalary < 2250):
                    ssl = 80
                elif (mSalary >= 2250) & (mSalary <= 2749.50):
                    ssl = 100
                elif (mSalary >= 2750) & (mSalary <= 3249.99):
                    ssl = 120
                elif (mSalary >= 3250) & (mSalary <= 3749.99):
                    ssl = 140
                elif (mSalary >= 3750) & (mSalary <= 4249.99):
                    ssl = 160
                elif (mSalary >= 4250) & (mSalary <= 4749.99):
                    ssl = 180
                elif (mSalary >= 4750) & (mSalary <= 5249.99):
                    ssl = 200
                elif (mSalary >= 5250) & (mSalary <= 5749.99):
                    ssl = 240
                elif (mSalary > 6250):
                    ssl = 260

                self.ui.SSS_Contribution.setText(str(ssl))
                self.ui.Income_Tax.setText(str(self.ui.Income_Tax.text()))
                self.ui.Pag_Ibig.setText(str(self.ui.Pag_Ibig.text()))
                self.ui.PhilHealth.setText(str(self.ui.PhilHealth.text()))
                #messagebox.showinfo("Gerald", "gerald")
            else:
                #messagebox.showerror("showerror", "Empty Field")
                self.ui.Name_of_Employee.clear()
                self.ui.Name_of_Company.clear()
                self.ui.Income_Tax.clear()
                self.ui.SSS_Contribution.clear()
                self.ui.Pag_Ibig.clear()
                self.ui.PhilHealth.clear()
                self.ui.Monthly_Salary.clear()
        else:
            self.ui.Name_of_Employee.clear()
            self.ui.Name_of_Company.clear()
            self.ui.Income_Tax.clear()
            self.ui.SSS_Contribution.clear()
            self.ui.Pag_Ibig.clear()
            self.ui.PhilHealth.clear()
            self.ui.Monthly_Salary.clear()

    def PAG_IBIG(self):

        checknumbers = self.ui.Monthly_Salary.text()

        if checknumbers.isnumeric():
            if len(self.ui.Monthly_Salary.text()):
                pagaw = 0

                salar = float(self.ui.Monthly_Salary.text())

                if (salar <= 1500):
                    pagaw = salar * 0.01
                else:
                    pagaw = salar * 0.02

                self.ui.Pag_Ibig.setText(str(pagaw))
                self.ui.Income_Tax.setText(str(self.ui.Income_Tax.text()))
                self.ui.SSS_Contribution.setText(str(self.ui.SSS_Contribution.text()))
                self.ui.PhilHealth.setText(str(self.ui.PhilHealth.text()))
                #messagebox.showinfo("Gerald", "gerald")
            else:
                #messagebox.showerror("showerror", "Empty Field")
                self.ui.Name_of_Employee.clear()
                self.ui.Name_of_Company.clear()
                self.ui.Income_Tax.clear()
                self.ui.SSS_Contribution.clear()
                self.ui.Pag_Ibig.clear()
                self.ui.PhilHealth.clear()
                self.ui.Monthly_Salary.clear()
        else:
            self.ui.Name_of_Employee.clear()
            self.ui.Name_of_Company.clear()
            self.ui.Income_Tax.clear()
            self.ui.SSS_Contribution.clear()
            self.ui.Pag_Ibig.clear()
            self.ui.PhilHealth.clear()
            self.ui.Monthly_Salary.clear()

    def PHILHEALTH(self):

        checknumbers = self.ui.Monthly_Salary.text()

        if checknumbers.isnumeric():
            if len(self.ui.Monthly_Salary.text()):

                Phil = 0

                Philhealth = float(self.ui.Monthly_Salary.text())

                if (Philhealth < 8999.99):
                    Phil = 100.0
                elif (Philhealth >= 9000) & (Philhealth <= 9999.99):
                    Phil = 112.5
                elif (Philhealth >= 10000.00) & (Philhealth <= 10999.99):
                    Phil = 125.0
                elif (Philhealth >= 11000.00) & (Philhealth <= 11999.99):
                    Phil = 137.5
                elif (Philhealth >= 12000.00) & (Philhealth <= 12999.99):
                    Phil = 150.0
                elif (Philhealth >= 13000.00) & (Philhealth <= 13999.99):
                    Phil = 162.5
                elif (Philhealth >= 14000.00) & (Philhealth <= 14999.99):
                    Phil = 175.0
                elif (Philhealth >= 15000.00) & (Philhealth <= 15999.99):
                    Phil = 187.5
                elif (Philhealth >= 16000.00) & (Philhealth <= 16999.99):
                    Phil = 200.0
                elif (Philhealth >= 17000.00) & (Philhealth <= 17999.99):
                    Phil = 212.5
                elif (Philhealth >= 18000.00) & (Philhealth <= 18999.99):
                    Phil = 225.0
                elif (Philhealth >= 19000.00) & (Philhealth <= 19999.99):
                    Phil = 237.5
                elif (Philhealth >= 20000.00) & (Philhealth <= 20999.99):
                    Phil = 250.0
                elif (Philhealth >= 21000.00) & (Philhealth <= 21999.99):
                    Phil = 262.5
                elif (Philhealth >= 22000.00) & (Philhealth <= 22999.99):
                    Phil = 275.0
                elif (Philhealth >= 23000.00) & (Philhealth <= 23999.99):
                    Phil = 287.5
                elif (Philhealth >= 24000.00) & (Philhealth <= 24999.99):
                    Phil = 300.0
                elif (Philhealth >= 25000.00) & (Philhealth <= 25999.99):
                    Phil = 312.5
                elif (Philhealth >= 26000.00) & (Philhealth <= 26999.99):
                    Phil = 325.0
                elif (Philhealth >= 27000.00) & (Philhealth <= 27999.99):
                    Phil = 337.5
                elif (Philhealth >= 28000.00) & (Philhealth <= 28999.99):
                    Phil = 350.0
                elif (Philhealth >= 29000.00) & (Philhealth <= 29999.99):
                    Phil = 362.5
                elif (Philhealth >= 30000.00) & (Philhealth <= 30999.99):
                    Phil = 375.0
                elif (Philhealth >= 31000.00) & (Philhealth <= 31999.99):
                    Phil = 387.5
                elif (Philhealth >= 32000.00) & (Philhealth <= 32999.99):
                    Phil = 400.0
                elif (Philhealth >= 33000.00) & (Philhealth <= 33999.99):
                    Phil = 412.5
                elif (Philhealth >= 34000.00) & (Philhealth <= 34999.99):
                    Phil = 425.0
                elif (Philhealth > 35000):
                    Phil = 437.5

                self.ui.PhilHealth.setText(str(Phil))
                self.ui.Income_Tax.setText(str(self.ui.Income_Tax.text()))
                self.ui.SSS_Contribution.setText(str(self.ui.SSS_Contribution.text()))
                self.ui.Pag_Ibig.setText(str(self.ui.Pag_Ibig.text()))
                self.ui.PhilHealth.setText(str(self.ui.PhilHealth.text()))
                #messagebox.showinfo("Gerald", "gerald")
            else:
                #messagebox.showerror("showerror", "Empty Field")
                self.ui.Name_of_Employee.clear()
                self.ui.Name_of_Company.clear()
                self.ui.Income_Tax.clear()
                self.ui.SSS_Contribution.clear()
                self.ui.Pag_Ibig.clear()
                self.ui.PhilHealth.clear()
                self.ui.Monthly_Salary.clear()
        else:
            self.ui.Name_of_Employee.clear()
            self.ui.Name_of_Company.clear()
            self.ui.Income_Tax.clear()
            self.ui.SSS_Contribution.clear()
            self.ui.Pag_Ibig.clear()
            self.ui.PhilHealth.clear()
            self.ui.Monthly_Salary.clear()

    def YES(self):

        self.ui.Income_Tax.clear()
        self.ui.SSS_Contribution.clear()
        self.ui.Pag_Ibig.clear()
        self.ui.PhilHealth.clear()
        self.ui.Monthly_Salary.clear()
        self.ui.Name_of_Employee.clear()
        self.ui.Name_of_Company.clear()

    def NO(self):
        QCoreApplication.instance().quit()

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = my_app()
    win.show()
    sys.exit(app.exec_())

app()