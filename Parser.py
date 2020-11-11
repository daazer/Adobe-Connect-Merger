import os
import re
cameraVoips = []
screenShares = []
mappedCameraVoips = []
mappedScreenShares = []
extractedDirectory = ""

def findFolder():
    extractedDirectory = input("where is the file located\n")
    findScreenShares(extractedDirectory)
    findCameraVoips(extractedDirectory)
    doMapping(extractedDirectory)



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

def doMapping(extractedDirectory):
    indexstream = open(extractedDirectory + "\indexstream.xml" , "r")
    for line in indexstream:
        if(containsTime(line)):
            time = line.split("\"")[1]
        elif(containsVoip(line)):
            mapTimeVoip(line , time)
        elif(containsScreen(line)):
            mapTimeScreen(line,time)


def mergeAudioAndVideo():
    os.system("ffmpeg -i screenshare_1_4.flv -i cameraVoip_0_3.flv -c:v copy -c:a aac output.mp4")

def hReadableTime() :
    for index in mappedCameraVoips :
        time = int(index[1])
        if time>3600000:
            hour = int(time/3600000)
            time = (time - hour*3600000)
            minute = int(time/60000)
            time = (time - minute * 60000)
            print(index[0] + "  ==>   " + str(hour) + ":" + str(minute) + ":" + str(time))
        elif time>60000:
            minute = int(time/60000)
            time = (time - (minute * 60000))
            print(index[0] + "  ==>   " + "00" + ":" + str(minute) + ":" + str(time))
        else:
            print(index[0] + "  ==>   " + "00" + ":" + "00" + ":" + str(time))
    for index in mappedScreenShares :
        time = int(index[1])
        if time>3600000:
            hour = int(time/3600000)
            time = (time - hour*3600000)
            minute = int(time/60000)
            time = (time - minute * 60000)
            print(index[0] + "  ==>   " + str(hour) + ":" + str(minute) + ":" + str(time))
        elif time>60000:
            minute = int(time/60000)
            time = (time - (minute * 60000))
            print(index[0] + "  ==>   " + "00" + ":" + str(minute) + ":" + str(time))
        else:
            print(index[0] + "  ==>   " + "00" + ":" + "00" + ":" + str(time))
        
findFolder()
# findScreenShares(extractedDirectory)
# findCameraVoips(extractedDirectory)
# doMapping()
# print(*mappedCameraVoips , sep="\n")
# print(*mappedScreenShares , sep = "\n")
hReadableTime()

#mergeAudioAndVideo()
