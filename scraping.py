# Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    } 

    # Stop webdriver and return data
    browser.quit()
    return data

# # Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver'}
# browser = Browser('chrome', **executable_path)

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
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
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

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())