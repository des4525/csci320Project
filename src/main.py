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
		try:
                	choice = int(input("Enter option #: "))
                except ValueError:
			print("Please only enter numbers")
			choice = -1
			continue
		if choice == 0:
                        print("Thanks for using our tool.")
                        exit(0)
                elif choice == 1:
                        register_user()
                elif choice == 2:
                        user_menu()
                elif choice == 3:
                        browse_music()
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

def user_menu():
	show_user_menu()

	while True:
		try:
                	choice = int(input("Enter option #: "))
                except ValueError:
			print("Please only enter numbers")
			choice = -1
			continue
		if choice == 0:
                        break;
                elif choice == 1:
                        add_song()
                elif choice == 2:
                        edit_song()
                elif choice == 3:
                        show_friends()
                elif choice == 4:
                        view_playlists()
                elif choice == 5:
                        edit_playlists()
                else:
                    print("Please choose an option...")

def show_user_menu():
	print(' 0. Go back')
	print(' 1. Add Song')
	print(' 2. Edit Song')
	print(' 3. View your Friends')
	print(' 4. View your Playlists')
	print(' 5. Edit your Playlists')		
	print('\n')
	
def search_menu():
	print('How would you like to browse the music?')
	print(' 0. Go back')
	print(' 1. Song')
	print(' 2. Artist')
	print(' 3. Album')
	print(' 4. Genre')
	print('\n')


def browse_music():
	#The user must be able to search for a song via the song, artist, album, or genre

	while True:
		search_menu()
		try:
                	choice = int(input("Enter option #: "))
                except ValueError:
			print("Please only enter numbers")
			choice = -1
			continue
		if choice == 0:
			break
		elif choice == 1:
                        song_search()
                elif choice == 2:
                        artist_search()
                elif choice == 3:
                        album_search()
                elif choice == 4:
                        genre_search()
                else:
                    print("Please choose an option...")

	


def song_search():
	print("What kind of search would you like?")
	print(" 0. Exact (Song = search)")
	print(" 1. Close (Song inclused search)")
	
	while True:
		try:
                	choice = int(input("Enter option #: "))
                except ValueError:
			print("Please only enter numbers")
			choice = -1
			continue
		if choice == 0 or choice == 1:
                        break
                else:
                    print("Please choose an option...")

	search = raw_input("Enter your search parameter: ").strip()
	

	if choice:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE "Song"."name" LIKE %s
		ORDER BY "Song"."name";
		'''
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE "Song"."name" = %s
		ORDER BY "Song"."name";
		'''
	
	cursor = connection.cursor()
	cursor.execute(sql, (search,))
	result = cursor.fetchall()
	print "Song: " + result[0][0]
	print "Album: " + result[0][1]
	print "Artist: " + result[0][2]
	print "Genre: " + result[0][3]
	print '\n'	

def list_users():
	#This function should inquire the user to see if there is a specific user they are looking for
	#	Otherwise it will display every user
	pass
	
def analytics():
	#Don't know if we need this yet, but this should give certain analytics 	
	pass

def show_main_menu():
        """
        Displays the main menu.
        :return: None
        """
        print(' 0. Exit')
        print(' 1. Register User')
        print(' 2. User Menu')
        print(' 3. Browse Music')
        print(' 4. List Users')
        print('\n')


if __name__ == "__main__":
        main()
