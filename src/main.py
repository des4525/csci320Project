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

	login()	

	start()
	
	connection.close()    
    
#----------MENUS----------

def show_main_menu():
        print(' 0. Exit')
        print(' 1. Register User')
        print(' 2. User Menu')
        print(' 3. Search Music')
        print(' 4. List Users')
        print('\n')
		
def show_user_menu():
	print(' 0. Go back')
	print(' 1. Play whole Playlist')
	print(' 2. Play Song')
	print(' 3. Friends Menu')
	print(' 4. Playlist Menu')		
	print('\n')
	
def search_menu():
	print('How would you like to search the music?')
	print(' 0. Go back')
	print(' 1. Song')
	print(' 2. Artist')
	print(' 3. Album')
	print(' 4. Genre')
	print('\n')

def friend_menu():
	print(' 0. Go back')
	print(' 1. View Friends')
	print(' 2. Find Friend')
	print(' 3. View Followers')		
	print('\n')
	
def login():
	print ("Do you have an account with our application?")
	print " 0. No I need to register"
	print " 1. Yes I need to login"
	
	choice = -1
	while choice == -1:
		try:
			choice = int(input("Enter option #: "))
		except ValueError:
			print("Please only enter numbers")
			choice = -1
			
	if choice == 0:
		register_user()
	else:
		usr = ""
		password = ""
		while  len(usr) == 0 or len(password) == 0:
			usr = raw_input("Enter your username: ").strip()
			password = raw_input("Enter your password: ").strip()
		sql = '''
		SELECT "User"."username", "User"."password", "User"."email", "User"."fname", "User"."lname"
		FROM "User";
		'''
		global currentEmail
		global currentUsername
	
		cursor = connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		loginSuccess = False

		if result != []:
			for entry in result:
				if entry[0] == usr and entry[1] == password:
					print "Welcome " + entry[3] + " " + entry[4]
					loginSuccess = True
					currentEmail = entry[2]
					currentUsername = entry[0]
					break
			if not loginSuccess:
				print("We couldn't find your account, please restart the program and try again.")
		else:
			print("Ther were no accounts retrieved, please register")
		
		if loginSuccess:
			sql = '''
			UPDATE "User"
			SET "ladate" = %s
			WHERE "email" = %s;
			'''
			now = datetime.now()
			ladate = now.strftime("%Y/%m/%d")
			cursor.execute(sql, (ladate, currentEmail))
		else:
			exit(-1)
			
def start():
        while True:
                show_main_menu()
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
                        play_playlist()
                elif choice == 2:
                        play_song()
                elif choice == 3:
                        friend_menu()
                elif choice == 4:
                        playlist_menu()
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
	login()
	cursor.close()



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

	


def play_song():
    def play_song():
        song_id = raw_input("Please type the song id: ")

        get_song_sql = '''
	    SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name"
	    FROM (((((("Song"
	    INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
	    INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
	    INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
	    INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
	    INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
	    INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
	    WHERE "Song"."songid" = %s
	    ORDER BY "Song"."name";
	    '''
        cursor = connection.cursor()
        cursor.execute(get_song_sql, (song_id,))
        result = cursor.fetchall()
        if result:
            song = result[0]
            print("Playing " + song[0] + " by " + song[1] + "\n")

        else:
            print("Sorry, there's no song in the database with that id.\n")

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
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Song"."name") LIKE LOWER(%s)
		ORDER BY "Song"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Song"."name") = LOWER(%s)
		ORDER BY "Song"."name";
		'''
	cursor = connection.cursor()
	cursor.execute(sql, (search,))
	result = cursor.fetchall()
	
	
	if result != []:
		for entry in result:
			print "Song: " + entry[0]
			print "Album: " + entry[1]
			print "Artist: " + entry[2]
			print "Genre: " + entry[3]
			print "Length: " + str(entry[4]) + " Seconds"
			print "Listen Count: " + str(entry[5]) + " Play(s)"
			print '\n'	
	else:
		print "Sorry but there were no records that matched your search"

	cursor.close()

def artist_search():
	print("What kind of search would you like?")
	print(" 0. Exact (Artist = search)")
	print(" 1. Close (Artist inclused search)")
	
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
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Artist"."name") LIKE LOWER(%s)
		ORDER BY "Artist"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Artist"."name") = LOWER(%s)
		ORDER BY "Artist"."name";
		'''
	cursor = connection.cursor()
	cursor.execute(sql, (search,))
	result = cursor.fetchall()
	
	
	if result != []:
		for entry in result:
			print "Song: " + entry[0]
			print "Album: " + entry[1]
			print "Artist: " + entry[2]
			print "Genre: " + entry[3]
			print "Length: " + str(entry[4]) + " Seconds"
			print "Listen Count: " + str(entry[5]) + " Play(s)"
			print '\n'	
	else:
		print "Sorry but there were no records that matched your search"

	cursor.close()
	
	
	
def album_search():
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
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Album"."name") LIKE LOWER(%s)
		ORDER BY "Album"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Album"."name") = LOWER(%s)
		ORDER BY "Album"."name";
		'''
	cursor = connection.cursor()
	cursor.execute(sql, (search,))
	result = cursor.fetchall()
	
	
	if result != []:
		for entry in result:
			print "Song: " + entry[0]
			print "Album: " + entry[1]
			print "Artist: " + entry[2]
			print "Genre: " + entry[3]
			print "Length: " + str(entry[4]) + " Seconds"
			print "Listen Count: " + str(entry[5]) + " Play(s)"
			print '\n'	
	else:
		print "Sorry but there were no records that matched your search"

	cursor.close()
	

def genre_search():
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
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Genre"."name") LIKE LOWER(%s)
		ORDER BY "Genre"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."name", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."name" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Genre"."name") = LOWER(%s)
		ORDER BY "Genre"."name";
		'''
	cursor = connection.cursor()
	cursor.execute(sql, (search,))
	result = cursor.fetchall()
	
	
	if result != []:
		for entry in result:
			print "Song: " + entry[0]
			print "Album: " + entry[1]
			print "Artist: " + entry[2]
			print "Genre: " + entry[3]
			print "Length: " + str(entry[4]) + " Seconds"
			print "Listen Count: " + str(entry[5]) + " Play(s)"
			print '\n'	
	else:
		print "Sorry but there were no records that matched your search"

	cursor.close()


if __name__ == "__main__":
        main()
