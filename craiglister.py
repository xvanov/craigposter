from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
import datetime
import os
import shutil
import sys
import smtplib, ssl
from inspect import getsourcefile
from os import environ
from os import listdir
from gmail import Gmail
from datetime import date
from PIL import Image
#from dotenv import load_dotenv, find_dotenv
from os.path import abspath, join, dirname
import traceback
import random




#--------------------------------------- Importing Stuff ----------------------
options = webdriver.ChromeOptions()
ua = UserAgent()
userAgent = ua.random
#options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument('user-agent={userAgent}')

file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)
listingsFolderDirectory = os.path.abspath(os.path.join(file_dir, "listings"))
listedFolderDirectory = os.path.join(listingsFolderDirectory,"listed")




#------------------Pull in email credentials---------------
#dotenv_path = join(dirname(__file__), 'settings_craiglister.env')
#dotenv_path = '/home/ubuntu/CraigListerSettings/settings_craiglister.env'
#load_dotenv(dotenv_path)


#------------------------------- Set Up Necessary Directories ---------

class listingInfoParse(object):
    def __init__(self,f):
        self.loc = parsing(f,"<Location>").lower()
        self.title = parsing(f,"<Title>")
        self.type = parsing(f,"<Type>")
        self.category = parsing(f,"<Category>")
        self.area = parsing(f, "<Area>")
        self.email = parsing(f,"<Email>")
        self.street = parsing(f,"<Street>")
        self.city = parsing(f,"<City>")
        self.xstreet = parsing(f,"<CrossStreet>")
        self.state = parsing(f,"<State>")
        self.geographicarea = parsing(f,"<GeographicArea>")
        self.postal = parsing(f,"<Postal>")
        self.body = parsing(f,"<Body>")
        # just get rid of everything that not unicode
        self.body = ''.join([i if ord(i) < 128 else '' for i in self.body])
        # tabs will actually go to the next field in craiglist
        self.body = " ".join(self.body.split("\t"))
        self.price = parsing(f,"<Price>")
        self.private_room = parsing(f,"<Private_room>")
        self.private_bath = parsing(f,"<Private_bath>")
        self.housing_type = parsing(f,"<Housing_type>")
        self.laundry = parsing(f,"<Laundry>")
        self.parking = parsing(f,"<Parking>")




#------------------------------  Helper Functions -----------------

# Prerequesit: element that is dentified, text that you want to input
def clickDropdown(identifier, information):
    select = identifier
    select.click()
    select.send_keys(information)
    select.send_keys(Keys.ENTER)




#------------------------------  Driver Navigation -----------------

#[[[[[[[[[[[[CLICKS]]]]]]]]]]]]]]]
def clickLocation(listing):
    #opens the dropdown, types in listin.city, then hits enter
    clickDropdown(listing.driver.find_element_by_id("ui-id-1-button"), listing.city)
    listing.driver.find_element_by_xpath("//button[@name='go']").click()

def clickArea(listing):
    listing.driver.find_element_by_xpath("//*[contains(text(),'"+ listing.area+"')]").click()

def clickDoneOnImageUploading(listing):
    listing.driver.find_element_by_xpath('//button[text()="done with images" ]').click()

# Don't always have to do this
def clickAbideByGuidelines(listing):
    try:
        listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/div/form/button").click()
    except:
        pass

def clickClassImageUploader(listing):
	listing.driver.find_element_by_id("classic").click()

def clickListingType(listing):
    listing.driver.find_element_by_xpath("//*[contains(text(),'"+ listing.type+"')]").click()

def clickListingCategory(listing):
    listing.driver.find_element_by_xpath("//*[contains(text(),'"+ listing.category+"')]").click()
    #listing.driver.find_element_by_xpath("//section/form/blockquote//label[contains(.,'" + listing.category + "')]/input").click()

def clickAcceptTerms(listing):
    listing.driver.find_element_by_xpath("/html/body/form[1]/input[4]").click()
    #listing.driver.find_element_by_partial_link_text("chicago.craigslist.org").click()

