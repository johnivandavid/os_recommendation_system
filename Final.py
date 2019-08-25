import sqlite3

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from collections import defaultdict

file=pd.ExcelFile("FA18SalesData.xlsx")

#print(file.sheet_names)

sales_data = file.parse("Orders")

record = sales_data.copy()

dfs = {sheet_name: file.parse("Orders") 
          for sheet_name in file.sheet_names} 
    
#print(record)

def login():
    conn = sqlite3.connect("OS_Employee.db")
    loginTest = False
    while loginTest == False:
        cur = conn.cursor()
        try:
            print("\n========================================================================================")
            print("                       = Office Solutions Recommendation System =")
            print("========================================================================================")
            userEmail = input("Please enter Employee Email: ")
            userEmail = userEmail.strip()
            userEmail = userEmail.lower()
            
            while userEmail == "":
                userEmail = input("                  = Error: Employee Email form must not be left blank! = \n\nPlease enter Employee Email: ")
                userEmail = userEmail.strip()
                userEmail = userEmail.lower()              
                
            userPassword = input("Please enter Employee Password: ")
            userPassword = userPassword.strip()
            userPassword = userPassword.lower()
            
            while userPassword == "":
                userPassword = input("                 = Error: Employee Password form must not be left blank! = \n\nPlease enter Employee Password: ")
                userPassword = userPassword.strip()
                userPassword = userPassword.lower()
            
            global emp_name
            emp_name = ""
            sql1 = "SELECT FirstName FROM Employee WHERE (Email = '" + userEmail + "'  AND Password = '"+ userPassword + "')"
            cur.execute(sql1)
            sql1 = cur.fetchone()
            emp_name = str(sql1)[2:-3]

            
            request = "SELECT COUNT (*) FROM Employee WHERE (Email = '" + userEmail + "'  AND Password = '"+ userPassword + "')"
            cur.execute(request)
            results = cur.fetchone()
            if results[0] == 1:
                print("\n                                 = Login Successful! = ")
                loginTest = True
            else:
                print("\n                 = Login unsuccessful! Please try logging in again! =")
        except:
            print("                            = Error: Connection failed! =")
            
    conn.close()

def register():
    conn = sqlite3.connect('OS_Employee.db')
    cur=conn.cursor()
    registerTest = False
    empID_test = False
