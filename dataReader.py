import math
import numpy
import array
import time
import csv
import cv2

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
    charList1 = readData(filename + "01")
    #charList2 = readData(filename + "02")
    #charList3 = readData(filename + "03")
    #print(len(charList))
    #printCharList(charList)

    #call the averaging (v1) function
    trainedList = avgDatav1([charList1])

    writeData(trainedList)

def printCharList(cL):
    #print("begin printCharList")
    for i in range(0,len(cL)):
        print("\n\n\nchar:" + LEXICON[i] +":\n")
        for j in range(0,len(cL[i])):
            print(" stroke:" + str(j+1) + ":")
            for k in cL[i][j]:
                #print(len(cL))
                print("  :" + str(k[0]) + ":" + str(k[1]) + ":")
                
def avgDatav1(cLL):#average the set of datalists - returns a single list
    
    lnum = len(cLL)

    #for i in cLL:
    #    i = scaleData(i)
    avgList = [[]]
    #go through and average each character
    for i in range(0,62):
        div = 0
        avgX = 0
        avgY = 0
        for l in cLL:
            for s in l[i]:
                for d in s:
                    div+=1
                    avgX+=d[0]
                    avgY+=d[1]
        avgX/=div
        avgY/=div
        print("avgX :" + str(avgX) + ": avgY :" + str(avgY))
        if i == 0:
            avgList[0] = [avgX,avgY]
        else:
            avgList.insert(i, [avgX,avgY])

def writeData(cL):

    with open("output","w") as file:
        for i in range(0,len(cL)):
            file.write("\n\n\nchar:" + LEXICON[i] +":\n")
            for j in range(0,len(cL[i])):
                file.write("\n\nstroke:" + str(j+1) + ":\n\n")
                for k in cL[i][j]:
                    #print("i,j = " + str(i) + "," + str(j))
                    file.write(":" + str(k[0]) + ":" + str(k[1]) + ":\n")

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
            #sets the counter to iterate through the dataStream array
            
            #this will read each character's id (if the line starts with ".SEGMENT")

            while(counter < len(dataStream) and dataStream[counter][0:8] != seg):
                #print("skip line")
                counter+=1
            charNum = charCounter#HOORAY! we have the character id, now just get each individual stroke and all of the coordiantes within
            charCounter+=1
            counter+=1
            strokeNum = 0
            #print("before big while")
            while(counter < len(dataStream) and dataStream[counter+2][0:8] != seg):
                #print("start of big while")
                #checks the line of input to see if it is equal to ".PEN_DOWN" - if it is pend, then begin intaking the stream of coordinates until you reach penu - this stream of coordinates is one stroke - check again 
                #print("before until pend while - counter:" + str(counter) + ": and dataStream[counter]:" + dataStream[counter])
                while(counter < len(dataStream) and dataStream[counter][0:9] != pend):
                    #print("until pend")
                    counter+=1#iterates until it is pend
                #print(counter)
                counter+=1
                coordStream = [[]]
                coordCount  = 0
                #loads the first coord in the stream just to make it simpler while using the .append function
                coordStream[0] = getCoord(dataStream[counter])
                counter+=1
                coordCount+=1
                #print("before coord while")
                while(counter < len(dataStream) and dataStream[counter][0:7] != penu):
                    #go through this loop until the stroke is done
                    #have a function that returns a coordinate, an array with two indexes, 0 = x, 1 = y
                    #print("coordCount" + str(coordCount))
                    coordStream.append(getCoord(dataStream[counter]))
                    #print("coordStream[coordCount = " + str(coordStream[coordCount]))
                    coordCount+=1
                    counter+=1
                #print("charNum = " + str(charNum) + "   strokeNum = " + str(strokeNum))
                if charNum == 0:
                    if strokeNum == 0:
                        charList[0][0] = coordStream
                    else:
                        charList[0].append(coordStream)
                elif strokeNum == 0:
                    newStrokeList = [[[]]]
                    newStrokeList[0] = coordStream
                    charList.append(newStrokeList)    
                else:                  
                    charList[charNum].append(coordStream)
                counter +=1
                strokeNum+=1
            #print(len(charList))
            #print("charC:"+str(charCounter)+": counter:"+str(counter)+":")

    return charList

def getCharNum(s):#will get the character index from the line string
    
    splitstring = s.split(" ")
    for i in splitstring:
        if i.isdigit():
            return int(i)
    return (-1)

def getCoord(s):#will get the array [x,y] from the string, which is just the line containing the coordinate

    coord = s.split(" ")
    #print("coord = " + str(coord))
    
    intcoord = [0,0]
    #print(coord[-1])
    if coord[0] == "":
        intcoord[0] = int(coord[1])
    else:
        intcoord[0] = int(coord[0])
    intcoord[1] = int(coord[-1])
    return intcoord


if __name__ == "__main__":
    main()