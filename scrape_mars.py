import numpy as np
import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import regex as re
import time

def openBrowser():
    executable_path = {'executable_path': '../chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    time.sleep(1)

#------------------------------------------------


def closeBrowser(browser):
    browser.quit()
    time.sleep(1)

#------------------------------------------------

def scrape():

    mars_data = {}

    mars_data["news_data"] = marsNews()

    mars_data["featured_image_url"] = marsFeaturedImage()

    mars_data["mars_weather"] = marsWeather()

    mars_data["mars_facts"] = marsFacts()

    mars_data["mars_hemispheres"] = marsHemispheres()

    return mars_data

#------------------------------------------------


def marsNews():

    browser = openBrowser()
    time.sleep(2)

    nasa_news_url = "https://mars.nasa.gov/news/"
    nasa_site = "https://mars.nasa.gov" 
    
    p_text = []
    news = {}

    # Navigate splinter/chrome browser to news url and zap the html into BS!
    browser.visit(nasa_news_url)
    time.sleep(1)
    news1_html = browser.html
    time.sleep(1)
    soup = bs(news1_html, 'html.parser')
    
    article1 = soup.find(class_="slide")
    article = article1.find_all('a')
    news_p = article[0].get_text().strip()
    news_title = article[1].get_text().strip()

    p_soup = article1.find_all('a', href=True)  
    url_p = p_soup[0]['href']
    url_link = nasa_site + url_p

    response2 = requests.get(url_link) 
    time.sleep(1)                                         
    paragraph_soup = bs(response2.text, "html.parser")                         
    html_paragraphs = paragraph_soup.find(class_='wysiwyg_content')           
    paragraphs = html_paragraphs.find_all('p')

    p_header = paragraphs[0].get_text().strip()
    p_intro = paragraphs[2].get_text().strip()

    news["newsTitle"] = news_title
    news['newsHeader'] = p_header
    news['newsIntro'] = p_intro

    closeBrowser(browser)

    return news

#------------------------------------------------

def marsFeaturedImage():

    browser = openBrowser()

    featured_image_array = []

    mars_pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mars_hd = "https://www.jpl.nasa.gov/spaceimages/"
    browser.visit(mars_pic_url)
    time.sleep(1)
    mars_pic_html = browser.html
    time.sleep(1)
    mars_pic_soup = bs(mars_pic_html, 'html.parser')
    time.sleep(1)
    mars_images = mars_pic_soup.find_all('div',class_="img")                                                   

    for image in mars_images:                        
        featured_image_array.append(image.find('img').get('src')) 

    featured_image = featured_image_array[0]
    t_1 = featured_image.split('-')                                       
    t_2 = t_1[0].split('/')                                     
    featured_image_url = mars_hd + "images/largesize/" + t_2[-1] + '_hires.jpg'

    closeBrowser(browser)

    return featured_image_url

#------------------------------------------------


def marsWeather():

    browser = openBrowser()

    weather_list = []
    mars_weather_posts = []

    mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather)
    time.sleep(1)
    weather_html = browser.html
    time.sleep(1)
    weather_soup = bs(weather_html, 'html.parser')
    time.sleep(1)
    mars_posts = weather_soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    for posts in mars_posts:
        weather_list.append(posts.text.strip())

    for x in weather_list:
        if re.search('Sol', x):
            mars_weather_posts.append(x)

    recent_mars_weather = mars_weather_posts[0]

    closeBrowser(browser)

    return recent_mars_weather

#------------------------------------------------

def marsFacts():

    data_url = "https://space-facts.com/mars/"
    table = pd.read_html(data_url)
    time.sleep(1)
    clean_table = table[0]
    clean_table.columns = ['Data', 'Values']
    mars_table_html = clean_table.to_html(header=False, index=False)
    mars_table_html.replace('\n', '')

    return mars_table_html

#------------------------------------------------

def marsHemispheres():

    browser = openBrowser()

    hemisphere_image_urls = []

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(1)
    hemi_html = browser.html
    time.sleep(1)
    hemi_soup = bs(hemi_html, 'html.parser')
    time.sleep(1)
    soup_results = hemi_soup.find('div', class_='result-list')                     
    hemispheres = soup_results.find_all('div', class_='item')                       

    for hemisphere in hemispheres:

        hemi = hemisphere.find('div', class_='description')
        title = hemi.a.text
        title = title.replace('Enhanced', '')
        browser.click_link_by_partial_text(title)
    
        asc_html = browser.html 
        time.sleep(1)                                               
        asc_soup = bs(asc_html, 'html.parser')                                 
        time.sleep(1)
        image = asc_soup.find('div', class_='downloads').find('ul').find('li')  
        image_url = image.a['href']
    
        hemisphere_image_urls.append({'title': title, 'image_url': image_url})   
    
        browser.click_link_by_partial_text('Back') 

    closeBrowser(browser)

    return hemisphere_image_urls


#------------------------------------------------


if __name__ == "__main__":
    print(scrape())