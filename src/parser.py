import csv
import os
import re
import sys




def main():
    data_ACOUSTICNESS = 0
    data_ARTISTS = 1
    data_DANCEABILITY = 2
    data_DURATION_MS = 3
    data_ENGERY=4
    data_EXPLICIT=5
    data_ID=6
    data_INSTRUMENTALNESS=7
    data_KEY=8
    data_LIVENESS=9
    data_LOUDNESS=10
    data_MODE=11
    data_NAME=12
    data_POPULARITY=13
    data_RELEASE_DATE=14
    data_SPEECHINESS=15
    data_TEMPO =16
    data_VALNCE =17
    data_YEAR = 18

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
        musicDB[row[data_ID]] = [row[data_NAME], row[data_ARTISTS], row[data_YEAR], row[data_RELEASE_DATE], row[data_ID]]

    for entry in musicDB:
        print(entry, musicDB[entry])

if __name__ == "__main__":
    main()
