#import dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrapeall(): 
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)
	news_title, news_paragraph = news(browser)
	featured_image_url = feature(browser)
	html_table = table()
	hemisphere_image_urls = hem(browser)

	return {
	        'latestheadline': news_title,
	        'latestparagraph':  news_paragraph,
	        'featuredimage': featured_image_url,
	        'marsfacts': html_table,
	        'hemispheres': hemisphere_image_urls,
	    }

def news(browser):
	url = "https://mars.nasa.gov/news/"
	browser.visit(url)
	html = browser.html
	news_soup = bs(html, "html.parser")
	slide_element = news_soup.select_one("ul.item_list li.slide")
	slide_element.find("div", class_="content_title")
	news_title = slide_element.find("div", class_="content_title").get_text()
	news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
	return news_title, news_paragraph

def feature(browser):
	featured_url = "https://spaceimages-mars.com/"
	browser.visit(featured_url)
	browser.click_link_by_partial_text('FULL IMAGE')
	bigimage_html = browser.html
	bigimage_soup = bs(bigimage_html, 'html.parser')
	bigimage = bigimage_soup.body.find(class_ = 'headerimage fade-in')
	bigimage_img = bigimage['src']
	bigimage_base_url = 'https://spaceimages-mars.com/'
	featured_image_url = bigimage_base_url + bigimage_img
	return featured_image_url

def table():
	mars_facts = pd.read_html("https://galaxyfacts-mars.com/")
	mars_df = mars_facts[0]
	header_row = 0
	mars_df.columns = mars_df.iloc[header_row]
	mars_df = mars_df.drop(header_row)
	html_table = mars_df.to_html()
	return html_table


def hem(browser):
	mars_hemispheres_url = "https://marshemispheres.com/"
	browser.visit(mars_hemispheres_url)
	hemisphere_image_urls = []
	for i in range (4):
	    browser.find_by_tag('h3')[i].click()
		hemispheres_html = browser.html
		hem_soup = bs(hemispheres_html, 'html.parser')
		hem = hem_soup.body.find('img', class_ = 'wide-image')
		hem_img = hem['src']
		title = hem_soup.find('h2', class_ = 'title').get_text()
		hem_base_url = 'https://marshemispheres.com/'
		hem_url = hem_base_url + hem_img
		hem_dict = {"title": title, "img_url": hem_url}
		hemisphere_image_urls.append(hem_dict)
		browser.back()
	return hemisphere_image_urls	




	

