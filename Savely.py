from tkinter import *
import tkinter.messagebox
import sqlite3
import calendar
import datetime
import time

db = sqlite3.connect('login.db')
cursor = db.cursor()
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, username TEXT, totalbudget FLOAT, totalusage FLOAT, 
    highestcat TEXT, highestvalue FLOAT, lowestcat TEXT, lowestvalue FLOAT,  foodbudget FLOAT, educationbudget FLOAT, 
                        groceriesbudget FLOAT, fuelbudget FLOAT, clothingbudget FLOAT, 
                        transportbudget FLOAT, utilitiesbudget FLOAT, healthbudget FLOAT, 
                        insurancebudget FLOAT, othersbudget FLOAT, food FLOAT, education FLOAT, 
                        groceries FLOAT, fuel FLOAT, clothing FLOAT, transport FLOAT, 
                        utilities FLOAT, health FLOAT, insurance FLOAT, others FLOAT, monthnumber INT)
 ''')
db.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT,
                       password TEXT, foodbudget FLOAT, educationbudget FLOAT, 
                        groceriesbudget FLOAT, fuelbudget FLOAT, clothingbudget FLOAT, 
                        transportbudget FLOAT, utilitiesbudget FLOAT, healthbudget FLOAT, 
                        insurancebudget FLOAT, othersbudget FLOAT, food FLOAT, education FLOAT, 
                        groceries FLOAT, fuel FLOAT, clothing FLOAT, transport FLOAT, 
                        utilities FLOAT, health FLOAT, insurance FLOAT, others FLOAT, 
                        dateinitial TEXT, dateafteronemonth TEXT, datetoday TEXT, state INT, monthnumber INT, 
                        totalbudget FLOAT, totalusage FLOAT, highestcat TEXT, highestvalue FLOAT, 
                        lowestcat TEXT, lowestvalue FLOAT)
''')
db.commit()

root = Tk()
root.geometry("1000x750")
root.title("Savely")

LoginFrame = Frame(root)
LoginFrame.pack()

RegisterFrame = Frame(root)

MainInterfaceFrame = Frame(root)

ExpenditureInterface = Frame(root)

ProfileFrame = Frame(root)

BudgetingFrame = Frame(root)

SummaryFrame = Frame(root)

HistoryFrame = Frame(root)

def LoginRegisterClicked():
    LoginFrame.pack_forget()
    RegisterFrame.pack()
    entry_1.delete(0, END)
    entry_1.insert(0, "")
    entry_2.delete(0, END)
    entry_2.insert(0, "")

def RegisterClicked():
    global InfoInput_1
    global InfoInput_2
    global InfoInput_3
    GetRegistrationName = InfoInput_1.get()
    GetRegistrationPass = InfoInput_2.get()
    GetRegistrationConfirmPass = InfoInput_3.get()

    checkTaken = 'No'
    for row in cursor.execute('SELECT username FROM users').fetchall():
        if row[0] == GetRegistrationName:
            checkTaken = 'Yes'

    if len(GetRegistrationName) <= 1 or len(GetRegistrationPass) <= 1:
        tkinter.messagebox.showerror("Error", "Invalid Credentials Entered")
    elif  GetRegistrationPass != GetRegistrationConfirmPass:
        tkinter.messagebox.showerror("Error", "Passwords do not match")
    elif GetRegistrationName == GetRegistrationPass:
        tkinter.messagebox.showerror("Error", "Password cannot be the same as the username for security purposes")
    elif checkTaken == 'Yes':
        tkinter.messagebox.showerror("Error", "That username has already been taken")
    else:
        cursor.execute(''' INSERT INTO users(username, password, foodbudget, educationbudget, groceriesbudget, fuelbudget, 
                            clothingbudget, transportbudget, utilitiesbudget, healthbudget, insurancebudget, othersbudget, 
                            food, education, groceries, fuel, clothing, transport, utilities, health, 
                            insurance, others, state, monthnumber, 
                            totalbudget, totalusage, highestcat, highestvalue, lowestcat, lowestvalue) 
                            VALUES(?, ?, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0) ''',
                       (GetRegistrationName, GetRegistrationPass))
        db.commit()
        tkinter.messagebox.showinfo("Success", "Registration Successful")
        InfoInput_1.delete(0, END)
        InfoInput_1.insert(0, "")
        InfoInput_2.delete(0, END)
        InfoInput_2.insert(0, "")
        InfoInput_3.delete(0, END)
        InfoInput_3.insert(0, "")
        RegisterFrame.pack_forget()
        LoginFrame.pack()

def fromRegToLogPage():
    RegisterFrame.pack_forget()
    LoginFrame.pack()
    InfoInput_1.delete(0, END)
    InfoInput_1.insert(0, "")
    InfoInput_2.delete(0, END)
    InfoInput_2.insert(0, "")
    InfoInput_3.delete(0, END)
    InfoInput_3.insert(0, "")

global state
GetLoginName = ' '