# variable to store the input data
    empID=''
    fname=''
    lname=''
    empEmail=''
    empPassword=''
    while registerTest == False:
        try:
            while empID_test == False:
                # checking for valid employee id
                while not empID:
                    print("\n========================================================================================")
                    print("                               = Register a New Employee =")
                    print("========================================================================================")
                    empID = input("Please enter the Employee ID: ")
                    # check the empID which is already exists in the table
                    if empID == '':
                        empID = print("\n                 = Error: Employee ID form must not be left blank! =\n                        = Please enter a valid Employee ID! =")
                    elif empID.isdigit() == False:
                        empID = print("\n                      = Error: Employee ID must be an integer! =\n                         = Please enter a valid Employee ID! =")                  
                    elif len(empID) != 4:
                        empID = print("\n                     = Error: Employee ID must have 4 digits! =\n                        = Please enter a valid Employee ID! =")
                    elif empID != '' and len(empID) == 4 and empID.isdigit() == True:
                        empID = int(empID)
                        # select query to check the emp ID
                        sql2 = "SELECT COUNT(*) FROM Employee WHERE EmployeeID = %d" % (empID)
                        # execute the query using sqlite connection
                        cur.execute(sql2)
                        # fetched answer is stored in the variable results
                        results = cur.fetchone()
                        #assign results to the variable rows
                        rows = results[0]
                        # If condition to check rows is equal to 1
                        if rows == 1:
                            print('\n                       = Error: Employee ID ' + str(empID) + ' already exists! =\n                         = Please enter a valid Employee ID! =')
                            empID=''
                            continue
                        else:
                            print('\n                             = Employee ID ' + str(empID) + ' is valid! =')
                            empID_test = True
                       
            # while loop to check for valid first name
            while not fname:
                fname = input("Please enter the Employee First Name: ")
                fname = fname.strip()
                fname = fname.lower()
                fname = fname.title()
                # check first name is not empty
                if fname == "":
                    print("\n                 = Error: Employee First Name form must not be left blank! =")
                    print("                         = Please enter a valid Employee First Name! =")
                else:
                # convert first name into uppercase
                    fname = fname.strip()
                    fname = fname.lower()
                    fname=fname.title()
                
            # while loop to check for valid last name
            while not lname:
                lname = input("Please enter the Employee Last Name: ")
                lname = lname.strip()
                lname = lname.lower()
                lname = lname.title()
                # check first name is not empty
                if lname == "":
                    print("\n                 = Error: Employee Last Name form must not be left blank! =")
                    print("                         = Please enter a valid Employee Last Name! =")
                else:
                # convert first name into uppercase
                    lname = lname.strip()
                    lname = lname.lower()
                    lname = lname.title()
                    
            # while loop to check for valid email
            while not empEmail:
                empEmail = input("Please enter the Employee Email: ")
                empEmail = empEmail.strip()
                empEmail = empEmail.lower()
            # check email is not empty
                if empEmail == "":
                    print("\n                  - Error: Employee Email form must not be left blank! -")
                    print("                         - Please enter a valid Employee Email! -")
                else:
                    empEmail = empEmail.strip()
                    empEmail = empEmail.lower()
                    
            while not empPassword:         
                empPassword = input("Please enter the Employee Password: ")
                empPassword = empPassword.strip()
                empPassword = empPassword.lower()
            # check email is not empty
                if empPassword == "":
                    print("\n                = Error: Employee Password form must not be left blank! =")
                    print("                        = Please enter a valid Employee Password! =")
                else:
                    empPassword = empPassword.strip()
                    empPassword = empPassword.lower()
                        
        # insert query to insert the employee data into table
            sql3="Insert into employee values( %d,'%s','%s','%s','%s')" %  (empID,fname,lname,empEmail,empPassword)
            # execute the insert query
            cur.execute(sql3)
            conn.commit()
            # select query to retrieve the employee data 
            sql4="select * from employee where employeeid= %d" % empID
            # execute the above query
            cur.execute(sql4)
            # fetch the data and assigned to the variable results
            results = cur.fetchall()
            print("\n========================================================================================\n")
            print("     = The following data has been successfully entered into the Employee Database =")
            print("\nEmployee ID: " + str(empID) + "\nEmployee First Name: " + str(fname) + "\nEmployee Last Name: " + str(lname))
            print("Employee Email: " + str(empEmail) + "\nEmployee Password: " + str(empPassword))
            print("\n========================================================================================")
            registerTest = True
    # if connection not established
        except:
            print("                            = Error: Connection failed! =")
        conn.close()
        exit

