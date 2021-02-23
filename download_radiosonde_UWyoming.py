# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# supress warnings
import warnings
warnings.filterwarnings('ignore') # don't output warnings

# import packages
from imports import (np, urllib3, BeautifulSoup, fct)

# reload imports
# %load_ext autoreload
# %autoreload 2



# +
stn = '01415' #1415 is ID for Stavanger


fct.createFolder('/home/franzihe/Documents/Data/Sounding/{}'.format(stn)) # for text files
# -

m = [#'12','01', 
     '02']
h = [#'00', 
    '12']

for month in m:
    if month == '12':
        t = np.array([8, 9, 10, 12, 15, 20, 21, 22, 23, 24, 25, 26, 29, 31])
    if month == '01':
        t = np.array([2, 3, 5, 6, 8, 9, 10, 11, 12, 28])
    if month == '02':
        t = np.array([2, 3, 4])    
    if month == '12':
        year = '2016'
    if month == '01' or month == '02':
        year = '2017'
    for day in t:
        if day < 10:
            day = '0%s' %day
        
        for hour in h:
            

            # 1) 
            # Wyoming URL to download Sounding from
            url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+str(day)+hour+'&TO='+str(day)+hour+'&STNM='+stn


            #2)
            # Remove the html tags
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data.decode('utf-8'),'lxml')
            data_text = soup.get_text()

            # 3)
            # Split the content by new line.
            splitted = data_text.split("\n",data_text.count("\n"))


            # 4)
            # Write this splitted text to a .txt document
            Sounding_filename = '/home/franzihe/Documents/Data/Sounding/{}/{}{}{}_{}.txt'.format(stn,year,month,day,hour)
            f = open(Sounding_filename,'w')
            for line in splitted[4:]:
                f.write(line+'\n')
            f.close()
            
            print('file written: {}'.format(Sounding_filename))
