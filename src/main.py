#This will be the main file that handles the menu and general functionality

import os
from time import sleep
from datetime import datetime, timedelta
import random
import psycopg2


def main():
        usr = "p320_02c"
        pw = "40lmwVV8ftOn"

	global connection

	connection = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + pw + " host=reddwarf.cs.rit.edu")
	print("Connected with: " + connection.dsn)
        start()
	
	connection.close()    
    
    
def start():
        while True:
                show_main_menu()
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
	cursor = connection.cursor()

	query = "SELECT username FROM user;"
	cursor.execute(query)
	usernames = cursor.fetchall()
	
	

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
