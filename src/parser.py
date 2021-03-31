import csv
import os
import re
import sys


#COLUMN CHEAT SHEET
global ACOUSTICNESS 
global ARTISTS 
global DANCEABILITY 
global DURATION_MS 
global ENGERY
global EXPLICIT
global ID
global INSTRUMENTALNESS
global KEY
global LIVENESS
global LOUDNESS
global MODE
global NAME
global POPULARITY
global RELEASE_DATE
global SPEECHINESS
global TEMPO 
global VALNCE 
global YEAR
ACOUSTICNESS = 0
ARTISTS = 1
DANCEABILITY = 2
DURATION_MS = 3
ENGERY=4
EXPLICIT=5
ID=6
INSTRUMENTALNESS=7
KEY=8
LIVENESS=9
LOUDNESS=10
MODE=11
NAME=12
POPULARITY=13
RELEASE_DATE=14
SPEECHINESS=15
TEMPO =16
VALNCE =17
YEAR = 18


def main():

    if  len(sys.argv) < 2 :
        print("Please put the file name as the command line arugment")
        print("Usage: python parser.py <file_name>")
        print("Make sure to inclue to correct file path!")
        exit(0)
    else:
        filename = sys.argv[1]

    if(os.path.exists(filename) and os.path.isfile(filename)):
        data = open(filename, "r")
    else:
        print("Please check if this file exists and if you are passing the correct path")
        exit(0)
    musicDB = {}
    baseData = csv.reader(data)
    for row in baseData:
        print(row[ARTISTS])


if __name__ == "__main__":
    main()