def clickPublishListing(listing):
    listing.driver.find_element_by_xpath('//button[text()="publish"]').click()

#[[[[[[[[[[[[TASKS]]]]]]]]]]]]]]]
def uploadImagePath(listing,image):
	listing.driver.find_element_by_xpath(".//*[@id='uploader']/form/input[3]").send_keys(image)

def fillOutListing(listing):
    listing.driver.find_element_by_name("PostingTitle").send_keys(listing.title)
    listing.driver.find_element_by_name("FromEMail").send_keys(listing.email)
    listing.driver.find_element_by_name("geographic_area").send_keys(listing.geographicarea)
    listing.driver.find_element_by_name("postal").send_keys(listing.postal)
    listing.driver.find_element_by_name("PostingBody").send_keys(listing.body)
    listing.driver.find_element_by_name('price').send_keys(listing.price)

    #listing.driver.find_element_by_xpath("//select[@name='moveinMonth']/option[text()='jul']").click()
    clickDropdown(listing.driver.find_element_by_id("ui-id-1-button"),listing.private_room)
    clickDropdown(listing.driver.find_element_by_id("ui-id-3-button"),listing.private_bath)
    clickDropdown(listing.driver.find_element_by_id("ui-id-2-button"),listing.housing_type)
    clickDropdown(listing.driver.find_element_by_id("ui-id-4-button"),listing.laundry)
    clickDropdown(listing.driver.find_element_by_id("ui-id-5-button"),listing.parking)

    listing.driver.find_element_by_xpath("/html/body/article/section/form/div/div/fieldset[2]/div/div/div[2]/label/label[2]/input").click()
    listing.driver.find_element_by_name("no_smoking").click()
    listing.driver.find_element_by_name("is_furnished").click()
    listing.driver.find_element_by_xpath("//button[@name='go']").click()

def elementIdVisible(element):
    print("Element {} is visible? ".format(element) + str(listing.driver.find_element_by_id(element).is_displayed()))

def elementNameVisible(element):
    print("Element {} is visible? ".format(element) + str(listing.driver.find_element_by_name(element).is_displayed()))

def fillOutGeolocation(listing):
    #time.sleep(1)
    elementNameVisible('xstreet0')
    #options.add_argument("window-size=1200x600")
    listing.driver.find_element_by_name("xstreet0").send_keys(listing.street)
    listing.driver.find_element_by_name("xstreet1").send_keys(listing.xstreet)
    #listing.driver.find_element_by_name("city").send_keys(listing.city)
    #listing.driver.find_element_by_name("region").send_keys(listing.state)
    #time.sleep(1)
    #elementIdVisible('search_button')
    listing.driver.find_element_by_id("search_button").click()
    #time.sleep(1)
    listing.driver.find_element_by_xpath("//*[@id='leafletForm']/button[1]").click()

def removeImgExifData(path):
    filename, extension = os.path.splitext(path)
    fullFilename = filename+extension
    image = Image.open(fullFilename)
    data = list(image.getdata())
    imageNoExif = Image.new(image.mode, image.size)
    imageNoExif.putdata(data)
    imageNoExif.save(filename + "copy" + extension)
    os.remove(filename + extension)
    os.rename(filename + "copy" + extension,fullFilename)

def uploadListingImages(listing):
    clickClassImageUploader(listing)
    for image in listing.images:
        removeImgExifData(image)
        uploadImagePath(listing,image)
        #time.sleep(1)
    clickDoneOnImageUploading(listing)

def postListing(listing):
    clickLocation(listing)
    print("clicked location")

    clickArea(listing)
    print("clicked area")

    clickListingType(listing)
    print("clicked listing type")

    clickListingCategory(listing)
    print("Clicked Category")

    #clickAbideByGuidelines(listing)
    #print("Clicked Guidelines")

    fillOutListing(listing)
    print("Filled out listing")

    fillOutGeolocation(listing)
    print("Clicked Geolocation")

    uploadListingImages(listing)
    print("Uploaded images")

    clickPublishListing(listing)
    print("Clicked publish listing")




