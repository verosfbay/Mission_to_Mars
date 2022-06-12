# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Connect to MongoDB
def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemispheres(browser),
      "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Visit the mars nasa news site
def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
    # begin scraping
        slide_elem.find('div', class_='content_title')
    # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    return news_title, news_p

# ### Featured Images

# Visit URL
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

   try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
   except BaseException:
        return None
    # Assign columns and set index of dataframe
   df.columns=['description', 'Mars', 'Earth']
   df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
   return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Parse the resulting html with soup
    hemisphere_html = browser.html
    hemisphere_soup = soup(hemisphere_html, 'html.parser')
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # Retrieve all items for hemispheres information
    items = hemisphere_soup.find_all('div', class_='item')

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    main_url = "https://astrogeology.usgs.gov/"

    # Create loop to scrape through all hemisphere information
    for item in range(4):
        # Create the hemisphere dictionary
        hemispheres = {}
        
        # Find the hemisphere pages and click
        browser.find_by_css('h3')[item].click()
        
        # Find the image link by 'Sample'
        sphere = browser.links.find_by_text('Sample')
        img_url = sphere['href'] 
        
        # Find the titles
        title = browser.find_by_css('h2.title').text
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title
        
        # Append the hemisphere data list
        hemisphere_image_urls.append(hemispheres)
        
        # Go back, do it again
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())





