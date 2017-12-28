#scratch for Rotten Tomatoes project


# In[203]:


#test out basic page fetching
r = urllib.request.urlopen('https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page=1&type=user').read()
soup = BeautifulSoup(r, "html5lib")
print(soup.prettify()[0:1000])


# In[209]:


#find the reviews
reviews = soup.body.find_all('div', class_="review_table_row") #returns a list of tags

#the stripped_strings approach seems to get the review text itself
for string in reviews[1].stripped_strings:
    print(repr(string))

#reviews[0].previous_sibling


reviewtbl = pd.DataFrame([reviewtbl_constructor(x) for x in reviews], columns = ["userid", "username", "rating", "text"])
reviewtbl


#put it all together - there should be a way to do this in one loop (See above)
reviewtbl = pd.DataFrame([get_user(x) for x in reviews], columns=["userid", "username"])
reviewtbl["rating"] = [get_rating(x) for x in reviews]
reviewtbl["review text"] = [get_review_text(x) for x in reviews]
reviewtbl


# In[208]:


#scratch cell
usertag = reviews[0].find_all(href=re.compile("user/id"))
print(usertag)
for string in usertag.stripped_strings:
    print(repr(string))


# In[83]:


#test grab rows and extract info

reviews = soup.body.find_all('div', class_="row review_table_row") #returns a list of tags
print(reviews[9].prettify())


