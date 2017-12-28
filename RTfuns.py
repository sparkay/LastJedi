
# coding: utf-8

# # Analyzing Last Jedi Reviews
# What are reviewers really saying about The Last Jedi? Is it all anti-progressives? How many negative reviews are responding to the treatment of Luke? To find out, this notebook scrapes user reviews for The Last Jedi from Rotten Tomatoes and does some basic text analysis.
print("loading functions for processing Rotten Tomatoes Last Jedi user reviews")
#load libraries
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re

#####################################
## FUNCTIONS
def get_user(mytag): #expects a review_table_row div container
    idtag = mytag.find_all(href=re.compile("user/id"))[-1] #get the last user id box
    userid = re.findall("[0-9]+", idtag['href'])
    userid.append([string for string in idtag.stripped_strings])
    return userid #figure out how to sort this tupple later

#count stars and get rating
def get_rating(mytag): #expects a review_table_row div container
    whole_stars = mytag.find_all(class_ = "glyphicon-star")
    #see if there is a half star at the end
    if len(whole_stars)>0:
        half_star = whole_stars[-1].next_sibling
    else:
        half_star = 1 #if whole_stars is 0 then the rating must be a half star
    return len(whole_stars) + (0.5 if half_star is not None else 0)

#get review text
def get_review_text(mytag):
    review_text = mytag.find('div', class_="user_review") #I hope there's only one
    return [string for string in review_text.stripped_strings]

def reviewtbl_constructor(mytag):
    tmp = get_user(mytag)
    tmp.append(get_rating(mytag))
    tmp.append(get_review_text(mytag))
    return tmp

#now iterate through the pages and get everything - muahahaha!
def rt_iterator(pagenum):
    print('processing page {}'.format(pagenum)) #slows things down, but useful for debugging
    #open page
    r = urllib.request.urlopen("https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page={}&type=user".format(pagenum)).read()
    soup = BeautifulSoup(r, "html5lib")
    
    #find the review block
    reviews = soup.body.find_all('div', class_="review_table_row") #returns a list of tags
    
    #check if empty
    if len(reviews) == 0:
        print("reviews is empty")

    #extract info
    return pd.DataFrame([reviewtbl_constructor(x) for x in reviews], columns = ["userid", "username", "rating", "text"])