def insight_1():
    
    insight_1_test = True
    
    while insight_1_test == True:
        
        region_option_test = True
        
        while region_option_test == True:
            
            print("\n========================================================================================")
            print("                   = Profit Calculations of Product Category by Region =")
            print("========================================================================================")
            
            print("\n1. West")
            
            print("\n2. Central")
            
            print("\n3. South")
            
            print("\n4. East")
            
            print("\n5. Total Profit by Region")
            
            print("\n6. Return to Main Menu")
        
            region_option = input("Please enter a number to select a region that you want to view: ")
            
            if region_option == "1":

                west_option_test = True
            
                while west_option_test == True:
                    
                    print("\n========================================================================================")
                    print("              = Profit Calculations of Product Category in the West Region =")
                    print("========================================================================================")
            
                    print("\n1. West/Office Furniture")
            
                    print("\n2. West/Office Supplies")
            
                    print("\n3. West/Technology")
                    
                    print("\n4. Return to Region Menu")
                    
                    west_option=input("Please enter a number to select the product that you want to view: ")
                    
                    if west_option == "1":
            
                        West=record.loc[record['Region'] == 'West'] #Selecting Region
            
                        Furniture=West.loc[West['Category'] == 'Furniture'] #Selecting
            
                        profit=sorted(Furniture["Profit"])
                        
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=====================Profit Calculations of West/Office Furniture======================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('West/Office Furniture')
                        plt.show()
                        
                    elif west_option == "2":
            
                        West=record.loc[record['Region'] == 'West']
            
                        Supplies=West.loc[West['Category'] == 'Office Supplies']
            
                        profit=sorted(Supplies["Profit"])                        
            
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n======================Profit Calculations of West/Office Supplies======================")
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('West/Office Supplies')
                        plt.show()
    
                    elif west_option == "3":
            
                        West=record.loc[record['Region'] == 'West']
            
                        Technology=West.loc[West['Category'] == 'Technology']
            
                        profit=sorted(Technology["Profit"])
                        
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=========================Profit Calculations of West/Technology=========================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('West/Technology')
                        plt.show()
                        
                    elif west_option == "4":
                        
                        west_option_test = False
                        
                    elif west_option.isdigit() == False or west_option == "" or float(west_option) > 4:
    
                        print("\n                                        = Error =")
                        print(" = You have entered numbers that are greater than 4, symbols, letters, or blank space! =")
                        print("      = Please enter a valid task number that you want to perform and press enter. =\n")

            elif region_option == "2":
                
                central_option_test = True
                
                while central_option_test == True:

                    print("\n========================================================================================")
                    print("             = Profit Calculations of Product Category in the Central Region =")
                    print("========================================================================================")
        
                    print("\n1. Central/Office Furniture")
        
                    print("\n2. Central/Office Supplies")
        
                    print("\n3. Central/Technology")
                    
                    print("\n4. Return to Region Menu")
 
                    central_option=input("Please enter a number to select the product that you want to view: ")
                    
                    if central_option == "1":
    
                        Central=record.loc[record['Region'] == 'Central']
    
                        Furniture=Central.loc[Central['Category'] == 'Furniture']
    
                        profit=sorted(Furniture["Profit"])
                        
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n====================Profit Calculations of Central/Office Furniture====================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('Central/Office Furniture')
                        plt.show()
                    
                    elif central_option == "2":
    
                        Central=record.loc[record['Region'] == 'Central']
    
                        Supplies=Central.loc[Central['Category'] == 'Office Supplies']
    
                        profit=sorted(Supplies["Profit"])
                        
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=====================Profit Calculations of Central/Office Supplies=====================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('Central/Office Supplies')
                        plt.show()
    
                    elif central_option == "3":
    
                        Central=record.loc[record['Region'] == 'Central']
    
                        Technology=Central.loc[Central['Category'] == 'Technology']
    
                        profit=sorted(Technology["Profit"])
            
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=======================Profit Calculations of Central/Technology=======================")
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('Central/Technology')
                        plt.show()
                    
                    elif central_option == "4":
                        
                        central_option_test = False
    
                    elif central_option.isdigit() == False or central_option == "" or float(central_option) > 4:
    
                        print("\n                                        = Error =")
                        print(" = You have entered numbers that are greater than 4, symbols, letters, or blank space! =")
                        print("      = Please enter a valid task number that you want to perform and press enter. =\n")

            elif region_option == "3":
                
                south_option_test = True
                
                while south_option_test == True:
    
                    print("\n========================================================================================")
                    print("              = Profit Calculations of Product Category in the South Region =")
                    print("========================================================================================")
        
                    print("\n1. South/Office Furniture")
                    
                    print("\n2. South/Office Supplies")
        
                    print("\n3. South/Technology")
                    
                    print("\n4. Return to Region Menu")
            
                    south_option=input("Please enter a number to select the product that you want to view: ")
                    
                    if south_option == "1":
    
                        South=record.loc[record['Region'] == 'South']
    
                        Furniture=South.loc[South['Category'] == 'Furniture']
    
                        profit=sorted(Furniture["Profit"])
    
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=====================Profit Calculations of South/Office Furniture=====================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('South/Office Furniture')
                        plt.show()
    
                    elif south_option == "2":
    
                        South=record.loc[record['Region'] == 'South']
    
                        Supplies=South.loc[South['Category'] == 'Office Supplies']
    
                        profit=sorted(Supplies["Profit"])
            
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n======================Profit Calculations of South/Office Supplies======================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('South/Office Supplies')
                        plt.show()
    
                    elif south_option == "3":
    
                        South=record.loc[record['Region'] == 'South']
    
                        Technology=South.loc[South['Category'] == 'Technology']
    
                        profit=sorted(Technology["Profit"])
            
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n========================Profit Calculations of South/Technology========================")                        
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('South/Technology')
                        plt.show()
                                          
                    elif south_option == "4":
                        
                        south_option_test = False
    
                    elif south_option.isdigit() == False or south_option == "" or float(south_option) > 4:
    
                        print("\n                                        = Error =")
                        print(" = You have entered numbers that are greater than 4, symbols, letters, or blank space! =")
                        print("      = Please enter a valid task number that you want to perform and press enter. =\n")
                 
            elif region_option == "4":
                
                east_option_test = True     
                               
                while east_option_test == True:

                    print("\n========================================================================================")
                    print("               = Profit Calculations of Product Category in the East Region =")
                    print("========================================================================================")
    
                    print("\n1. East/Office Furniture")
    
                    print("\n2. East/Office Supplies")
    
                    print("\n3. East/Technology")
                    
                    print("\n4. Return to Region Menu")
  
                    east_option=input("Please enter a number to select the product that you want to view: ")
    
                    if east_option == "1":
    
                        East=record.loc[record['Region'] == 'East']
    
                        Furniture=East.loc[East['Category'] == 'Furniture']
                            
                        profit=sorted(Furniture["Profit"])
                    
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n======================Profit Calculations of East/Office Furniture======================")
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('East/Office Furniture')
                        plt.show()
    
                    elif east_option == "2":
    
                        East=record.loc[record['Region'] == 'East']
    
                        Supplies=East.loc[East['Category'] == 'Office Supplies']
    
                        profit=sorted(Supplies["Profit"])
            
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n======================Profit Calculations of East/Office Supplies======================")
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('East/Office Supplies')
                        plt.show()
                
                    elif east_option == "3":
    
                        East=record.loc[record['Region'] == 'East']
                        
                        Technology=East.loc[East['Category'] == 'Technology']
                        
                        profit=sorted(Technology["Profit"])
                        
                        max_p = max(profit)
                        
                        min_p = min(profit)
                        
                        diff_p = max_p - abs(min_p)
                        
                        tot_p = sum(profit)
                        
                        print("\n=========================Profit Calculations of East/Technology=========================")
            
                        print("\nThe max profit: $", round(max_p, 2))
            
                        print("\nThe min profit: $", round(min_p, 2))
            
                        print("\nThe max/min profit difference: $", round(diff_p, 2))
                        
                        print("\nThe total profit: $", round(tot_p, 2))
                        
                        x = ('Total', 'Difference', 'Min', 'Max')
                        y = [tot_p, diff_p, min_p, max_p]
                        y_pos = np.arange(len(x))

                        plt.barh(y_pos, y, align = 'center')
                        plt.yticks(y_pos, x)
                        plt.xlabel('Value')
                        plt.ylabel('Profit')
                        plt.title('East/Technology')
                        plt.show()
                    
                    elif east_option == "4":
                        
                        east_option_test = False
                        
                    elif east_option.isdigit() == False or east_option == "" or float(east_option) > 4:
    
                        print("\n                                        = Error =")
                        print(" = You have entered numbers that are greater than 4, symbols, letters, or blank space! =")
                        print("      = Please enter a valid task number that you want to perform and press enter. =\n")

            elif region_option == "5":
                
                df = dfs['Orders']
                profits_data = np.array(list(df['Profit']))
                categories_data = np.array(list(df['Category']))
                sub_categories_data = np.array(list(df['Sub-Category']))
                regions_data = np.array(list(df['Region']))
                sorted_indices = np.argsort(profits_data)
                
                profits_data = profits_data[sorted_indices]
                categories_data = categories_data[sorted_indices]
                sub_categories_data = sub_categories_data[sorted_indices]
                regions_data = regions_data[sorted_indices]
                
                print("\n========================================================================================")
                print("             = Profit Calculations of Product Category in All Regions =")
                print("========================================================================================")
                
                regions_profits_dict = defaultdict(float)

                for i in range (profits_data.shape[0]):
                    regions_profits_dict[regions_data[i]] += profits_data[i] 
                    
                
                objects = tuple(regions_profits_dict.keys())
                y_pos = np.arange(len(objects))
                performance = list(regions_profits_dict.values())
                performance_0 = round(performance[0], 2)
                performance_1 = round(performance[1], 2)
                performance_2 = round(performance[2], 2)
                performance_3 = round(performance[3], 2)
                print("\nEast: $"+ str(performance_0))
                print("South: $"+ str(performance_1))
                print("Central: $"+ str(performance_2))
                print("West: $"+ str(performance_3))
                colors = ['green', 'yellow', 'red', 'blue', 'lightcoral'] 
                plt.bar(y_pos, performance, align='center', alpha=0.75, color=colors)
                plt.xticks(y_pos, objects)
                plt.xlabel('Region')
                plt.ylabel('Profit')
                plt.title('Profit by Region')
                plt.show()

                
            elif region_option == "6":  
                
                region_option_test = False
                insight_1_test = False
            
            elif region_option.isdigit() == False or region_option == "" or float(region_option) > 6:
    
                print("\n                                        = Error =")
                print(" = You have entered numbers that are greater than 6, symbols, letters, or blank space! =")
                print("      = Please enter a valid task number that you want to perform and press enter. =\n")
                
