# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Visit the Mars NASA news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up the HTML parses
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try: 
        # Create parent element
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# # Scrape Mars Data: Featured Image

def featured_image(browser):
    # Visit the URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with Soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# # Scrape Mars Data: Mars Facts

def mars_facts():
    # Add try/except error handling
    try:
        # use pandas 'read_html' to scrape the facts into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException: # BaseException because pandas read_html is used instead of BS and splinter
        return None
    
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    return df.to_html()

browser.quit()