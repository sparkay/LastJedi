#############################################################
## Run the code for RT
import RTfuns

#load libraries
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re
#get initial page
r = urllib.request.urlopen('https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page=1&type=user').read()
soup = BeautifulSoup(r, "html5lib")

#get maximum pages
maxpage = re.findall("[0-9]+$", soup.body.find('span', class_="pageInfo").string)[0]
print("Total pages: {}". format(maxpage))
	
#go! - test with small num
maxpage = 52
reviewtbl = pd.concat([RTfuns.rt_iterator(pgnum) for pgnum in range(1, int(maxpage)+1)], ignore_index=True)

#check results
print(reviewtbl.shape)
print(reviewtbl.tail()) #shoot, I think this messed up b/c I forgot to ignore index - well, actually later pages apear to be blank

#save file so we don't have to do this again
import os
os.getcwd()
date = pd.to_datetime('today')
#reviewtbl.to_pickle("RT_Last_Jedi_{}-{}-{}.pkl".format(date.year, date.month, date.day)) #that didn't seem to work
reviewtbl.to_csv("RT_Last_Jedi_{}-{}-{}.txt".format(date.year, date.month, date.day), index=False, sep='\t') #and this one is missing

### Get Audience Score: % rating 3.5 or higher
score = sum([1 if score>=3.5 else 0 for score in reviewtbl["rating"]])/len(reviewtbl)
print("data has a mean rating of {:.1f} and a score of {:.0f}%".format(reviewtbl["rating"].mean(), score*100))