def insight_2():
    insight_2_test = True
    while insight_2_test == True:
        df = dfs['Orders']
        l = list(df.columns)
        l[6] = l[2]
        l[2] = 'Customer Name'
        df = df[l]
        
        ntop = 10
        return_counts = np.unique(df['Customer ID'], return_counts=True)
        
        sort_indices = np.argsort(return_counts[1])
        arr_counts = return_counts[1][sort_indices]
        arr_ids = return_counts[0][sort_indices]
        top_customers = []
        for id_ in arr_ids[-ntop:]:
                val = list(df['Customer Name'][df['Customer ID'] == id_])
                top_customers.append(val[0])
         
        print("\n========================================================================================")
        print("                       = Top Customers Eligible for Loyalty Program = ")
        print("========================================================================================")
        print ("\nTop Customers Names:")
        print (top_customers[::-1])
        
        
        region_tuple = np.unique(df['Region'], return_counts=True)
        pie_sources =df.groupby('Region').agg('count')
        
        source_labels = list(region_tuple[0])
        source_counts = list(region_tuple[1])
        labels = list(region_tuple[0]) 
        sizes = list(region_tuple[1])
        #print (len(labels), len(sizes)) 
        explode = (0, 0, 0, 0.2)   
        plt.pie(sizes,              
                explode=explode,    
                labels=labels,      
                autopct='%1.1f%%',  
                shadow=True,
                startangle=70
                )
        
        plt.axis('equal')
        plt.title("Top Customers By Region")
        plt.show()
        
        top_return_test = True
        while top_return_test == True:
            
            print("\n========================================================================================")
            print("                     = Would you like to return to the Main Menu? = ")
            print("========================================================================================")
            print("\n1. Return to Main Menu")
            top_return = input("Please type the number corresponding to the task you want to perform and press enter: ")
            
            if top_return == "1":
               top_return_test = False 
               insight_2_test = False
           
            elif top_return.isdigit() == False or top_return == "" or float(top_return) > 1:
        
                    print("\n                                        = Error =")
                    print(" = You have entered numbers that are greater than 1, symbols, letters, or blank space! =")
                    print("      = Please enter a valid task number that you want to perform and press enter. =\n")

