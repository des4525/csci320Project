#	main.py
#
#	This will be the main file that handles the menu and general functionality
#
#	Author: Duncan Small
import operator
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
        print(' 1. Register User') # works
        print(' 2. Play Menu')
        print(' 3. Search Music') # works
	print(' 4. Follow Menu')
	print(' 5. Playlist Menu')
        print('\n')
		
def show_play_menu():
	print(' 0. Go back')
	print(' 1. Play Whole Playlist')
	print(' 2. Play Song')		
	print('\n')
	
def show_search_menu():
	print('How would you like to search the music?')
	print(' 0. Go Back')
	print(' 1. Song')
	print(' 2. Artist')
	print(' 3. Album')
	print(' 4. Genre')
	print('\n')

def show_follower_menu():
	print(' 0. Go Back')
	print(' 1. View Who is Following You')
	print(' 2. View Who You are Following')
	print(' 3. Find User')
	print(' 4. Unfollow User')
	print('\n')
	
def show_playlist_menu():
	print(' 0. Go back')
	print(' 1. View My Playlists')
	print(' 2. Edit Playlist Name')
	print(' 3. Add To Playlist')
	print(' 4. Remove From Playlist')
	print(' 5. Delete Playlist')
	print(' 6. Create Playlist')
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
		connection.commit()
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
			connection.commit()
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
                        play_menu()
                elif choice == 3:
                        search_music()
                elif choice == 4:
                        follower_menu()
                elif choice == 5:
                        playlist_menu()
                else:
                    print("Please choose an option...")

def play_menu():

	while True:
		show_play_menu()
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
                else:
                    print("Please choose an option...")

def playlist_menu():
	while True:
                show_playlist_menu()
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
                        view_playlists()
                elif choice == 2:
                        edit_playlist_name()
                elif choice == 3:
                        add_to_playlist()
                elif choice == 4:
                        remove_from_playlist()
                elif choice == 5:
                        delete_playlist()
		elif choice == 6:
			create_playlist()
                else:
                    print("Please choose an option...")

def play_playlist():
	cursor = connection.cursor()
	playlist_name = raw_input("Please type the playlist name: ").strip()
	get_playlist_sql = '''
	SELECT "Playlist"."playlistid", "Playlist"."playlistname", "Playlist"."numsongs", "Playlist"."duration", "Playlist"."email"
	FROM "Playlist"	
	WHERE LOWER("Playlist"."playlistname") = LOWER(%s)
	ORDER BY "Playlist"."playlistname";
	'''
	cursor.execute(get_playlist_sql, (playlist_name,))
	result = cursor.fetchall()
	if result == []:
		print("Sorry, there's no playlist in the database with that name.\n")
		return
	elif len(result) == 1:
		playlist = result[0]
	else:
		print("There are multiple playlists with that name. Which would you like to listen to?")
		i = 1
		for entry in result:
			print(str(i) + ".      Name: " + entry[1] + ", Owner: " + entry[4])
			i = i + 1
		print("")
		playlist = result[int(raw_input("enter the number of the song you want: ")) - 1]

	print("Playing " + playlist[1] + " by " + playlist[4] + "; Number of songs: " + str(playlist[2])+ ", Duration: " + str(playlist[3]))

	get_songs_sql = '''
	SELECT "PlaylistContains"."songid", "PlaylistContains"."song_index"
	FROM "PlaylistContains"	
	WHERE "PlaylistContains"."playlistid" = %s
	ORDER BY "PlaylistContains"."song_index";
	'''
	cursor.execute(get_songs_sql, (playlist[0],))
	result = cursor.fetchall()

	for entry in result:
		song_id = entry[0]
		get_song_sql = '''
		SELECT "Song"."name", "Artist"."aname"
		FROM (((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		WHERE "Song"."songid" = %s
		'''
		cursor.execute(get_song_sql, (song_id,))
		result = cursor.fetchall()
		if not result:
			print("Error: no result found for the song_id found in the playlist")
			cursor.close()
			return

		song = result[0]
		print(str(entry[1]) + ".     " + "Playing " + song[0] + " by " + song[1])

		add_to_history_sql = '''
		INSERT INTO "PlayHistory" (email, songid, listen_date)
		VALUES (%s, %s, %s);
		'''
		cursor.execute(add_to_history_sql, (currentEmail, song_id, datetime.now().strftime("%Y/%m/%d"),))
		connection.commit()

		update_listens_sql = '''
		UPDATE "Song" SET listens = listens + 1
		WHERE songid = %s;
		'''
		cursor.execute(update_listens_sql, (song_id,))
	print("")
	cursor.close()

