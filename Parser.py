import os
import re
cameraVoips = []
screenShares = []
mappedCameraVoips = []
mappedScreenShares = []


def findShit():
    indexstream = open("indexstream.xml" , "r")
    print(cameraVoips)



extractedDirectory = "."
def findCameraVoips(extractedDirectory):
    for filename in os.listdir(extractedDirectory):
        if "cameraVoip" in filename:
            if "flv" in filename:
                cameraVoips.append(filename.split(".flv")[0])

def findScreenShares(extractedDirectory):
    for filename in os.listdir(extractedDirectory):
        if "screenshare" in filename:
            if "flv" in filename:
                screenShares.append(filename.split(".flv")[0])

    
def containsTime(line):
    if("<Message time=" in line) :
        return True
    else:
        return False

def containsVoip(line):
    if("cameraVoip" in line):
        return True
    else:
        return False

def containsScreen(line):
    if ("screenshare" in line):
        return True
    else:
        return False

def mapTimeScreen(line , time):
    for exact in screenShares :
        if (exact in line):
            mappedScreenShares.append([exact,time])
            screenShares.remove(exact)


def mapTimeVoip (line , time):
    for exact in cameraVoips :
        if (exact in line):
            mappedCameraVoips.append([exact , time])
            cameraVoips.remove(exact)

def doMapping():
    indexstream = open("indexstream.xml" , "r")
    for line in indexstream:
        if(containsTime(line)):
            time = line.split("\"")[1]
        elif(containsVoip(line)):
            mapTimeVoip(line , time)
        elif(containsScreen(line)):
            mapTimeScreen(line,time)


def mergeAudioAndVideo():
    os.system("ffmpeg -i screenshare_1_4.flv -i cameraVoip_0_3.flv -c:v copy -c:a aac output.mp4")

findScreenShares(extractedDirectory)
findCameraVoips(extractedDirectory)
doMapping()
print(*mappedCameraVoips , sep="\n")
print(*mappedScreenShares , sep = "\n")

#mergeAudioAndVideo()