def LoginCredentials():
    global entry_1
    global entry_2
    global GetLoginName
    global GetLoginPassword
    GetLoginName = entry_1.get()
    GetLoginPassword = entry_2.get()
    str(GetLoginName)
    str(GetLoginPassword)
    test = cursor.execute(''' SELECT password FROM users WHERE username = ?''', (GetLoginName, )).fetchone()
    if test:
        checkPassword = test
        if GetLoginPassword == checkPassword[0]:
            tkinter.messagebox.showinfo("Perfect", "Login Successful")
            global now
            now = datetime.datetime.today()
            test = cursor.execute(''' SELECT dateinitial FROM users WHERE username = ?''', (GetLoginName,)).fetchone()

            cursor.execute(''' SELECT foodbudget, educationbudget, groceriesbudget, fuelbudget, clothingbudget, transportbudget, 
                                                        utilitiesbudget, healthbudget, insurancebudget, othersbudget FROM users WHERE username=?''',
                           (GetLoginName,))
            budgetValues = cursor.fetchone()

            cursor.execute(''' SELECT food, education, groceries, fuel, clothing, transport, 
                                                        utilities, health, insurance, others FROM users WHERE username=?''',
                           (GetLoginName,))
            usageValues = cursor.fetchone()

            TotalBudget = 0
            for values in budgetValues:
                TotalBudget = TotalBudget + values

            TotalUsage = 0
            highestUsage = 0
            lowestUsage = 99999999
            highestUsageCat = 'Nil'
            lowestUsageCat = 'Nil'
            counter = 0
            overBudget = 0
            overBudgetCat = []
            i = 0
            categoryList = ['Food', 'Education', 'Groceries', 'Fuel', 'Clothing', 'Transport', 'Utilities', 'Health', 'Insurance', 'Others']
            for values in usageValues:
                if values > budgetValues[i]:
                    overBudgetCat.append(categoryList[i])
                    overBudget = overBudget + 1
                i = i + 1

            for values in usageValues:
                TotalUsage = TotalUsage + values
                if values > highestUsage:
                    highestUsage = values
                    if counter == 0:
                        highestUsageCat = 'Food'
                    elif counter == 1:
                        highestUsageCat = 'Education'
                    elif counter == 2:
                        highestUsageCat = 'Groceries'
                    elif counter == 3:
                        highestUsageCat = 'Fuel'
                    elif counter == 4:
                        highestUsageCat = 'Clothing'
                    elif counter == 5:
                        highestUsageCat = 'Transport'
                    elif counter == 6:
                        highestUsageCat = 'Utilities'
                    elif counter == 7:
                        highestUsageCat = 'Health'
                    elif counter == 8:
                        highestUsageCat = 'Insurance'
                    elif counter == 9:
                        highestUsageCat = 'Others'
                counter = counter + 1
            counter = 0
            for values in usageValues:
                if values < lowestUsage and values != 0:
                    lowestUsage = values
                    if counter == 0:
                        lowestUsageCat = 'Food'
                    elif counter == 1:
                        lowestUsageCat = 'Education'
                    elif counter == 2:
                        lowestUsageCat = 'Groceries'
                    elif counter == 3:
                        lowestUsageCat = 'Fuel'
                    elif counter == 4:
                        lowestUsageCat = 'Clothing'
                    elif counter == 5:
                        lowestUsageCat = 'Transport'
                    elif counter == 6:
                        lowestUsageCat = 'Utilities'
                    elif counter == 7:
                        lowestUsageCat = 'Health'
                    elif counter == 8:
                        lowestUsageCat = 'Insurance'
                    elif counter == 9:
                        lowestUsageCat = 'Others'

                counter = counter + 1

                cursor.execute(''' UPDATE users SET totalbudget = ?, totalusage = ?, highestcat = ?, highestvalue = ?, 
                                    lowestcat = ?, lowestvalue = ? WHERE username = ?''', (TotalBudget, TotalUsage, highestUsageCat,
                                                                                           highestUsage, lowestUsageCat,
                                                                                           lowestUsage, GetLoginName,))

            if test[0] is None:
                cursor.execute(''' UPDATE users SET dateinitial = ? WHERE username = ? ''', (now, GetLoginName,))
                db.commit()
                days = calendar.monthrange(now.year, now.month)[1]
                afterOneMonth = now + datetime.timedelta(days=days)
                cursor.execute(''' UPDATE users SET dateafteronemonth = ? WHERE username = ? ''',
                               (afterOneMonth, GetLoginName,))
                db.commit()

            cursor.execute(''' UPDATE users SET datetoday = ? WHERE username = ? ''', (now, GetLoginName,))
            db.commit()
            global monthEndDate
            global today
            global daysLeft
            monthEndDate = cursor.execute(''' SELECT dateafteronemonth FROM users WHERE username = ?''',
                                          (GetLoginName,)).fetchone()

            time.sleep(0.5)
            LoginFrame.pack_forget()
            MainInterfaceFrame.pack()
            entry_1.delete(0, END)
            entry_1.insert(0, "")
            entry_2.delete(0, END)
            entry_2.insert(0, "")

            test = cursor.execute(''' SELECT foodbudget, educationbudget, groceriesbudget, fuelbudget, clothingbudget, transportbudget, 
                            utilitiesbudget, healthbudget, insurancebudget, othersbudget FROM users WHERE username=?''', (GetLoginName,)).fetchone()
            total = 0
            for values in test:
                total = total + values
            if total == 0:
                tkinter.messagebox.showinfo("Welcome", "The system has detected that you are a new user. You will now be redirected to the budgeting page to insert your budget for each category")
                state = 1
                time.sleep(1)
                LoginFrame.pack_forget()
                MainInterfaceFrame.pack_forget()
                BudgetingFrame.pack()

            now = datetime.datetime.today()
            daysLeft = (datetime.datetime.strptime(monthEndDate[0], '%Y-%m-%d %H:%M:%S.%f') - now).days
            if daysLeft <= 0:

                foodBudgetHistory = cursor.execute(''' SELECT foodbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                educationBudgetHistory = cursor.execute(''' SELECT educationbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                groceriesBudgetHistory = cursor.execute(''' SELECT groceriesbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                fuelBudgetHistory = cursor.execute(''' SELECT fuelbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                clothingBudgetHistory = cursor.execute(''' SELECT clothingbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                transportBudgetHistory = cursor.execute(''' SELECT transportbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                utilitiesBudgetHistory = cursor.execute(''' SELECT utilitiesbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                healthBudgetHistory = cursor.execute(''' SELECT healthbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                insuranceBudgetHistory = cursor.execute(''' SELECT insurancebudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                othersBudgetHistory = cursor.execute(''' SELECT othersbudget FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()

                foodHistory = cursor.execute(''' SELECT food FROM users where username = ? ''',
                                                   (GetLoginName,)).fetchone()
                educationHistory = cursor.execute(''' SELECT education FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                groceriesHistory = cursor.execute(''' SELECT groceries FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                fuelHistory = cursor.execute(''' SELECT fuel FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                clothingHistory = cursor.execute(''' SELECT clothing FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                transportHistory = cursor.execute(''' SELECT transport FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                utilitiesHistory = cursor.execute(''' SELECT utilities FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                healthHistory = cursor.execute(''' SELECT health FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                insuranceHistory = cursor.execute(''' SELECT insurance FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                othersHistory = cursor.execute(''' SELECT others FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()

                totalBudgetHistory = cursor.execute(''' SELECT totalbudget FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                totalUsageHistory = cursor.execute(''' SELECT totalusage FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                highestCatHistory = cursor.execute(''' SELECT highestcat FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                highestValueHistory = cursor.execute(''' SELECT highestvalue FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                lowestCatHistory = cursor.execute(''' SELECT lowestcat FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()
                lowestValueHistory = cursor.execute(''' SELECT lowestvalue FROM users where username = ? ''',
                                             (GetLoginName,)).fetchone()

                monthnumber = cursor.execute(''' SELECT monthnumber FROM users WHERE username = ? ''',
                                             (GetLoginName,)).fetchone()
                updatedmonthnumber = int(monthnumber[0]) + 1

                cursor.execute(''' UPDATE users SET monthnumber = ? ''', (updatedmonthnumber,))
                db.commit()

                cursor.execute(''' INSERT INTO history (username, foodbudget, educationbudget, groceriesbudget, 
                fuelbudget, clothingbudget, transportbudget, utilitiesbudget, healthbudget, 
                insurancebudget, othersbudget, food, education, groceries, fuel, clothing, 
                transport, utilities, health, insurance, others, monthnumber, totalbudget, totalusage, 
                highestcat, highestvalue, lowestcat, lowestvalue ) VALUES  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                               (GetLoginName, foodBudgetHistory[0], educationBudgetHistory[0], groceriesBudgetHistory[0],
                                fuelBudgetHistory[0], clothingBudgetHistory[0], transportBudgetHistory[0],
                                utilitiesBudgetHistory[0], healthBudgetHistory[0], insuranceBudgetHistory[0],
                                othersBudgetHistory[0], foodHistory[0], educationHistory[0], groceriesHistory[0],
                                fuelHistory[0], clothingHistory[0], transportHistory[0], utilitiesHistory[0],
                                healthHistory[0], insuranceHistory[0], othersHistory[0], updatedmonthnumber,
                                totalBudgetHistory[0], totalUsageHistory[0], highestCatHistory[0], highestValueHistory[0],
                                lowestCatHistory[0], lowestValueHistory[0]))
                db.commit()


                cursor.execute(''' UPDATE users SET dateinitial = ? WHERE username = ? ''', (now, GetLoginName))
                db.commit()
                days = calendar.monthrange(now.year, now.month)[1]
                afterOneMonth = now + datetime.timedelta(days=days)
                cursor.execute(''' UPDATE users SET dateafteronemonth = ? WHERE username = ? ''',
                               (afterOneMonth, GetLoginName))
                db.commit()


                cursor.execute(''' UPDATE users SET foodbudget = 0.0, educationbudget = 0.0, groceriesbudget = 0.0, fuelbudget = 0.0, 
                                            clothingbudget = 0.0, transportbudget = 0.0, utilitiesbudget = 0.0, healthbudget = 0.0, insurancebudget = 0.0, othersbudget = 0.0, 
                                            food = 0.0, education = 0.0, groceries = 0.0, fuel = 0.0, clothing = 0.0, transport = 0.0, utilities = 0.0, health = 0.0, 
                                            insurance = 0.0, others = 0.0 WHERE username = ? ''', (GetLoginName, ))
                db.commit()

                tkinter.messagebox.showinfo("Notification",
                                      "It's already been a month. You are now being redirected to the budgeting interface to enter your budget for this month")
                LoginFrame.pack_forget()
                MainInterfaceFrame.pack_forget()
                BudgetingFrame.pack()

            cursor.execute(''' SELECT foodbudget, educationbudget, groceriesbudget, fuelbudget, clothingbudget, transportbudget, 
                                                        utilitiesbudget, healthbudget, insurancebudget, othersbudget FROM users WHERE username=?''',
                           (GetLoginName,))
            budgetValues = cursor.fetchone()

            cursor.execute(''' SELECT food, education, groceries, fuel, clothing, transport, 
                                                        utilities, health, insurance, others FROM users WHERE username=?''',
                           (GetLoginName,))
            usageValues = cursor.fetchone()

            TotalBudget = 0
            for values in budgetValues:
                TotalBudget = TotalBudget + values

            TotalUsage = 0
            highestUsage = 0
            lowestUsage = 99999999
            highestUsageCat = 'Nil'
            lowestUsageCat = 'Nil'
            counter = 0
            overBudget = 0
            overBudgetCat = []
            i = 0
            categoryList = ['Food', 'Education', 'Groceries', 'Fuel', 'Clothing', 'Transport', 'Utilities', 'Health', 'Insurance', 'Others']
            for values in usageValues:
                if values > budgetValues[i]:
                    overBudgetCat.append(categoryList[i])
                    overBudget = overBudget + 1
                i = i + 1

            for values in usageValues:
                TotalUsage = TotalUsage + values
                if values > highestUsage:
                    highestUsage = values
                    if counter == 0:
                        highestUsageCat = 'Food'
                    elif counter == 1:
                        highestUsageCat = 'Education'
                    elif counter == 2:
                        highestUsageCat = 'Groceries'
                    elif counter == 3:
                        highestUsageCat = 'Fuel'
                    elif counter == 4:
                        highestUsageCat = 'Clothing'
                    elif counter == 5:
                        highestUsageCat = 'Transport'
                    elif counter == 6:
                        highestUsageCat = 'Utilities'
                    elif counter == 7:
                        highestUsageCat = 'Health'
                    elif counter == 8:
                        highestUsageCat = 'Insurance'
                    elif counter == 9:
                        highestUsageCat = 'Others'
                counter = counter + 1
            counter = 0
            for values in usageValues:
                if values < lowestUsage and values != 0:
                    lowestUsage = values
                    if counter == 0:
                        lowestUsageCat = 'Food'
                    elif counter == 1:
                        lowestUsageCat = 'Education'
                    elif counter == 2:
                        lowestUsageCat = 'Groceries'
                    elif counter == 3:
                        lowestUsageCat = 'Fuel'
                    elif counter == 4:
                        lowestUsageCat = 'Clothing'
                    elif counter == 5:
                        lowestUsageCat = 'Transport'
                    elif counter == 6:
                        lowestUsageCat = 'Utilities'
                    elif counter == 7:
                        lowestUsageCat = 'Health'
                    elif counter == 8:
                        lowestUsageCat = 'Insurance'
                    elif counter == 9:
                        lowestUsageCat = 'Others'

                counter = counter + 1

            text = ''
            for x in overBudgetCat:
                text = text + x + '\n'

            state = cursor.execute(''' SELECT state FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()

            if state[0] == 1:
                if overBudget > 0:
                    tkinter.messagebox.showwarning("Warning",
                                                   "You have exceeded the budget limit for the following categories:" + "\n" + "\n" + text + "\n" + "\n" + "Be careful while spending in the above categories")

                if TotalUsage > 0 and TotalBudget > 0:
                    percentage = (float(TotalUsage) / float(TotalBudget)) * 100
                    if percentage > 100:
                        tkinter.messagebox.showwarning("Warning", "You have exceeded your total budget for this month")
                    elif percentage >= 70:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded 70% of your budget for this month. Be careful with your spending")
                c.select()
            else:
                c.deselect()

        else:
            tkinter.messagebox.showerror("Error", "Wrong Password")
    else:
        tkinter.messagebox.showerror("Error", "User does not exist. Please register first.")


def onClickExpenditure():
    MainInterfaceFrame.pack_forget()
    ExpenditureInterface.pack()

def onClickProfile():
    MainInterfaceFrame.pack_forget()
    ProfileFrame.pack()

def onClickSummary():
    MainInterfaceFrame.pack_forget()
    SummaryFrame.pack()
    monthEndDate = cursor.execute(''' SELECT dateafteronemonth FROM users WHERE username = ?''', (GetLoginName,)).fetchone()
    today = datetime.datetime.today()
    daysLeft = Label(SummaryFrame, text=(datetime.datetime.strptime(monthEndDate[0], '%Y-%m-%d %H:%M:%S.%f') - today).days)
    daysLeft.grid(row=1, column=1)

    cursor.execute(''' SELECT foodbudget, educationbudget, groceriesbudget, fuelbudget, clothingbudget, transportbudget, 
                                                            utilitiesbudget, healthbudget, insurancebudget, othersbudget FROM users WHERE username=?''',
                   (GetLoginName,))
    budgetValues = cursor.fetchone()

    cursor.execute(''' SELECT food, education, groceries, fuel, clothing, transport, 
                                                            utilities, health, insurance, others FROM users WHERE username=?''',
                   (GetLoginName,))
    usageValues = cursor.fetchone()

    TotalBudget = 0
    for values in budgetValues:
        TotalBudget = TotalBudget + values

    global TotalUsage
    global highestUsage
    global lowestUsage
    global highestUsageCat
    global lowestUsageCat

    TotalUsage = 0
    highestUsage = 0
    lowestUsage = 99999999999999999999999
    highestUsageCat = 'Nil'
    lowestUsageCat = 'Nil'
    counter = 0

    for values in usageValues:
        TotalUsage = TotalUsage + values
        if values > highestUsage:
            highestUsage = values
            if counter == 0:
                highestUsageCat = 'Food'
            elif counter == 1:
                highestUsageCat = 'Education'
            elif counter == 2:
                highestUsageCat = 'Groceries'
            elif counter == 3:
                highestUsageCat = 'Fuel'
            elif counter == 4:
                highestUsageCat = 'Clothing'
            elif counter == 5:
                highestUsageCat = 'Transport'
            elif counter == 6:
                highestUsageCat = 'Utilities'
            elif counter == 7:
                highestUsageCat = 'Health'
            elif counter == 8:
                highestUsageCat = 'Insurance'
            elif counter == 9:
                highestUsageCat = 'Others'
        counter = counter + 1
    counter = 0
    for values in usageValues:
        if values < lowestUsage and values != 0:
            lowestUsage = values
            if counter == 0:
                lowestUsageCat = 'Food'
            elif counter == 1:
                lowestUsageCat = 'Education'
            elif counter == 2:
                lowestUsageCat = 'Groceries'
            elif counter == 3:
                lowestUsageCat = 'Fuel'
            elif counter == 4:
                lowestUsageCat = 'Clothing'
            elif counter == 5:
                lowestUsageCat = 'Transport'
            elif counter == 6:
                lowestUsageCat = 'Utilities'
            elif counter == 7:
                lowestUsageCat = 'Health'
            elif counter == 8:
                lowestUsageCat = 'Insurance'
            elif counter == 9:
                lowestUsageCat = 'Others'

        counter = counter + 1

    if lowestUsage == 99999999999999999999999:
        lowestUsage = 0
    if highestUsageCat == 'Nil':
        highestUsageCat = 'TBD'
    if lowestUsageCat == 'Nil':
        lowestUsageCat = 'TBD'

    quotaleft = TotalBudget - TotalUsage
    if quotaleft == 0:
        quotaleft = 0
    elif quotaleft < 0:
        quotaleft = str(quotaleft) + " ,the negative sign indicates the amount has exceeded the budget"
    averagedaily = 0
    Days = 30.0 - float((datetime.datetime.strptime(monthEndDate[0], '%Y-%m-%d %H:%M:%S.%f') - today).days)
    if Days != 0:
        averagedaily = TotalUsage / Days
    else:
        averagedaily = TotalUsage

    food = cursor.execute(''' SELECT food FROM users where username = ? ''',
                                 (GetLoginName,)).fetchone()
    education = cursor.execute(''' SELECT education FROM users where username = ? ''',
                                      (GetLoginName,)).fetchone()
    groceries = cursor.execute(''' SELECT groceries FROM users where username = ? ''',
                                      (GetLoginName,)).fetchone()
    fuel = cursor.execute(''' SELECT fuel FROM users where username = ? ''',
                                 (GetLoginName,)).fetchone()
    clothing = cursor.execute(''' SELECT clothing FROM users where username = ? ''',
                                     (GetLoginName,)).fetchone()
    transport = cursor.execute(''' SELECT transport FROM users where username = ? ''',
                                      (GetLoginName,)).fetchone()
    utilities = cursor.execute(''' SELECT utilities FROM users where username = ? ''',
                                      (GetLoginName,)).fetchone()
    health = cursor.execute(''' SELECT health FROM users where username = ? ''',
                                   (GetLoginName,)).fetchone()
    insurance = cursor.execute(''' SELECT insurance FROM users where username = ? ''',
                                      (GetLoginName,)).fetchone()
    others = cursor.execute(''' SELECT others FROM users where username = ? ''',
                                   (GetLoginName,)).fetchone()

    QuotaLeftLabel = Label(SummaryFrame, text=quotaleft)
    QuotaLeftLabel.grid(row=2, column=1)

    TotalExpensesLabel = Label(SummaryFrame, text=TotalUsage)
    TotalExpensesLabel.grid(row=3, column=1)

    HighestUsageLabel = Label(SummaryFrame, text=str(highestUsageCat) + ', ' + str(highestUsage))
    HighestUsageLabel.grid(row=4, column=1)

    LowestUsageLabel = Label(SummaryFrame, text=str(lowestUsageCat) + ', ' + str(lowestUsage))
    LowestUsageLabel.grid(row=5, column=1)

    averagedailylabel = Label(SummaryFrame, text=averagedaily)
    averagedailylabel.grid(row=6, column=1)

    Label(SummaryFrame, text="Expenditure for Food: ").grid(row=7, column=0, sticky=E)
    foodsummary = Label(SummaryFrame, text=food[0])
    foodsummary.grid(row=7, column=1)

    Label(SummaryFrame, text="Expenditure for Education: ").grid(row=8, column=0, sticky=E)
    educationsummary = Label(SummaryFrame, text=education[0])
    educationsummary.grid(row=8, column=1)

    Label(SummaryFrame, text="Expenditure for Groceries: ").grid(row=9, column=0, sticky=E)
    groceriessummary = Label(SummaryFrame, text=groceries[0])
    groceriessummary.grid(row=9, column=1)

    Label(SummaryFrame, text="Expenditure for Fuel: ").grid(row=10, column=0, sticky=E)
    fuelsummary = Label(SummaryFrame, text=fuel[0])
    fuelsummary.grid(row=10, column=1)

    Label(SummaryFrame, text="Expenditure for Clothing: ").grid(row=11, column=0, sticky=E)
    clothingsummary = Label(SummaryFrame, text=clothing[0])
    clothingsummary.grid(row=11, column=1)

    Label(SummaryFrame, text="Expenditure for Transport: ").grid(row=12, column=0, sticky=E)
    transportsummary = Label(SummaryFrame, text=transport[0])
    transportsummary.grid(row=12, column=1)

    Label(SummaryFrame, text="Expenditure for Utilites: ").grid(row=13, column=0, sticky=E)
    utilitiessummary = Label(SummaryFrame, text=utilities[0])
    utilitiessummary.grid(row=13, column=1)

    Label(SummaryFrame, text="Expenditure for Health Care: ").grid(row=14, column=0, sticky=E)
    healthsummary = Label(SummaryFrame, text=health[0])
    healthsummary.grid(row=14, column=1)

    Label(SummaryFrame, text="Expenditure for Insurance: ").grid(row=15, column=0, sticky=E)
    insurancesummary = Label(SummaryFrame, text=insurance[0])
    insurancesummary.grid(row=15, column=1)

    Label(SummaryFrame, text="Expenditure for Others: ").grid(row=16, column=0, sticky=E)
    otherssummary = Label(SummaryFrame, text=others[0])
    otherssummary.grid(row=16, column=1)

    def backSummary():
        daysLeft.grid_forget()
        QuotaLeftLabel.grid_forget()
        TotalExpensesLabel.grid_forget()
        HighestUsageLabel.grid_forget()
        LowestUsageLabel.grid_forget()
        averagedailylabel.grid_forget()
        foodsummary.grid_forget()
        educationsummary.grid_forget()
        groceriessummary.grid_forget()
        fuelsummary.grid_forget()
        clothingsummary.grid_forget()
        transportsummary.grid_forget()
        utilitiessummary.grid_forget()
        healthsummary.grid_forget()
        insurancesummary.grid_forget()
        otherssummary.grid_forget()
        SummaryFrame.pack_forget()
        MainInterfaceFrame.pack()

    button1 = Button(SummaryFrame, text="Back", command=backSummary)
    button1.grid(row=17, columnspan=3)

def onClickBudgeting():
    MainInterfaceFrame.pack_forget()
    BudgetingFrame.pack()

    getFoodBudget = cursor.execute(''' SELECT foodbudget FROM users WHERE username = ?''',
                                   (GetLoginName,)).fetchone()
    foodbudgetlabel = Label(BudgetingFrame, text=getFoodBudget[0])
    foodbudgetlabel.grid(row=0, column=0)

    getEducationBudget = cursor.execute(''' SELECT educationbudget FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
    educationbudgetlabel = Label(BudgetingFrame, text=getEducationBudget[0])
    educationbudgetlabel.grid(row=1, column=0)

    getGroceriesBudget = cursor.execute(''' SELECT groceriesbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    groceriesbudgetlabel = Label(BudgetingFrame, text=getGroceriesBudget[0])
    groceriesbudgetlabel.grid(row=2, column=0)

    getFuelBudget = cursor.execute(''' SELECT fuelbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    fuelbudgetlabel = Label(BudgetingFrame, text=getFuelBudget[0])
    fuelbudgetlabel.grid(row=3, column=0)

    getClothingBudget = cursor.execute(''' SELECT clothingbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    clothingbudgetlabel = Label(BudgetingFrame, text=getClothingBudget[0])
    clothingbudgetlabel.grid(row=4, column=0)

    getTransportBudget = cursor.execute(''' SELECT transportbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    transportbudgetlabel = Label(BudgetingFrame, text=getTransportBudget[0])
    transportbudgetlabel.grid(row=5, column=0)

    getUtilitiesBudget = cursor.execute(''' SELECT utilitiesbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    utilitiesbudgetlabel = Label(BudgetingFrame, text=getUtilitiesBudget[0])
    utilitiesbudgetlabel.grid(row=6, column=0)

    getHealthBudget = cursor.execute(''' SELECT healthbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    healthbudgetlabel = Label(BudgetingFrame, text=getHealthBudget[0])
    healthbudgetlabel.grid(row=7, column=0)

    getInsuranceBudget = cursor.execute(''' SELECT insurancebudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    insurancebudgetlabel = Label(BudgetingFrame, text=getInsuranceBudget[0])
    insurancebudgetlabel.grid(row=8, column=0)

    getOthersBudget = cursor.execute(''' SELECT othersbudget FROM users WHERE username = ? ''',
                                        (GetLoginName,)).fetchone()
    othersbudgetlabel = Label(BudgetingFrame, text=getOthersBudget[0])
    othersbudgetlabel.grid(row=9, column=0)

def onClickHistory():
    global getMonthNumber
    global monthHistoryEntry
    global CheckHistory1
    getMonthNumber = cursor.execute(''' SELECT monthnumber FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
    Label(HistoryFrame, text="Our records show that you have history for data for " + str(getMonthNumber[0]) + " months. \n Please enter the number of months previosly to view the history for that month").grid(row=0, columnspan=2)
    monthHistoryEntry = Entry(HistoryFrame)
    monthHistoryEntry.grid(row=1, columnspan=2)
    monthHistoryEntry.focus_set()
    CheckHistory1 = Button(HistoryFrame, text="Enter", command=historyEnter1)
    CheckHistory1.grid(row=2, columnspan=2)
    backhistory = Button(HistoryFrame, text="Back", command=backToMainUI)
    backhistory.grid(row=30, columnspan=2)

    MainInterfaceFrame.pack_forget()
    HistoryFrame.pack()

def onClickInsertValue():
    global variable
    global inputCategoryValue
    obtainedCategory = variable.get()
    obtainedCategoryValue = inputCategoryValue.get()
    cursor.execute(''' SELECT food, education, groceries, fuel, clothing, transport, 
                        utilities, health, insurance, others FROM users WHERE username=?''', (GetLoginName,))
    values = cursor.fetchone()
    global initialValue
    global newValue
    if obtainedCategoryValue:
        if str(obtainedCategoryValue).isdigit() or obtainedCategoryValue.replace('.','',1).isdigit():
            if obtainedCategory == 'Food':
                initialValue = values[0]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET food = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT foodbudget FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT food FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100)> 70:
                            tkinter.messagebox.showwarning("Warning", "You surpassed 70 percent of your budget for Food. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning", "You have exceeded the budget for Food. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Education':
                initialValue = values[1]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET education = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT educationbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT education FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning", "You surpassed 70 percent of your budget for Education. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning", "You have exceeded the budget for Education. Be extra careful with your money")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Groceries':
                initialValue = values[2]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET groceries = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT groceriesbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT groceries FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Groceries. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Groceries. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Fuel':
                initialValue = values[3]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET fuel = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT fuelbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT fuel FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Fuel. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Fuel. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Clothing':
                initialValue = values[4]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET clothing = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT clothingbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT clothing FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Clothing. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Clothing. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Transport':
                initialValue = values[5]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET transport = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT transportbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT transport FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Transport. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Transport. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Utilities':
                initialValue = values[6]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET utilities = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT utilitiesbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT utilities FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Utilities. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Utilities. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Health Care':
                initialValue = values[7]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET health = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT healthbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT health FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Health Care. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Health Care. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Insurance':
                initialValue = values[8]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET insurance = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT insurancebudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT insurance FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Insurance. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Insurance. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            elif obtainedCategory == 'Others':
                initialValue = values[9]
                newValue = float(initialValue) + float(obtainedCategoryValue)
                cursor.execute(''' UPDATE users SET others = ? WHERE username = ? ''', (newValue, GetLoginName,))
                db.commit()
                testB = cursor.execute(''' SELECT othersbudget FROM users WHERE username = ? ''',
                                       (GetLoginName,)).fetchone()
                testU = cursor.execute(''' SELECT others FROM users WHERE username = ? ''', (GetLoginName,)).fetchone()
                if float(testB[0]) > 0.0:
                    if ((float(testU[0]) / float(testB[0])) * 100) < 100:
                        if ((float(testU[0]) / float(testB[0])) * 100) > 70:
                            tkinter.messagebox.showwarning("Warning",
                                                           "You surpassed 70 percent of your budget for Others. Be wise with your spendings.")
                    else:
                        tkinter.messagebox.showwarning("Warning",
                                                       "You have exceeded the budget for Others. Be extra careful with your money.")
                else:
                    tkinter.messagebox.showwarning("Warning", "You have entered expenditure without adding a budget")

            tkinter.messagebox.showinfo("Success", "Value successfully registered!")
        else:
            tkinter.messagebox.showerror("Error", "Please enter a valid value")
    else:
        tkinter.messagebox.showerror("Error", "Please enter a value")

    inputCategoryValue.delete(0, END)
    inputCategoryValue.insert(0, "")

def backToMainUI():
    LoginFrame.pack_forget()
    RegisterFrame.pack_forget()
    ExpenditureInterface.pack_forget()
    ProfileFrame.pack_forget()
    BudgetingFrame.pack_forget()
    SummaryFrame.pack_forget()
    HistoryFrame.pack_forget()
    MainInterfaceFrame.pack()

def onClickSave():
    global getTestUsername
    global getNewPassword
    global getConfirmNewPassword
    getTestUsername = e1.get()
    getNewPassword = e2.get()
    getConfirmNewPassword = e3.get()
    if len(getTestUsername) <= 0:
        tkinter.messagebox.showerror("Error", "Please fill up everything")
    elif len(getNewPassword) <= 0:
        tkinter.messagebox.showerror("Error", "Please fill up everything")
    elif getTestUsername != GetLoginName:
        tkinter.messagebox.showerror("Error", "The username entered is not the same as the one used to log in!")
    elif getNewPassword != getConfirmNewPassword:
        tkinter.messagebox.showerror("Error", "Passwords do not match. Please try again.")
    elif getNewPassword == getTestUsername:
        tkinter.messagebox.showerror("Error", "Password cannot be the same as the username for security purposes")
    else:
        cursor.execute(''' UPDATE users SET password = ? WHERE username = ? ''', (getNewPassword, getTestUsername,))
        db.commit()
        tkinter.messagebox.showinfo("Success", "Successfully changed password. You can now use your new password to log in.")
    e1.delete(0, END)
    e1.insert(0, "")
    e2.delete(0, END)
    e2.insert(0, "")
    e3.delete(0, END)
    e3.insert(0, "")


def historyEnter1():
    CheckHistory1.grid_forget()
    number = monthHistoryEntry.get()
    names = []
    rowid = []
    MonthNumber = []
    specificuser = 0

    for row in cursor.execute(''' SELECT username FROM history ''').fetchall():
        names.append(row[0])

    for row in cursor.execute(''' SELECT id FROM history ''').fetchall():
        rowid.append(row[0])

    for row in cursor.execute(''' SELECT monthnumber FROM history ''').fetchall():
        MonthNumber.append(row[0])

    if str(number).isdigit():
        if int(number) <= int(getMonthNumber[0]):
            c = 0
            for username in names:
                if username == GetLoginName:
                    if MonthNumber[c] == int(number):
                        specificuser = rowid[c]
                c = c + 1

            Label(HistoryFrame, text="Food Budget: ").grid(row=3, column=0, sticky=E)
            getFoodBudget = cursor.execute(''' SELECT foodbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            foodbudgetlabel = Label(HistoryFrame, text=getFoodBudget)
            foodbudgetlabel.grid(row=3, column=1, sticky=W)

            Label(HistoryFrame, text="Education Budget: ").grid(row=4, column=0, sticky=E)
            getEducationBudget = cursor.execute(''' SELECT educationbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            educationbudgetlabel = Label(HistoryFrame, text=getEducationBudget)
            educationbudgetlabel.grid(row=4, column=1, sticky=W)

            Label(HistoryFrame, text="Groceries Budget: ").grid(row=5, column=0, sticky=E)
            getGroceriesBudget = cursor.execute(''' SELECT groceriesbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            groceriesbudgetlabel = Label(HistoryFrame, text=getGroceriesBudget)
            groceriesbudgetlabel.grid(row=5, column=1, sticky=W)

            Label(HistoryFrame, text="Fuel Budget: ").grid(row=6, column=0, sticky=E)
            getFuelBudget = cursor.execute(''' SELECT fuelbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            fuelbudgetlabel = Label(HistoryFrame, text=getFuelBudget)
            fuelbudgetlabel.grid(row=6, column=1, sticky=W)

            Label(HistoryFrame, text="Clothing Budget: ").grid(row=7, column=0, sticky=E)
            getClothingBudget = cursor.execute(''' SELECT clothingbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            clothingbudgetlabel = Label(HistoryFrame, text=getClothingBudget)
            clothingbudgetlabel.grid(row=7, column=1, sticky=W)

            Label(HistoryFrame, text="Transport Budget: ").grid(row=8, column=0, sticky=E)
            getTransportBudget = cursor.execute(''' SELECT transportbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            transportbudgetlabel = Label(HistoryFrame, text=getTransportBudget)
            transportbudgetlabel.grid(row=8, column=1, sticky=W)

            Label(HistoryFrame, text="Utilities Budget: ").grid(row=9, column=0, sticky=E)
            getUtilitiesBudget = cursor.execute(''' SELECT utilitiesbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            utilitiesbudgetlabel = Label(HistoryFrame, text=getUtilitiesBudget)
            utilitiesbudgetlabel.grid(row=9, column=1, sticky=W)

            Label(HistoryFrame, text="Health Budget: ").grid(row=10, column=0, sticky=E)
            getHealthBudget = cursor.execute(''' SELECT healthbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            healthbudgetlabel = Label(HistoryFrame, text=getHealthBudget)
            healthbudgetlabel.grid(row=10, column=1, sticky=W)

            Label(HistoryFrame, text="Insurance Budget: ").grid(row=11, column=0, sticky=E)
            getInsuranceBudget = cursor.execute(''' SELECT insurancebudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            insurancebudgetlabel = Label(HistoryFrame, text=getInsuranceBudget)
            insurancebudgetlabel.grid(row=11, column=1, sticky=W)

            Label(HistoryFrame, text="Others Budget: ").grid(row=12, column=0, sticky=E)
            getOthersBudget = cursor.execute(''' SELECT othersbudget FROM history WHERE id = ?''',
                                           (specificuser,)).fetchone()
            othersbudgetlabel = Label(HistoryFrame, text=getOthersBudget)
            othersbudgetlabel.grid(row=12, column=1, sticky=W)

            Label(HistoryFrame, text="Food Expenditure: ").grid(row=13, column=0, sticky=E)
            getFood = cursor.execute(''' SELECT food FROM history WHERE id = ?''',
                                             (specificuser,)).fetchone()
            foodlabel = Label(HistoryFrame, text=getFood)
            foodlabel.grid(row=13, column=1, sticky=W)

            Label(HistoryFrame, text="Education Expenditure: ").grid(row=14, column=0, sticky=E)
            getEducation = cursor.execute(''' SELECT education FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            educationlabel = Label(HistoryFrame, text=getEducation)
            educationlabel.grid(row=14, column=1, sticky=W)

            Label(HistoryFrame, text="Groceries Expenditure: ").grid(row=15, column=0, sticky=E)
            getGroceries = cursor.execute(''' SELECT groceries FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            grocerieslabel = Label(HistoryFrame, text=getGroceries)
            grocerieslabel.grid(row=15, column=1, sticky=W)

            Label(HistoryFrame, text="Fuel Expenditure: ").grid(row=16, column=0, sticky=E)
            getFuel = cursor.execute(''' SELECT fuel FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            fuellabel = Label(HistoryFrame, text=getFuel)
            fuellabel.grid(row=16, column=1, sticky=W)

            Label(HistoryFrame, text="Clothing Expenditure: ").grid(row=17, column=0, sticky=E)
            getClothing = cursor.execute(''' SELECT clothing FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            clothinglabel = Label(HistoryFrame, text=getClothing)
            clothinglabel.grid(row=17, column=1, sticky=W)

            Label(HistoryFrame, text="Transport Expenditure: ").grid(row=18, column=0, sticky=E)
            getTransport = cursor.execute(''' SELECT transport FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            transportlabel = Label(HistoryFrame, text=getTransport)
            transportlabel.grid(row=18, column=1, sticky=W)

            Label(HistoryFrame, text="Utilities Expenditure: ").grid(row=19, column=0, sticky=E)
            getUtilities = cursor.execute(''' SELECT utilities FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            utilitieslabel = Label(HistoryFrame, text=getUtilities)
            utilitieslabel.grid(row=19, column=1, sticky=W)

            Label(HistoryFrame, text="Health Expenditure: ").grid(row=20, column=0, sticky=E)
            getHealth = cursor.execute(''' SELECT health FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            healthlabel = Label(HistoryFrame, text=getHealth)
            healthlabel.grid(row=20, column=1, sticky=W)

            Label(HistoryFrame, text="Insurance Expenditure: ").grid(row=21, column=0, sticky=E)
            getInsurance = cursor.execute(''' SELECT insurance FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            insurancelabel = Label(HistoryFrame, text=getInsurance)
            insurancelabel.grid(row=21, column=1, sticky=W)

            Label(HistoryFrame, text="Others Expenditure: ").grid(row=22, column=0, sticky=E)
            getOthers = cursor.execute(''' SELECT others FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            otherslabel = Label(HistoryFrame, text=getOthers)
            otherslabel.grid(row=22, column=1, sticky=W)

            Label(HistoryFrame, text="Total Budget: ").grid(row=23, column=0, sticky=E)
            getTotalBudget = cursor.execute(''' SELECT totalbudget FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            totalbudgetlabel = Label(HistoryFrame, text=getTotalBudget)
            totalbudgetlabel.grid(row=23, column=1, sticky=W)

            Label(HistoryFrame, text="Total Usage: ").grid(row=24, column=0, sticky=E)
            getTotalUsage = cursor.execute(''' SELECT totalusage FROM history WHERE id = ?''',
                                     (specificuser,)).fetchone()
            totalusagelabel = Label(HistoryFrame, text=getTotalUsage)
            totalusagelabel.grid(row=24, column=1, sticky=W)

            def historyEnter2():
                foodbudgetlabel.grid_forget()
                educationbudgetlabel.grid_forget()
                groceriesbudgetlabel.grid_forget()
                fuelbudgetlabel.grid_forget()
                clothingbudgetlabel.grid_forget()
                transportbudgetlabel.grid_forget()
                utilitiesbudgetlabel.grid_forget()
                healthbudgetlabel.grid_forget()
                insurancebudgetlabel.grid_forget()
                othersbudgetlabel.grid_forget()
                foodlabel.grid_forget()
                educationlabel.grid_forget()
                grocerieslabel.grid_forget()
                fuellabel.grid_forget()
                clothinglabel.grid_forget()
                transportlabel.grid_forget()
                utilitieslabel.grid_forget()
                healthlabel.grid_forget()
                insurancelabel.grid_forget()
                otherslabel.grid_forget()
                totalbudgetlabel.grid_forget()
                totalusagelabel.grid_forget()
                historyEnter1()

            CheckHistory2 = Button(HistoryFrame, text="Enter", command=historyEnter2)
            CheckHistory2.grid(row=2, columnspan=2)



        else:
            tkinter.messagebox.showerror("Error", "Please enter a number which is in range of the previous months")
    else:
        tkinter.messagebox.showerror("Error", "Please enter a valid number for the months")

def quit():
    exit()

'''

LOGIN FRAME 

'''
photo = PhotoImage(file="savely.png")
label = Label(LoginFrame, image=photo)
label.grid(row=0, columnspan=2, sticky=E)


label_1 = Label(LoginFrame, text="Name: ")      #Display the text(name) in login page
label_2 = Label(LoginFrame, text="Password:")   #Display the text(password) in login page
entry_1 = Entry(LoginFrame)                     #Creates a field for users to enter their login name
entry_2 = Entry(LoginFrame)                     #Creates a field for users to enter their login password
entry_2.config(show='*')
entry_1.focus_set()                             #Tells the program to focus on user login name input
entry_2.focus_set()                             #Tells the program to focus on user login password input

label_1.grid(row=1, column=0, sticky=E)
label_2.grid(row=2, column=0, sticky=E)

entry_1.grid(row=1, column=1)
entry_2.grid(row=2, column=1)

LoginButton = Button(LoginFrame, text="Login", fg="blue", command=LoginCredentials)
LoginButton.grid(columnspan=2)

RegisterButton = Button(LoginFrame, text="Register", fg="blue", command=LoginRegisterClicked)
RegisterButton.grid(columnspan=2)

QuitButton = Button(LoginFrame, text="Exit Program", fg="blue", command=quit)
QuitButton.grid(columnspan=2)

'''

END LOGIN FRAME

'''

'''

REGISTER FRAME

'''

Info_1 = Label(RegisterFrame, text="Username")
Info_2 = Label(RegisterFrame, text="Password")
Info_3 = Label(RegisterFrame, text="Confirm Password")
TextRegister = Button(RegisterFrame, text="Register", fg="blue", command=RegisterClicked)
TextRegister.grid(row=3, columnspan=2)
RegFrameBackLogin = Button(RegisterFrame,text="Go back to login", fg="blue", command=fromRegToLogPage)
RegFrameBackLogin.grid(row=4, columnspan=2)

InfoInput_1 = Entry(RegisterFrame)
InfoInput_2 = Entry(RegisterFrame)
InfoInput_2.config(show='*')
InfoInput_3 = Entry(RegisterFrame)
InfoInput_3.config(show='*')
InfoInput_1.focus_set()
InfoInput_2.focus_set()
InfoInput_3.focus_set()

Info_1.grid(row=0, column=0, sticky=E)
Info_2.grid(row=1, column=0, sticky=E)
Info_3.grid(row=2, column=0, sticky=E)

InfoInput_1.grid(row=0, column=1)
InfoInput_2.grid(row=1, column=1)
InfoInput_3.grid(row=2, column=1)



'''

END REGISTER FRAME

'''



''''

MAIN INTERFACE 

'''

def logout():
    MainInterfaceFrame.pack_forget()
    LoginFrame.pack()

budgetingButton = Button(MainInterfaceFrame, text="Budgeting", command=onClickBudgeting, bg="green", fg="white", activebackground="white", activeforeground="green", font=('Verdana',15))
budgetingButton.pack(ipadx=9999, ipady=10)

expenditureButton = Button(MainInterfaceFrame, text="Expenditure", command=onClickExpenditure, bg="blue", fg="white", activebackground="white", activeforeground="blue", font=('Verdana',15))
expenditureButton.pack(ipadx=9999, ipady=10)

summaryButton = Button(MainInterfaceFrame, text="Summary", command=onClickSummary, bg="red", fg="white", activebackground="white", activeforeground="red", font=('Verdana',15))
summaryButton.pack(ipadx=9999, ipady=10)

profileButton = Button(MainInterfaceFrame, text="Profile", command=onClickProfile, bg="orange", fg="white", activebackground="white", activeforeground="orange", font=('Verdana',15))
profileButton.pack(ipadx=9999, ipady=10)

historyButton = Button(MainInterfaceFrame, text="History", command=onClickHistory, bg="purple", fg="white", activebackground="white", activeforeground="purple", font=('Verdana',15))
historyButton.pack(ipadx=9999, ipady=10)

logOutButton = Button(MainInterfaceFrame, text="Log Out", bg="black", fg="white", activebackground="white", activeforeground="black", command=logout)
logOutButton.pack(pady=60, ipadx=100, ipady=10)

'''

END MAIN INTERFACE

'''

'''

EXPENDITURE INTERFACE

'''


expenditureLabel = Label(ExpenditureInterface, text="Expenditure \n\n Select a category from the drop down then input the amount you have spent on that category \n")
expenditureLabel.grid(row=0, columnspan=2)

categoryText = Label(ExpenditureInterface, text="Choose your category:")
categoryValueText = Label(ExpenditureInterface, text="Insert Value:")

variable = StringVar(ExpenditureInterface)
variable.set("Food") #default value

inputCategory = OptionMenu(ExpenditureInterface, variable, "Food", "Education", "Groceries", "Fuel",
                           "Clothing", "Transport", "Utilities", "Health Care", "Insurance", "Others")
inputCategoryValue = Entry(ExpenditureInterface)

insertValueButton = Button(ExpenditureInterface, text="Insert Value", command=onClickInsertValue)
backToMainUIButtonE = Button(ExpenditureInterface, text="Back", command=backToMainUI)

inputCategory.focus_set()
inputCategoryValue.focus_set()

categoryText.grid(row=1, column=0, sticky=E)
categoryValueText.grid(row=2, column=0, sticky=E)

inputCategory.grid(row=1, column=1)
inputCategoryValue.grid(row=2, column=1)

insertValueButton.grid(row=3, columnspan=2)
backToMainUIButtonE.grid(row=4, columnspan=2)




'''

END EXPENDITURE INTERFACE

'''

'''

PROFILE FRAME

'''

def notification():
    getState = var.get()
    cursor.execute('''  UPDATE users SET state = ? WHERE username = ? ''', (getState, GetLoginName))

Label(ProfileFrame, text="You can change your account password here. You may also choose to disable the notifications.\n").grid(row=0, columnspan=2)
Label(ProfileFrame, text="Username:").grid(row=1, column=0, sticky=E)
Label(ProfileFrame, text="New Password:").grid(row=2, column=0, sticky=E)
Label(ProfileFrame, text="Confirm password:").grid(row=3, column=0, sticky=E)


e1 = Entry(ProfileFrame)
e2 = Entry(ProfileFrame)
e2.config(show='*')
e3 = Entry(ProfileFrame)
e3.config(show='*')
b1 = Button(ProfileFrame, text="Save", command=onClickSave)

e1.grid(row=1, column=1, sticky=W)
e2.grid(row=2, column=1, sticky=W)
e3.grid(row=3, column=1, sticky=W)
b1.grid(row=4, columnspan=2)

backToMainUIButtonE = Button(ProfileFrame, text="Back", command=backToMainUI)
backToMainUIButtonE.grid(row=5, columnspan=2)

var = IntVar()
c = Checkbutton(ProfileFrame, text="Toggle this button to turn notification on or off", variable=var, command=notification)
c.grid(row=6, columnspan=3, pady=50)

'''

END PROFILE FRAME

'''

''' 

SUMMARY FRAME

'''

words = Label(SummaryFrame, text="Summary \n This page displays the summary of your expenditure \n", bg="green", fg="white")
Label1 = Label(SummaryFrame, text="Days left before month ends: ")
Label2 = Label(SummaryFrame, text="Quota left for the month: ")
Label3 = Label(SummaryFrame, text="Total expenses so far: ")
Label4 = Label(SummaryFrame, text="Highest expenditure so far by category: ")
Label5 = Label(SummaryFrame, text="Lowest expenditure so far by category: ")
Label16 = Label(SummaryFrame, text="Average daily expenditure: ")

words.grid(row=0, columnspan=3)
Label1.grid(row=1, column=0, sticky=E)
Label2.grid(row=2, column=0, sticky=E)
Label3.grid(row=3, column=0, sticky=E)
Label4.grid(row=4, column=0, sticky=E)
Label5.grid(row=5, column=0, sticky=E)
Label16.grid(row=6, column=0, sticky=E)


'''

END SUMMARY FRAME

'''


'''

BUDGETING FRAME

'''

def radButton1():
    radEntry1.grid(column=2, row=0)
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton2():
    radEntry1.grid_forget()
    radEntry2.grid(column=2, row=1)
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton3():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid(column=2, row=2)
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton4():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid(column=2, row=3)
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton5():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid(column=2, row=4)
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton6():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid(column=2, row=5)
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton7():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid(column=2, row=6)
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton8():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid(column=2, row=7)
    radEntry9.grid_forget()
    radEntry10.grid_forget()

def radButton9():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid(column=2, row=8)
    radEntry10.grid_forget()

def radButton10():
    radEntry1.grid_forget()
    radEntry2.grid_forget()
    radEntry3.grid_forget()
    radEntry4.grid_forget()
    radEntry5.grid_forget()
    radEntry6.grid_forget()
    radEntry7.grid_forget()
    radEntry8.grid_forget()
    radEntry9.grid_forget()
    radEntry10.grid(column=2, row=9)

def budgetingButtonEnter():

    cursor.execute(''' SELECT foodbudget, educationbudget, groceriesbudget, fuelbudget, clothingbudget, transportbudget, 
                            utilitiesbudget, healthbudget, insurancebudget, othersbudget FROM users WHERE username=?''', (GetLoginName,))
    values = cursor.fetchone()

    if selected.get():
        if radEntry1.get() or radEntry2.get() or radEntry3.get() or radEntry4.get() or radEntry5.get() or radEntry6.get() or radEntry7.get() or radEntry8.get() or radEntry9.get() or radEntry10.get():
            if str(radEntry1.get()).isdigit() or str(radEntry2.get()).isdigit() or str(radEntry3.get()).isdigit() or \
                    str(radEntry4.get()).isdigit() or str(radEntry5.get()).isdigit() or str(radEntry6.get()).isdigit() or str(radEntry7.get()).isdigit() \
                    or str(radEntry8.get()).isdigit() or str(radEntry9.get()).isdigit() or str(radEntry10.get()).isdigit():
                if selected.get() == 1:
                    budgetInput = radEntry1.get()
                    iValue = values[0]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET foodbudget = ? WHERE username = ? ''', (nValue, GetLoginName,))
                    db.commit()
                    radEntry1.delete(0, END)
                    radEntry1.insert(0, "")
                elif selected.get() == 2:
                    budgetInput = radEntry2.get()
                    iValue = values[1]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET educationbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry2.delete(0, END)
                    radEntry2.insert(0, "")
                elif selected.get() == 3:
                    budgetInput = radEntry3.get()
                    iValue = values[2]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET groceriesbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry3.delete(0, END)
                    radEntry3.insert(0, "")
                elif selected.get() == 4:
                    budgetInput = radEntry4.get()
                    iValue = values[3]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET fuelbudget = ? WHERE username = ? ''', (nValue, GetLoginName,))
                    db.commit()
                    radEntry4.delete(0, END)
                    radEntry4.insert(0, "")
                elif selected.get() == 5:
                    budgetInput = radEntry5.get()
                    iValue = values[4]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET clothingbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry5.delete(0, END)
                    radEntry5.insert(0, "")
                elif selected.get() == 6:
                    budgetInput = radEntry6.get()
                    iValue = values[5]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET transportbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry6.delete(0, END)
                    radEntry6.insert(0, "")
                elif selected.get() == 7:
                    budgetInput = radEntry7.get()
                    iValue = values[6]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET utilitiesbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry7.delete(0, END)
                    radEntry7.insert(0, "")
                elif selected.get() == 8:
                    budgetInput = radEntry8.get()
                    iValue = values[7]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET healthbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry8.delete(0, END)
                    radEntry8.insert(0, "")
                elif selected.get() == 9:
                    budgetInput = radEntry9.get()
                    iValue = values[8]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET insurancebudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry9.delete(0, END)
                    radEntry9.insert(0, "")
                elif selected.get() == 10:
                    budgetInput = radEntry10.get()
                    iValue = values[9]
                    nValue = float(iValue) + float(budgetInput)
                    cursor.execute(''' UPDATE users SET othersbudget = ? WHERE username = ? ''',
                                   (nValue, GetLoginName,))
                    db.commit()
                    radEntry10.delete(0, END)
                    radEntry10.insert(0, "")
                tkinter.messagebox.showinfo("Success", "Value successfully registered")

                getFoodBudget = cursor.execute(''' SELECT foodbudget FROM users WHERE username = ?''',
                                               (GetLoginName,)).fetchone()
                foodbudgetlabel = Label(BudgetingFrame, text=getFoodBudget[0])
                foodbudgetlabel.grid(row=0, column=0)

                getEducationBudget = cursor.execute(''' SELECT educationbudget FROM users WHERE username = ? ''',
                                                    (GetLoginName,)).fetchone()
                educationbudgetlabel = Label(BudgetingFrame, text=getEducationBudget[0])
                educationbudgetlabel.grid(row=1, column=0)

                getGroceriesBudget = cursor.execute(''' SELECT groceriesbudget FROM users WHERE username = ? ''',
                                                    (GetLoginName,)).fetchone()
                groceriesbudgetlabel = Label(BudgetingFrame, text=getGroceriesBudget[0])
                groceriesbudgetlabel.grid(row=2, column=0)

                getFuelBudget = cursor.execute(''' SELECT fuelbudget FROM users WHERE username = ? ''',
                                               (GetLoginName,)).fetchone()
                fuelbudgetlabel = Label(BudgetingFrame, text=getFuelBudget[0])
                fuelbudgetlabel.grid(row=3, column=0)

                getClothingBudget = cursor.execute(''' SELECT clothingbudget FROM users WHERE username = ? ''',
                                                   (GetLoginName,)).fetchone()
                clothingbudgetlabel = Label(BudgetingFrame, text=getClothingBudget[0])
                clothingbudgetlabel.grid(row=4, column=0)

                getTransportBudget = cursor.execute(''' SELECT transportbudget FROM users WHERE username = ? ''',
                                                    (GetLoginName,)).fetchone()
                transportbudgetlabel = Label(BudgetingFrame, text=getTransportBudget[0])
                transportbudgetlabel.grid(row=5, column=0)

                getUtilitiesBudget = cursor.execute(''' SELECT utilitiesbudget FROM users WHERE username = ? ''',
                                                    (GetLoginName,)).fetchone()
                utilitiesbudgetlabel = Label(BudgetingFrame, text=getUtilitiesBudget[0])
                utilitiesbudgetlabel.grid(row=6, column=0)

                getHealthBudget = cursor.execute(''' SELECT healthbudget FROM users WHERE username = ? ''',
                                                 (GetLoginName,)).fetchone()
                healthbudgetlabel = Label(BudgetingFrame, text=getHealthBudget[0])
                healthbudgetlabel.grid(row=7, column=0)

                getInsuranceBudget = cursor.execute(''' SELECT insurancebudget FROM users WHERE username = ? ''',
                                                    (GetLoginName,)).fetchone()
                insurancebudgetlabel = Label(BudgetingFrame, text=getInsuranceBudget[0])
                insurancebudgetlabel.grid(row=8, column=0)

                getOthersBudget = cursor.execute(''' SELECT othersbudget FROM users WHERE username = ? ''',
                                                 (GetLoginName,)).fetchone()
                othersbudgetlabel = Label(BudgetingFrame, text=getOthersBudget[0])
                othersbudgetlabel.grid(row=9, column=0)
            else:
                tkinter.messagebox.showerror("Error", "Enter a valid value")
        else:
            tkinter.messagebox.showerror("Error", "Enter a value")
    else:
        tkinter.messagebox.showerror("Error", "Select a category first")


selected = IntVar()

rad1 = Radiobutton(BudgetingFrame, text='Food', value=1, variable=selected, command=radButton1)

rad2 = Radiobutton(BudgetingFrame, text='Education', value=2, variable=selected, command=radButton2)

rad3 = Radiobutton(BudgetingFrame, text='Groceries', value=3, variable=selected, command=radButton3)

rad4 = Radiobutton(BudgetingFrame, text='Fuel', value=4, variable=selected, command=radButton4)

rad5 = Radiobutton(BudgetingFrame, text='Clothing', value=5, variable=selected, command=radButton5)

rad6 = Radiobutton(BudgetingFrame, text='Transport', value=6, variable=selected, command=radButton6)

rad7 = Radiobutton(BudgetingFrame, text='Utilities', value=7, variable=selected, command=radButton7)

rad8 = Radiobutton(BudgetingFrame, text='Health Care', value=8, variable=selected, command=radButton8)

rad9 = Radiobutton(BudgetingFrame, text='Insurance', value=9, variable=selected, command=radButton9)

rad10 = Radiobutton(BudgetingFrame, text='Others', value=10, variable=selected, command=radButton10)

radEntry1 = Entry(BudgetingFrame)

radEntry2 = Entry(BudgetingFrame)

radEntry3 = Entry(BudgetingFrame)

radEntry4 = Entry(BudgetingFrame)

radEntry5 = Entry(BudgetingFrame)

radEntry6 = Entry(BudgetingFrame)

radEntry7 = Entry(BudgetingFrame)

radEntry8 = Entry(BudgetingFrame)

radEntry9 = Entry(BudgetingFrame)

radEntry10 = Entry(BudgetingFrame)

btn1 = Button(BudgetingFrame, text="Enter",  fg="blue", command=budgetingButtonEnter)

rad1.grid(column=1, row=0, sticky=W)

rad2.grid(column=1, row=1, sticky=W)

rad3.grid(column=1, row=2, sticky=W)

rad4.grid(column=1, row=3, sticky=W)

rad5.grid(column=1, row=4, sticky=W)

rad6.grid(column=1, row=5, sticky=W)

rad7.grid(column=1, row=6, sticky=W)

rad8.grid(column=1, row=7, sticky=W)

rad9.grid(column=1, row=8, sticky=W)

rad10.grid(column=1, row=9, sticky=W)

radEntry1.grid_forget()

radEntry2.grid_forget()

radEntry3.grid_forget()

radEntry4.grid_forget()

radEntry5.grid_forget()

radEntry6.grid_forget()

radEntry7.grid_forget()

radEntry8.grid_forget()

radEntry9.grid_forget()

radEntry10.grid_forget()

btn1.grid(columnspan=3, row=10)

btn2 = Button(BudgetingFrame, text="Back",  fg="blue", command=backToMainUI)
btn2.grid(columnspan=3, row=11)

'''

END BUDGETING FRAME

'''
root.mainloop()