def view_playlists():
	sql = '''
	SELECT "playlistname", "email"
	FROM "Playlist"
	WHERE "email" = %s;
	'''
	cursor = connection.cursor()
	cursor.execute(sql, (currentEmail,))
	connection.commit()
	
	result = cursor.fetchall()
	for entry in result:
		print("Playlist: " + entry[0])
		print("Created by: " + entry[1])

def edit_playlist_name():
	playlistName = ""
	while len(playlistName) == 0:
		playlistName = raw_input("Which playlist would you like to alter?").strip()
	
	
	newPlaylistName = ""
	while len(newPlaylistName) == 0:
		newPlaylistName = raw_input("What would you like the new name to be?").strip()

	sql = '''
	UPDATE "Playlist"
	SET "playlistname" = %s
	WHERE "playlistname" = %s AND "email" = %s;
	'''
	
	cursor = connection.cursor()
	cursor.execute(sql, (newPlaylistName, playlistName, currentEmail))
	connection.commit()
	
	print("All done!")

def add_to_playlist():
	playlistName = ""
	while len(playlistName) == 0:
		playlistName = raw_input("Which playlist would you like to add a song to?").strip()

	songName = ""
	while len(songName) == 0:
		songName = raw_input("Which song would you like to add?").strip()
	
	artistName = ""	
	while len(artistName) == 0:
		artistName = raw_input("Who is the artist who released that song?").strip()
	
	sql = '''
	SELECT "Song"."name", "Artist"."aname", "Song"."songid", "Song"."length" 
		FROM (((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		WHERE LOWER("Song"."name") LIKE LOWER(%s) AND LOWER("Artist"."aname") LIKE LOWER(%s)
		ORDER BY "Song"."name";
	'''
	
	cursor = connection.cursor()
	cursor.execute(sql, (songName, artistName))
	connection.commit()
	result = cursor.fetchall()
	
	if not result:
		print("Sorry, there's no song in the database with that name.\n")
		return
	elif len(result) == 1:
		song = result[0]
	else:
		print("There are multiple songs with that name. Which would you like to add?")
 		i = 0
		for entry in result:
			print(str(i)+".      Song: " + entry[0] + "Artist: "+entry[1])
		song = result[raw_input("Enter the number of the song you want: ")]
	
	sqlGetPlaylist = '''
	SELECT "playlistid", "numsongs", "duration"
	FROM "Playlist"
	WHERE "playlistname" = %s AND "email" = %s;
	'''
	cursor.execute(sqlGetPlaylist, (playlistName, currentEmail))
	connection.commit()
	playlists = cursor.fetchall()
	if playlists != []:
		curPlaylist = playlists[0]
	else:
		return
	
	sqlAddPlaylist = '''
	INSERT INTO "PlaylistContains" (playlistid, songid, song_index)
	VALUES (%s, %s, %s);
	'''
	cursor.execute(sqlAddPlaylist, (curPlaylist[0], song[2], curPlaylist[1]))
	connection.commit()
	
	sqlUpdatePlaylist = '''
	UPDATE "Playlist"
	SET "numsongs" = "numsongs" + 1, "duration" = %s;
	WHERE "playlistid" = %s;
	'''
	cursor.execute(sqlUpdatePlaylist, (curPlaylist[2], (song[3] + curPlaylist[0])))
	connection.commit()
	
	print("Your song has been added.")

	