def insight_3():
    df = dfs['Orders']
    
    profits_data = np.array(list(df['Profit']))
    categories_data = np.array(list(df['Category']))
    sub_categories_data = np.array(list(df['Sub-Category']))
    regions_data = np.array(list(df['Region']))
    sorted_indices = np.argsort(profits_data)
    
    profits_data = profits_data[sorted_indices]
    categories_data = categories_data[sorted_indices]
    sub_categories_data = sub_categories_data[sorted_indices]
    regions_data = regions_data[sorted_indices]
    
    insight_3_test = True
    while insight_3_test == True:
        
        print("\n========================================================================================")
        print("                        = Total Profit by Category/Sub-Category =")
        print("========================================================================================")
        
        print("\n1. View Total Profit by Category")
                
        print("\n2. View Total Profit by Sub-Category")
                
        print("\n3. Return to Main Menu")
        
        profit_option = input("Please type the number corresponding to the task you want to perform and press enter: ")
        
        if profit_option == "1":
            profit_cat_test = True
            while profit_cat_test == True:
                print("\n========================================================================================")
                print("                              = Total Profit by Category =")
                print("========================================================================================")
                cats_profits_dict = defaultdict(float)
                
                for i in range (profits_data.shape[0]):
                    cats_profits_dict[categories_data[i]] += profits_data[i] 
                
                
                objects = tuple(cats_profits_dict.keys())
                y_pos = np.arange(len(objects))
                performance = list(cats_profits_dict.values())
                performance_0 = round(performance[0], 2)
                performance_1 = round(performance[1], 2)
                performance_2 = round(performance[2], 2)
                print("\nTechnology: $"+ str(performance_0))
                print("Office Supplies: $"+ str(performance_1))
                print("Office Furniture: $"+ str(performance_2))
                colors = ['green', 'yellow', 'red', 'blue', 'lightcoral'] 
                plt.bar(y_pos, performance, align='center', alpha=0.75, color=colors)
                plt.xticks(y_pos, objects)
                plt.ylabel('Profit')
                plt.title('Total Profit by Category')
                
                plt.show()
                
                cat_return_test = True
                while cat_return_test == True:
                    
                    print("\n========================================================================================")
                    print("               = Would you like to return to the Category/Sub-Category Menu? = ")
                    print("========================================================================================")
                    print("\n1. Return to Category/Sub-Category Menu")
                    cat_return = input("Please type the number corresponding to the task you want to perform and press enter: ")
                    
                    if cat_return == "1":
                       cat_return_test = False 
                       profit_cat_test = False
                   
                    elif cat_return.isdigit() == False or cat_return == "" or float(cat_return) > 1:
        
                            print("\n                                        = Error =")
                            print(" = You have entered numbers that are greater than 1, symbols, letters, or blank space! =")
                            print("      = Please enter a valid task number that you want to perform and press enter. =\n")
            
        elif profit_option == "2":
            profit_sub_test = True
            while profit_sub_test == True:
                subcats_profits_dict = defaultdict(float)
                
                for i in range (profits_data.shape[0]):
                    subcats_profits_dict[sub_categories_data[i]] += profits_data[i] 
                
                
                objects = tuple(subcats_profits_dict.keys())
                y_pos = np.arange(len(objects))
                performance = list(subcats_profits_dict.values())
                performance_0 = round(performance[0], 2)
                performance_1 = round(performance[1], 2)
                performance_2 = round(performance[2], 2)
                performance_3 = round(performance[3], 2)
                performance_4 = round(performance[4], 2)
                performance_5 = round(performance[5], 2)
                performance_6 = round(performance[6], 2)
                performance_7 = round(performance[7], 2)
                performance_8 = round(performance[8], 2)
                performance_9 = round(performance[9], 2)
                performance_10 = round(performance[10], 2)
                performance_11 = round(performance[11], 2)
                performance_12 = round(performance[12], 2)
                performance_13 = round(performance[13], 2)
                performance_14 = round(performance[14], 2)
                performance_15 = round(performance[15], 2)
                performance_16 = round(performance[16], 2)
                print("\n========================================================================================")
                print("                            = Total Profit by Sub-Category =")
                print("========================================================================================")
                print("\n                                      = Legend =")
                print("                                 = Technology - Green =")
                print("                               = Office Supplies - Blue =")
                print("                               = Office Furniture - Red =")
                colors = ['green', 'lightskyblue', 'red', 'red','lightskyblue', 'lightskyblue', 'red', 'red', 'green', 'lightskyblue', 'green', 'lightskyblue', 'lightskyblue', 'lightskyblue', 'lightskyblue', 'lightskyblue', 'green' ]
                plt.barh(y_pos, performance, align='center', alpha=0.95, color=colors)
                plt.yticks(y_pos, objects)
                plt.xlabel('Profit')
                plt.title('Profit by Sub-Category')
                plt.show()
                print("Copiers: $" + str(performance_16)) 
                print("Paper: $" + str(performance_15)) 
                print("Labels: $" + str(performance_14)) 
                print("Envelopes: $" + str(performance_13))
                print("Art: $" + str(performance_12))
                print("Fasteners: $" + str(performance_11))
                print("Accessories: $" + str(performance_10))
                print("Storage: $" + str(performance_9)) 
                print("Phones: $" + str(performance_8)) 
                print("Furnishings: $" + str(performance_7))
                print("Chairs: $" + str(performance_6))
                print("Supplies: $" + str(performance_5))
                print("Appliances: $" + str(performance_4))
                print("Bookcases: $" + str(performance_3))
                print("Tables: $" + str(performance_2))
                print("Binders: $" + str(performance_1))
                print("Machines: $" + str(performance_0))
                
                cat_return_test = True
                while cat_return_test == True:
                    
                    print("\n========================================================================================")
                    print("               = Would you like to return to the Category/Sub-Category Menu? = ")
                    print("========================================================================================")
                    print("\n1. Return to Category/Sub-Category Menu")
                    cat_return = input("Please type the number corresponding to the task you want to perform and press enter: ")
                    
                    if cat_return == "1":
                       cat_return_test = False 
                       profit_sub_test = False
                   
                    elif cat_return.isdigit() == False or cat_return == "" or float(cat_return) > 1:
        
                            print("\n                                        = Error =")
                            print(" = You have entered numbers that are greater than 1, symbols, letters, or blank space! =")
                            print("      = Please enter a valid task number that you want to perform and press enter. =\n")
        
        elif profit_option == "3":
            
            profit_cat_test = False
            insight_3_test = False
            
        elif profit_option.isdigit() == False or profit_option == "" or float(profit_option) > 3:
    
            print("\n                                        = Error =")
            print(" = You have entered numbers that are greater than 3, symbols, letters, or blank space! =")
            print("      = Please enter a valid task number that you want to perform and press enter. =\n")

