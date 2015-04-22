import praw,httplib,io,time,ctypes
def main():
    path = "D:/redditWallpapers/"
    dateToday = time.localtime()
    ddmmyy = time.ctime()[0:11] + time.ctime()[-1:-5:-1][::-1]
    listOfDates = getDatesDownloaded(path)
    if(not(ddmmyy in listOfDates)):
        pictureUrl = getImgurLink()    
        downloadImage(pictureUrl , ddmmyy, path)
        setWallpaperForTheDay(ddmmyy, path)
    else:
        print("Already downloaded")
    
def getImgurLink():
    redditObject = praw.Reddit(user_agent = 'Wallpaper Get')
    while True:
        TopWallpaperSubmissions = redditObject.get_subreddit('wallpapers').get_top_from_day(limit = 1)
        for submission in TopWallpaperSubmissions:
            try:
                return submission.url
            
            except ConnectionError:
                continue
    
def getDatesDownloaded(path):
    logList = []
    logFile = open(path + "wallpaperLog.txt" , 'r')
    for line in logFile.readlines():
        logList.append(line)
    return logList

def downloadImage(url , date, path):
    connectionToImage = httplib.HTTPConnection("i.imgur.com")
    connectionToImage.request("GET", url[-1:-12:-1][::-1])
    imageResponse = connectionToImage.getresponse()
    imageData = imageResponse.read()    
    dataWriter = io.FileIO(path + 'wallpaperOfTheDay ' + date + '.jpg', 'w')
    dataWriter.write(imageData)
    updateDateFile(date, path)
    print("Downloaded and added to list")
    
def updateDateFile(date, path):
    logFile = open(path + 'wallpaperLog.txt','a')
    logFile.write(date)
    logFile.close()

def setWallpaperForTheDay(date, path):
    ctypes.windll.user32.SystemParametersInfoA(20,0,path + "wallpaperOfTheDay " + date + ".jpg", 0)
    
main()