def remove_from_playlist():
	playlistName = ""
	while len(playlistName) == 0:
		playlistName = raw_input("Which playlist would you like to add a song to?").strip()

	songName = ""
	while len(songName) == 0:
		songName = raw_input("Which song would you like to add?").strip()
	
	artistName = ""	
	while len(artistName) == 0:
		artistName = raw_input("Who is the artist who released that song?").strip()
	
	sql = '''
	SELECT "Song"."name", "Artist"."aname", "Song"."songid", "Song"."length" 
		FROM (((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		WHERE LOWER("Song"."name") LIKE LOWER(%s) AND LOWER("Artist"."aname") LIKE LOWER(%s)
		ORDER BY "Song"."name";
	'''
	
	cursor = connection.cursor()
	cursor.execute(sql, (songName, artistName))
	connection.commit()
	result = cursor.fetchall()
	
	if not result:
		print("Sorry, there's no song in the database with that name.\n")
		return
	elif len(result) == 1:
		song = result[0]
	else:
		print("There are multiple songs with that name. Which would you like to add?")
 		i = 0
		for entry in result:
			print(str(i)+".      Song: " + entry[0] + "Artist: "+entry[1])
		song = result[raw_input("Enter the number of the song you want: ")]
	
	sqlGetPlaylist = '''
	SELECT "playlistid", "numsongs", "duration"
	FROM "Playlist"
	WHERE "playlistname" = %s AND "email" = %s;
	'''
	cursor.execute(sqlGetPlaylist, (playlistName, currentEmail))
	connection.commit()
	playlists = cursor.fetchall()
	if playlists != []:
		curPlaylist = playlists[0]
	else:
		return
		
	
def delete_playlist():
	playlistName = ""
	while len(playlistName) == 0:
		playlistName = raw_input("Which playlist would you like to delete?").strip()
	
	sqlSearch = '''

	SELECT "playlistname", "playlistid", "numsongs" 
	FROM "Playlist"
	WHERE "playlistid" = %s AND "email" = %s AND "playlistname" = %s;
	'''
	#TODO fix playlistid
	playlistid = hash( currentEmail)

	cursor = connection.cursor()
	cursor.execute(sqlSearch, (playlistid, currentEmail, playlistName))
	connection.commit()
	
	result = cursor.fetchall()
	
	if result != []:
		print("WARNING!")
		print("Are you sure you want to delete " + playlistName + "?")
		answer = -1
		while answer !=  -1:
			answer = int(raw_input("Enter 1 for yes and 0 for no: "))
		
		if answer:
			sqlDelete = '''
			DELETE FROM "Playlist" 
			WHERE "playlistid" = %s;
			'''
			cursor.execute(sqlDelete, (result[0][1],))
			connection.commit()
			sqlDelete2 = '''
			DELETE FROM "PlaylistContains"
			WHERE "playlistid" = %s;
			'''
			cursor.execute(sqlDelete, (result[0][1],))
			connection.commit()
			
		else:
			print("Play list has NOT been deleted")

def create_playlist():	
	playlistName = ""
	while len(playlistName) == 0:
		playlistName = raw_input("What would you like to name your new playlist?").strip()
	
	sql = '''
	INSERT INTO "Playlist"
	(playlistid, playlistname, numsongs, duration, email)
	VALUES (%s, %s,  %s, %s, %s);
	'''
	
	playlistid = hash(currentEmail + playlistName)
	
	
	cursor = connection.cursor()
	cursor.execute(sql, (playlistid, playlistName, 0, 0, currentEmail))
	connection.commit()
	
	print("Your playlist " + playlistName + " has been created!")

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



def search_music():
	#The user must be able to search for a song via the song, artist, album, or genre

	while True:
		show_search_menu()
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


def follower_menu():
	while True:
		show_follower_menu()
		try:
			choice = int(input("Enter option #: "))
		except ValueError:
			print("Please only enter numbers")
			choice = -1
			continue
		if choice == 0:
			break
		elif choice == 1:
			view_followers()
		elif choice == 2:
			view_following()
		elif choice == 3:
			find_user()
		elif choice == 4:
			unfollow_user()
		else:
			print("Please choose an option...")


