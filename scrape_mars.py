#imports
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#scrape all function
def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
   #the goal is to returen a json that has all of the neccessary data, so that it 
   # can be loaded into MongoDB

   #get the information from the news page
    news_title, news_paragraph = scrape_news(browser)

    #build a dictionry using the information from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

   #stop the webdriver
    browser.quit()

    #display output
    return marsData

#scrape the mars news page
def scrape_news(browser):
    # go to the Mars NASA news site
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    # grabs the title 
    news_title = slide_elem.find('div', class_='content_title').get_text()
    # grabs the paragraph for the headline
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # browser.is_element_present_by_css('div.list_text', wait_time = 1)
    return news_title, news_p


#scrape throug the featured image page
def scrape_feature_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the img url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


#scrape through the facts page
def scrape_facts_page(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #find the fact location 
    factsLocation = fact_soup.find('div', class_= "diagram mt-4")
    factTable = factsLocation.find('table') #grab the html cod for the fact table

    #create an empty string
    facts = ""

    #add the text to the empty string then return
    facts += str(factTable)

    return facts


#scrape through the hemispheres page
def scrape_hemispheres(browser):
    # base url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # set up the loop
    for i in range(4):
        # loop  through each of the pages
        #hemisphere info dictionary
        hemisphereInfo = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']
        
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
        
        # Finally, we navigate backwards
        browser.back()

    # return the hemisphere urls with the titles
    return hemisphere_image_urls


#set up as a flask app
if __name__ == "__main__":
    print(scrape_all())
