#	main.py
#
#	This will be the main file that handles the menu and general functionality
#
#	Author: Duncan Small
import os
from time import sleep
from datetime import datetime, timedelta
import random
import psycopg2


def main():
	usr = "p320_02c"
	pw = "40lmwVV8ftOn"

	global connection

	connection = psycopg2.connect("dbname=" + usr+ " user=" + usr + " password=" + pw + " host=reddwarf.cs.rit.edu")

	print("Connected with: " + connection.dsn)
	start()
	
	connection.close()    
    
    
def start():
        while True:
                show_main_menu()
		#TODO put in try catch 
                choice = int(input("Enter option #: "))
                if choice == 0:
                        print("Thanks for using our tool.")
                        exit(0)
                elif choice == 1:
                        register_user()
                elif choice == 2:
                        user_menu()
                elif choice == 3:
                        browse_tools()
                elif choice == 4:
                        list_users()
                elif choice == 5:
                        analytics()
                else:
                    print("Please choose an option...")


def register_user():
	'''
	This function asks the user for their Username, Password, Firstname, Lastname,
		and Email to create their user profile.

	'''
	cursor = connection.cursor()

	queryUsername = 'SELECT "username" FROM "User";'
	cursor.execute(queryUsername)
	usernames = cursor.fetchall()

	isUsernameValid = False
	
	usr =""	
	while not isUsernameValid:
		usr = str(raw_input("Enter your desired username: "))
		usr = usr.strip()
		isUsernameValid = True
		if len(usr) == 0:
			isUsernameValid = False
			print("Please enter an actual username (Must contain characters)!")
			continue
		for name in usernames:
			print(name[0])
			if name[0] == usr:
				print("That name is already taken, please try again!")
				isUsernameValid = False
				break
		
	

	password = ""
	#TODO make password more secure
	while len(password) == 0:
		password = str(raw_input("Enter your password: ")).strip()


	firstName = ""
	lastName = ""
	
	while len(firstName) == 0:
		firstName = str(raw_input("Enter your first name: ")).strip()
	
	while len(lastName) == 0:
		lastName = str(raw_input("Enter your last name: ")).strip()


	queryEmail = 'SELECT "email" FROM "User";'
	cursor.execute(queryEmail)
	emails = cursor.fetchall()

	isEmailValid = False
	
	while not isEmailValid:
		userEmail = raw_input("Enter your email: ").strip()
		isEmailValid = True
		if len(userEmail) == 0: #TODO make sure its actually an email
			print("Please enter a valid email!")
			isEmailValid = False
			continue
		for email in emails:
			print(email[0])
			if userEmail == email[0]:
				isEmailValid = False
				print("That email is already taken, be sure you don't already have an account!")
				break
		
	
	now = datetime.now()
	creation_time = now.strftime("%Y/%m/%d")
	registerQuery = '''
	INSERT INTO "User"
 	("email", "username", "fname", "lname", "cdate", "ladate", "password") 
	VALUES (%s, %s, %s, %s, %s, %s, %s);
	'''
	
	cursor.execute(registerQuery, (userEmail, usr, firstName, lastName, creation_time, creation_time, password))
	connection.commit()
	check = 'SELECT "username" FROM "User" where "username"=%s;' 
	cursor.execute(check, (usr,))
	result = cursor.fetchall()
	
	i = 0
	for users in result:
		i+= 1
	
	if i == 0:
		print("There might have been an issue registering you, please try again or query the User table.")
	elif i == 1:
		print("You have been successfully registered, welcome!")
	else:
		print("THERE HAS BEEN A GRAVE ERROR PLEASE CHECK THE TABLES FOR INCONSISTENCY")
		exit(-1)
	
	cursor.close()

def show_main_menu():
        """
        Displays the main menu.
        :return: None
        """
        print(' 0. Exit')
        print(' 1. Register User')
        print(' 2. User Menu')
        print(' 3. Browse Tools')
        print(' 4. List Users')
        print(' 5. Analytics')
        print('\n')


if __name__ == "__main__":
        main()