def insight_4():
    insight_4_test = True
    while insight_4_test == True:
        print("\n========================================================================================")
        print("                        = Top Performing States by Sales Quantity =")
        print("========================================================================================")
        
        print("\n1. Test Top Performing States")
            
        print("\n2. Return to Main Menu")
        
        state_option = input("Please type the number corresponding to the task you want to perform and press enter: ")
        
        if state_option == "1":
            top_number_test = True
            while top_number_test == True:
                top_number = input("Please type the number of states that you would like to view and press enter: ")
                if top_number.isdigit() == True:
                    state_quant_cols = sales_data[["State","Quantity"]]
                    state_purchases = state_quant_cols.groupby(by="State").sum().sort_values(by="Quantity", ascending=False)
                    print("\n=======================Top " + top_number + " Performing States by Sales Quantity=======================\n")
                    print(state_purchases.head(int(top_number)))
                    top_number_test = False
                    
                elif top_number.isdigit() == False or top_number == "":
    
                    print("\n                                        = Error =")
                    print("              = You have either entered symbols, letters, or blank space! =")
                    print("                       = Please enter a number and press enter. =\n")
        
        elif state_option == "2":
            top_number_test = False
            insight_4_test = False
        
        elif state_option.isdigit() == False or state_option == "" or float(state_option) > 2:

            print("\n                                        = Error =")
            print(" = You have entered numbers that are greater than 2, symbols, letters, or blank space! =")
            print("      = Please enter a valid task number that you want to perform and press enter. =\n")