# --------------------------- Emails ---------------------

def getCraigslistEmailUrl(listing,emails):
    for email in emails:
        email.fetch()
        email.read()
        if listing.title[0:15] and "email verification" in email.subject:
            emailMessage = email.body
            acceptTermsLink = emailMessage.split("https")
            acceptTermsLink = acceptTermsLink[1].split("\r\n")
            email.delete()
            print("Confirmation URL: https{0}".format(acceptTermsLink[0]))
            return acceptTermsLink[0]


def acceptTermsAndConditions(listing,termsUrl):
    listing.driver.get("https" + termsUrl)
    print("URL loaded: https{0}".format(termsUrl))
    #clickAcceptTerms(listing)
    #time.sleep(10)

def acceptEmailTerms(listing):
    gmail = Gmail()
    #print(gmailUser,os.getenv("GMAILPASS"))
    gmail.login(gmailUser,os.getenv("GMAILPASS"))
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    print("Receiving email confirmation...")
    sleep_time = 2
    print('sleep for {} s'.format(sleep_time))
    time.sleep(sleep_time)
    print ("Checking email")
    emails = gmail.inbox().mail(sender="robot@craigslist.org",unread=True,after=datetime.date(year, month, day-1))
    termsUrl = getCraigslistEmailUrl(listing,emails)
    acceptTermsAndConditions(listing,termsUrl)

    gmail.logout()
    print ("Confirmed")




# --------------------------- Craigslist Posting Actions ---------------


def moveToListedFolder(folder,listedFolderDirectory):
    
    #/home/ubuntu/CraigLister/listings/listed
    doesItExist = os.listdir(file_dir + '/listings/listed')
    todaysDate = time.strftime("%x").replace("/","-")
    print(doesItExist)
    print(todaysDate)

    # %x >>>get the date like this 7/16/2014
    today_dir = os.path.join(listedFolderDirectory,time.strftime("%x").replace("/","-"))

    # Make todays date under the listed directory
    if todaysDate in doesItExist:
        shutil.move(folder, today_dir)
        print('only moved')
    else:
        os.makedirs(today_dir)
        shutil.move(folder, today_dir)
        print("made and moved")

def parsing(f,splits):
    fsplit = f.split(splits)
    return fsplit[1]


# If more than 24 hours passed will look like
# 1 day, 13:37:47.356000
def hasItBeenXDaysSinceFolderListed(folder,x):
    dateSplit = folder.split('-')
    folderDate = datetime.date(int(dateSplit[2]) + 2000, int(dateSplit[0]), int(dateSplit[1]))
    currentDatetime = datetime.datetime.now()
    folderTimePassed = currentDatetime - datetime.datetime.combine(folderDate, datetime.time())
    if "day" not in str(folderTimePassed):
        return False
    daysPassed = str(folderTimePassed).split('day')[0]
    if int(daysPassed.strip()) >= x:
        return True
    return False

def getOrderedListingImages(listingFolder):
    print ('listingFolder',listingFolder)
    listingImages = [f for f in os.listdir(listingFolder) if os.path.isfile(os.path.join(listingFolder,f)) and f[0] != '.'  and f != 'info.txt' ]
    print ('listingImages',listingImages)
    secondList = [os.path.abspath(os.path.join(listingFolder, x)) for x in listingImages if (x[1] != "_") or (x[0].isdigit() == False) and x[0] != '.']
    firstList = [os.path.abspath(os.path.join(listingFolder, x)) for x in listingImages if (x[1] == "_") and (x[0].isdigit()) and x[0] != '.']

    firstList.sort()
    secondList.sort()

    orderedListingImages = []
    for x in firstList:orderedListingImages.append(x)
    for x in secondList:orderedListingImages.append(x)
    return orderedListingImages





