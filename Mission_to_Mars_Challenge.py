# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the Mars NASA news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Set up the HTML parses
html = browser.html
news_soup = soup(html, 'html.parser')
# Create parent element
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
#news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
#news_p


# # Scrape Mars Data: Featured Image

# Visit the URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting HTML with Soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
#img_url


# # Scrape Mars Data: Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
#df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Scrape the page with soup
html_hemispheres = browser.html
html_soup = soup(html_hemispheres, 'html.parser')

# Retrieve container with necessary elements
items = html_soup.find_all('div', class_='description')
#items

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Create variable with main URL to concatenate with partial image link
main_url = 'https://astrogeology.usgs.gov'

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in items:
    img_url = i.find('a', class_='itemLink product-item')['href']
    title = i.find('h3').text
    browser.visit(main_url + img_url)
    img_html = browser.html
    img_soup = soup(img_html, 'html.parser')
    image_div = img_soup.find('div', class_='downloads')
    full_image = image_div.find('a')['href']
    hemisphere = {'title': title, 'img_url': full_image}
    hemisphere_image_urls.append(hemisphere)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

