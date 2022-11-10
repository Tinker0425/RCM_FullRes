#################
# KT - 11/9/22
# Goal is to grab Full Res RCM
# Mini forge: python C:/Users/kayla.tinker/Desktop/SARFullRes.py
###############
### Must name month file i.e. 'November_2022'
### Must name day file i.e. '04Nov22'
### Line 46 & 47 need user input
#################

from datetime import date, timedelta
import datetime
#from bs4 import BeautifulSoup
import requests
import re
import io
import os
import os.path
import zipfile
import shutil



### First get the current date names for strings
today = date.today()
year = today.strftime("%Y")
yr = today.strftime("%y")
month = today.strftime("%B")
mon = today.strftime("%b")
mon_num = today.strftime("%m")
day = today.strftime("%d")
print('Current date: ',yr, mon, day)

### Only need for the text file:
yesterday = today - timedelta(days=1)
print(yesterday)
yr_y = yesterday.strftime("%y")
mon_y = yesterday.strftime("%b")
day_y = yesterday.strftime("%d")

url = 'https://www.star.nesdis.noaa.gov/socd/mecb/rcm/NWSAlaska/'

### Only need for the text file:
filename_Mapping = 'FilenameMapping_'+day_y+mon_y+yr_y+'-'+day+mon+yr+'.txt'
url_filename_Mapping = url+filename_Mapping
username = ''
password = ''

#data = requests.get(url, auth=(username, password)).text
#soup = BeautifulSoup(data, 'html.parser')

### Only need for the text file:
data_txt = requests.get(url_filename_Mapping, auth=(username, password)).text.split()
for line in data_txt:
    both_strings = str(line).split(',')
    filename_tiff = both_strings[0]
    filemap = both_strings[1]
    lon_eastorwest = filemap[47]
    lon_check = int(filemap[41:44])


### grab correct file
##for link in soup.findAll('a', attrs={'href': re.compile(year+mon_num+day)}):
    #print('zipped filename: ',link.get('href'))
    ##filename_tiff = str(link.get('href'))


    full_url = url+filename_tiff
    folder = 'I:\\IMAGERY\\SarImages_Daily\\'+month+'_'+year+'\\'+day+mon+yr+'\\'
    output = folder+filename_tiff
    print(output)
    datestring = filename_tiff[-29:-21]

    if os.path.exists(output):
        print(filename_tiff,': File exists')

    elif lon_check >= 180 and lon_eastorwest == "E":
        print(filename_tiff,': File may be over 180 line')

    elif datestring != year+mon_num+day:
        print(datestring, year+mon_num+day, ': file is not from today')

    else:
        print('Please wait for file to download and unzip, may take multiple minutes')
        r = requests.get(full_url, auth=(username, password))
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(output)
        ###Rename folder
        print('Download complete for this folder, now moving imagery files to DDMMMYY and rename them')
        extract_foldername = filename_tiff[0:-4]
        renaming_name = filename_tiff[-29:-14]
        imagery_location = output+'/'+extract_foldername+'/imagery/'
        allfiles = os.listdir(imagery_location)

        for f in allfiles:
            src_path = os.path.join(imagery_location, f)
            dst_path = os.path.join(folder, renaming_name+'_'+f)
            #dst_path = os.path.join(folder, f)
            #can I rename the file here too?
            os.rename(src_path, dst_path)
            #shutil.copyfile Try this tomorrow

        ###shutil.rmtree(output)
        ### don't want to do this because then I can't check if it exists



########

### Need to grab the filename that falls within lat/lon
### Read name, convert to number, make sure it isn't higher/lower? All above 50 deg N
### It might already be boxing itself...
#    lat_check = int(filemap[49:51])
#    lon_eastorwest = filemap[47]
#    long_check = int(filemap[41:44])
#    if lat_check > 50 and lon_eastorwest == "E":
#        lon_E = int(filemap[41:44])
#        if lon_E > 180
#        print(filemap[41:44])