if __name__ == "__main__":
   
    login_test = True
    
    while login_test == True:
        
        login()
            
        main_menu_test = True
        
        while main_menu_test == True:
        
            print("\n========================================================================================")
            print("\n              = Welcome to the Office Solutions Recommendation System, " + emp_name + "! =")
            print("                         = What task would you like to perform? =\n")
            print("========================================================================================\n")
            
            print("\n1. Register new Employee")
                
            print("\n2. View Profit Calculations of Product Category by Region")
            
            print("\n3. View Top Customers Eligible for Loyalty Program")
            
            print("\n4. View Total Profit by Category/Sub-Category")
            
            print("\n5. View Top Performing States by Sales Quantity")
            
            print("\n6. Logout")
            
            user_choice = input("Please type the number corresponding to the task you want to perform and press enter: ")
        
            if user_choice == "1":
                
                register()
                
                register_test = True
                
                while register_test == True:
                
                    print("\n             = Would you like to login using the new employee credentials? =")
                    print("\n1. Yes, login using the new employee credentials")
                    print("\n2. No, return to Main Menu")
                    
                    register_choice = input("Please type the number corresponding to the task you want to perform and press enter: ")
                
                    if register_choice == "1":
                        register_test = False
                        main_menu_test = False
                       
                   
                    elif register_choice == "2":
                        register_test = False
                    
                    elif register_choice.isdigit() == False or register_choice == "" or float(register_choice) > 2:
                        print("\n========================================================================================")
                        print("\n                                        = Error =")
                        print(" = You have entered numbers that are greater than 2, symbols, letters, or blank space! =")
                        print("      = Please enter a valid task number that you want to perform and press enter. =")
                        print("========================================================================================")
                        
            elif user_choice == "2":
                
                insight_1()
            
            elif user_choice == "3":
                
                insight_2()
            
            elif user_choice == "4":
                
                insight_3()
            
            elif user_choice == "5":
                
                insight_4()
            
            elif user_choice == "6":
                print("\n========================================================================================")
                print("            = Thank you for using the Office Solutions Recommendation System! =")
                print("                                      = Good-bye! = ")
                print("========================================================================================\n")
                main_menu_test = False
                login_test = False
                break
            
            elif user_choice.isdigit() == False or user_choice == "" or float(user_choice) > 5:
        
                print("\n                                        = Error =")
                print(" = You have entered numbers that are greater than 6, symbols, letters, or blank space! =")
                print("      = Please enter a valid task number that you want to perform and press enter. =\n") 
         
    
    
 
     


