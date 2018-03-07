import math
import numpy
import array
import time
import csv
#yo listen up here is the story
'''
    dataReader.py will read 10 of the UJIpenchars-wXX files and will return
      a file of the master (trained average) set of characters
    
    Author - Duncan Harmon

    for AI with Ms. Bunn

    On my honor, I have neither given nor recieved any unauthorized help
      on this assignment

    6 March 2018
'''

#stuff for reading the files, edit based on the type of file you're
#reading.  For this, nothing should really be changed unless there
#is an error.

filename = "UJIpenchars-w" #this will be (later) followed by a two digit number, 01-11
LEXICON  = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]

#these are the commands within the actual input files
seg      = ".SEGMENT"
pend     = ".PEN_DOWN"
penu     = ".PEN_UP"
def main():
    #this will get the read data, average them into the master set, and print to a file
    charList = readData(filename + "01")
    printCharList(charList)

def printCharList(cL):
    for i in range(0,len(cL)):
        print(LEXICON[i] +"\n")
        for j in range(0,len(cL[i])):
            print("stroke #" + str(j+1))
            for k in cL[i][j]:
                print("  " + k[0] + " " + k[1])


def readData(fn):

    charList = [[[[]]]]
    #charList is a 4D array with setup [charNum[strokeNum[coordinate[x,y]]]]
    with open(("data/"+fn),"r") as file:
        #these files come with some stuff in the front, only the .LEXICON line is useful
        #the first 40 lines of each file are useless - this gets rid of them for all we care
        for i in range(1,40):
            file.readline()
        #dataStream is an array of all of the lines in the file to be read
        dataStream = file.readlines()
        counter = 0
        charCounter = 0
        for i in range(0,62):
            #sets the coutner to iterate through the dataStream array
            
            #this will read each character's id (if the line starts with ".SEGMENT")

            while(counter < len(dataStream) and dataStream[counter][0:8] != seg):
                counter+=1
            charNum = charCounter#HOORAY! we have the character id, now just get each individual stroke and all of the coordiantes within
            charCounter+=1
            counter+=1
            strokeNum = 0
            while(counter < len(dataStream) and dataStream[counter+2] != seg):
                #checks the line of input to see if it is equal to ".PEN_DOWN" - if it is pend, then begin intaking the stream of coordinates until you reach penu - this stream of coordinates is one stroke - check again 
                while(counter < len(dataStream) and dataStream[counter] != pend):
                    counter+=1#iterates until it is pend
                counter+=1
                coordStream = []
                coordCount  = 0
                while(counter < len(dataStream) and dataStream[counter] != penu):
                    #go through this loop until the stroke is done
                    #have a function that returns a coordinate, an array with two indexes, 0 = x, 1 = y
                    coordStream[coordCount] = getCoord(dataStream[counter])
                charList[charNum][strokeNum] = coordStream
                counter +=1
                print(counter)
    return charList

def getCharNum(s):#will get the character index from the line string
    
    splitstring = s.split(" ")
    for i in splitstring:
        if i.isdigit():
            return int(i)
    return (-1)

def getCoord(s):#will get the array [x,y] from the string, which is just the line containing the coordinate

    coord = s.split(" ")
    coord[0] = int(coord[0])
    coord[1] = int(coord[1])
    return coord


if __name__ == "__main__":
    main()