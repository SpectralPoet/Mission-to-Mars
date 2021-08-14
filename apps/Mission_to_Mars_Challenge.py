# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import re

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# # 3. Write code to retrieve the image urls and titles for each hemisphere.

# Convert the browser html to a soup object and then quit the browser
html = browser.html
jpgs0_soup = soup(html, 'html.parser')

# we need to navigate to a different url for each of these images to get the full size image;
# this is the tag and class of those hrefs
itemLinks = jpgs0_soup.findAll('a', class_="itemLink product-item")

# of the matching items returned, these are the 4 we want
itemLinks_clean = [itemLinks[0], itemLinks[2], itemLinks[4], itemLinks[6]]

# let's get these items as string
items_as_string = []
for each in itemLinks_clean:
    items_as_string.append(str(each))

# now we want just the href, using regex
pattern = 'href="(.*)">'

# and we'll store them in a list
nested_urls = []

# then apply the pattern to each string
for each in items_as_string:
    nested_urls.append(re.search(pattern, each).groups([0]))

#clean up some formatting
nested_urls_clean = []
for each in nested_urls:
    nested_urls_clean.append(each[0])

#let's make 2 lists to hold our results
image_urls_list = []
titles_list = []

# for each in etc.
for each in nested_urls_clean:

    # visit our urls to scrape from
    url = f'https://marshemispheres.com/{each}'
    browser.visit(url)
    html = browser.html
    jpgs1_soup = soup(html, 'html.parser')

    # append the image url in this page into the images list
    images = jpgs1_soup.findAll('a', target="_blank")
    image_urls_list.append(str(images[2]))

    # append the title from the page into the title list
    titles_list.append(jpgs1_soup.findAll('h2', class_="title"))


# useful global variables
image_urls_succinct = []
urls_list_clean = []
i=0

# clean and format image urls list
for each in image_urls_list:

    pattern = 'href="(.*)"\s'
    image_urls_succinct.append(re.search(pattern, each).groups([0]))
    urls_list_clean.append(image_urls_succinct[i][0])
    i+=1


# useful global variables
titles_succinct = []
titles_clean = []
i = 0

##clean and format titles list
for each in titles_list:

    pattern = '>(.*)<'
    titles_succinct.append(re.search(pattern, str(each)).groups([0]))
    titles_clean.append(titles_succinct[i][0])
    i+=1

# reset base url
url = 'https://marshemispheres.com/'


# create the dicts using the scraped data
cerberus_dict = {'img_url': f'{url}{urls_list_clean[0]}', 'title': f'{titles_clean[0]}'}
schiaparelli_dict = {'img_url': f'{url}{urls_list_clean[1]}', 'title': f'{titles_clean[1]}'}
syrtis_major_dict = {'img_url': f'{url}{urls_list_clean[2]}', 'title': f'{titles_clean[2]}'}
valles_marineris_dict = {'img_url': f'{url}{urls_list_clean[3]}', 'title': f'{titles_clean[3]}'}

hemisphere_image_urls = [cerberus_dict, schiaparelli_dict, syrtis_major_dict, valles_marineris_dict]

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