# Get all the date folders of listed items
listedItemsFolders = [folder for folder in os.listdir(listedFolderDirectory) if folder[0] != "."]

# Moving items that are 3 days or older back into the queue to get listed again
for dayListedFolder in listedItemsFolders:

    #if (hasItBeenXDaysSinceFolderListed(dayListedFolder,3) == False):
        #continue
    if 'placeholder' in dayListedFolder:
        continue

    listedFolders = [listedFolders for listedFolders in os.listdir(os.path.join(listedFolderDirectory,dayListedFolder)) if listedFolders[0] != "."]
    dayListedFolderDirectory = os.path.join(listedFolderDirectory,dayListedFolder)

    for listedFolder in listedFolders:
        theListedFolderDirectory = os.path.join(dayListedFolderDirectory,listedFolder)
        shutil.move(theListedFolderDirectory,listingsFolderDirectory)
    shutil.rmtree(dayListedFolderDirectory)













# ------------------------------LIST ITEMS----------------------------------
listingFolders = [listing for listing in os.listdir(listingsFolderDirectory) if listing[0] != "." and listing != "listed"]
cycleNum = 1
linkCounter=-1

for listingFolder in listingFolders:

    if True:

        listingFolder = os.path.abspath(os.path.join(listingsFolderDirectory, listingFolder))
        with open(os.path.abspath(os.path.join(listingFolder, 'info.txt')), 'r') as info:
            listing = listingInfoParse(info.read())

        #Pull in the email credentials
        gmailUser = listing.email
        print(userAgent)
        listing.images = getOrderedListingImages(listingFolder)
        print("images are ready")

        driver = webdriver.Chrome(options=options, executable_path='/usr/lib/chromium-browser/chromedriver')
        #'/home/alex/cur/rep/CraigLister/chrome87-linux'
        #driver = webdriver.Chrome(options=options, executable_path=file_dir + '/chrome87-win') 
        #driver = webdriver.Chrome(options=options, executable_path='/home/ubuntu/CraigLister/chrome87-mac')
        listing.driver = driver
        print("driver is ready")


        listing.driver.start_client()
        listing.driver.implicitly_wait(5)

        listing.driver.get("https://post.craigslist.org/c/" + listing.loc + "?lang=en")
        print("site reached")

        postListing(listing)
        acceptEmailTerms(listing)

        print("Listings posted: ", cycleNum)
        cycleNum = cycleNum + 1

        listing.driver.quit()
        listing.driver.stop_client()

        moveToListedFolder(listingFolder,listedFolderDirectory)
        sleeptime = 5
        print ("Waiting {} seconds".format(sleeptime))
        time.sleep(sleeptime)

    else: #Sends an email when an error occurs

        errorString = traceback.format_exc() #Gets the traceback log after an error happens

        receiver_email = os.getenv("ToEmail")
        message = "Subject: Craigslist Error Occurred!\n\nHere's the log:\n\n " + errorString
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = os.getenv("SenderEmail")
        password = os.getenv("GMAILPASS")

        # Try to log in to server and send email
        server = smtplib.SMTP(smtp_server,port)
        server.starttls() # Secure the connection
        print(sender_email, password)
        server.login(sender_email, password)
        server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=message) # send email
        server.quit() 
        sys.exit()





#  Sends an email upon success!
#      |  |  |
#      V  V  V
today_dir = os.path.join(listedFolderDirectory,time.strftime("%x").replace("/","-"))
today_date = time.strftime("%x").replace("/","-")
receiver_email = os.getenv("ToEmail")
message = "Subject: Successful job " + today_date + "\n\nHere's what posted: \n\n" + str(os.listdir(today_dir)) + "\n\n Tune in next week!"

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = os.getenv("SenderEmail")
password = os.getenv("GMAILPASS")

# Try to log in to server and send email
server = smtplib.SMTP(smtp_server,port)
server.starttls() # Secure the connection
server.login(sender_email, password)
server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=message) # send email
server.quit()
sys.exit()