def view_followers():
	cursor = connection.cursor()
	get_emails_sql = '''
	SELECT "UserFollows"."followerEmail"
	FROM "UserFollows"
	WHERE "UserFollows"."followeeEmail" = %s
	ORDER BY "UserFollows"."followerEmail"
	'''
	cursor.execute(get_emails_sql, (currentEmail,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, you don't have any followers yet.\n")
	else:
		print("These are your current followers:")
		for email in result:
			email = email[0]
			get_username_sql = '''
			SELECT "User"."username"
			FROM "User"
			WHERE "User"."email" = %s
			'''
			cursor.execute(get_username_sql, (email,))
			username = cursor.fetchall()[0][0]
			print("     " + username + "        (" + email + ")")
		print("\n")
	cursor.close()


def view_following():
	cursor = connection.cursor()
	get_emails_sql = '''
	SELECT "UserFollows"."followeeEmail"
	FROM "UserFollows"
	WHERE "UserFollows"."followerEmail" = %s
	ORDER BY "UserFollows"."followeeEmail"
	'''
	cursor.execute(get_emails_sql, (currentEmail,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, you aren't following anyone yet.\n")
	else:
		print("These are the users you are currently following:")
		for email in result:
			email = email[0]
			get_username_sql = '''
			SELECT "User"."username"
			FROM "User"
			WHERE "User"."email" = %s
			'''
			cursor.execute(get_username_sql, (email,))
			username = cursor.fetchall()[0][0]
			print("     " + username + "        (" + email + ")")
		print("\n")
	cursor.close()


def find_user():
	cursor = connection.cursor()
	user_email = raw_input("Please type the email of the user: ").strip()
	get_friend_sql = '''
	SELECT "User"."username"
	FROM "User"
	WHERE "User"."email" = %s
	'''
	cursor.execute(get_friend_sql, (user_email,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, there's no user in the database with that email.\n")
	else:
		user_username = result[0][0]
		check_following_sql = '''
		SELECT *
		FROM "UserFollows"
		WHERE "UserFollows"."followerEmail" = %s AND "UserFollows"."followeeEmail" = %s
		'''
		cursor.execute(check_following_sql, (currentEmail, user_email,))
		is_following = cursor.fetchall()
		if is_following:
			print("You are already following that user!")
		else:
			input = raw_input("Follow user '" + user_username + "'? (y/n): ")
			if input[0] == "y":
				add_following_sql = '''		
				INSERT INTO "UserFollows" ("followerEmail", "followeeEmail")
				VALUES (%s, %s);
				'''
				cursor.execute(add_following_sql, (currentEmail, user_email,))
				connection.commit()
				print("You are now following '" + user_username + "'!\n")
	cursor.close()


def unfollow_user():
	cursor = connection.cursor()
	user_email = raw_input("Please type the email of the user: ").strip()
	get_friend_sql = '''
	SELECT "User"."username"
	FROM "User"
	WHERE "User"."email" = %s
	'''
	cursor.execute(get_friend_sql, (user_email,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, there's no user in the database with that email.\n")
	else:
		user_username = result[0][0]
		check_following_sql = '''
		SELECT *
		FROM "UserFollows"
		WHERE "UserFollows"."followerEmail" = %s AND "UserFollows"."followeeEmail" = %s
		'''
		cursor.execute(check_following_sql, (currentEmail, user_email,))
		is_following = cursor.fetchall()
		if not is_following:
			print("You are not following that user!")
		else:
			input = raw_input("Unfollow user '" + user_username + "'? (y/n): ")
			if input[0] == "y":
				remove_following_sql = '''		
				DELETE 
				FROM "UserFollows"
				WHERE "UserFollows"."followerEmail" = %s AND "UserFollows"."followeeEmail" = %s
				'''
				cursor.execute(remove_following_sql, (currentEmail, user_email,))
				connection.commit()
				print("You are no longer following '" + user_username + "'\n")
	cursor.close()


def play_song():
	cursor = connection.cursor()
	song_name = raw_input("Please type the song name: ").strip()
	get_song_sql = '''
	SELECT "Song"."name", "Artist"."aname", "Song"."songid"
	FROM (((("Song"
	INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
	INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
	INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
	INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
	WHERE LOWER("Song"."name") = LOWER(%s)
	ORDER BY "Song"."name";
	'''
	cursor.execute(get_song_sql, (song_name,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, there's no song in the database with that name.\n")
		cursor.close()
		return
	elif len(result) == 1:
		song = result[0]
	else:
		print("There are multiple songs with that name. Which would you like to listen to?")
		i = 1
		for entry in result:
			print(str(i)+".      Song: " + entry[0] + "Artist: "+entry[1])
			i = i + 1
		song = result[int(raw_input("(enter the number of the song you want: )")) - 1]

	print("Playing "+song[0]+" by "+song[1])
	add_to_history_sql = '''
	INSERT INTO "PlayHistory" (email, songid, listen_date)
	VALUES (%s, %s, %s);
	'''
	cursor.execute(add_to_history_sql, (currentEmail, song[2], datetime.now().strftime("%Y/%m/%d"),))
	connection.commit()
	update_listens_sql = '''
	UPDATE "Song" SET listens = listens + 1
	WHERE songid = %s;
	'''
	cursor.execute(update_listens_sql, (song[2],))
	cursor.close()


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
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Song"."name") LIKE LOWER(%s)
		ORDER BY "Song"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
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
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Artist"."aname") LIKE LOWER(%s)
		ORDER BY "Artist"."aname";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."aname", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Artist"."aname") = LOWER(%s)
		ORDER BY "Artist"."aname";
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
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Album"."name") LIKE LOWER(%s)
		ORDER BY "Album"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
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
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
		INNER JOIN "GenreClassifies" ON "GenreClassifies"."songid" = "Song"."songid")
		INNER JOIN "Genre" ON "Genre"."name" = "GenreClassifies"."gname")
		WHERE LOWER("Genre"."name") LIKE LOWER(%s)
		ORDER BY "Genre"."name";
		'''
		search = "%" + search + "%"	
	else:
		sql = ''' 
		SELECT "Song"."name", "Album"."name", "Artist"."aname", "Genre"."name", "Song"."length", "Song"."listens"
		FROM (((((("Song"
		INNER JOIN "AlbumContains" ON "AlbumContains"."songid" = "Song"."songid")
		INNER JOIN "Album" ON "Album"."albumid" = "AlbumContains"."albumid")
		INNER JOIN "ArtistReleases" ON "ArtistReleases"."songid" = "Song"."songid")
		INNER JOIN "Artist" ON "Artist"."aname" = "ArtistReleases"."aname")
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


def top_ten_artists():
	cursor = connection.cursor()
	get_friend_sql = '''
		SELECT "PlayHistory"."songid"
		FROM "PlayHistory"
		WHERE "PlayHistory"."email" = %s
		'''
	cursor.execute(get_friend_sql, (currentEmail,))
	result = cursor.fetchall()
	if not result:
		print("Sorry, this user hasn't played any songs yet.\n")
	else:
		songs = dict()
		for song in result:
			if song in songs:
				songs[song] = songs[song] + 1
			else:
				songs[song] = 1

		artists = dict()
		for song in songs:
			get_artist_sql = '''
				SELECT "ArtistReleases"."aname"
				FROM "ArtistReleases"
				WHERE "ArtistReleases"."songid" = %s
				'''
			cursor.execute(get_artist_sql, (song,))
			result = cursor.fetchall()
			artist = result[0][0]
			if artist in artists:
				artists[artist] = artists[artist] + songs[song]
			else:
				artists[artist] = songs[song]
		sorted_artists = sorted(artists.items(), key=operator.itemgetter(1), reverse=True)
		print("Top 10 Favorite (Most Played) Artists:")
		for i in range(0, 10):
			if i == len(sorted_artists):
				break
			print("     " + str(i + 1) + ". " + sorted_artists[i][0] + ", listened to " + str(
				sorted_artists[i][1]) + " times")
	print("")
	cursor.close()


if __name__ == "__main__":
        main()
