import requests as req
from bs4 import BeautifulSoup as bs
from ..models import Article

from . import tts

list_of_categories = [
	"https://www.salom.com.tr/haberler/50/artionsekiz",
	"https://www.salom.com.tr/haberler/24/genclik-egitim",
	"https://www.salom.com.tr/haberler/7/kultur",
	"https://www.salom.com.tr/haberler/17/judeo-espanyol",
	"https://www.salom.com.tr/haberler/6/spor",
	"https://www.salom.com.tr/haberler/35/cocuk-aile",
	"https://www.salom.com.tr/haberler/26/saglik",
	"https://www.salom.com.tr/haberler/4/ekonomi",
	"https://www.salom.com.tr/haberler/8/perspektif",
	"https://www.salom.com.tr/haberler/14/kavram",
	"https://www.salom.com.tr/haberler/36/sanat",
	"https://www.salom.com.tr/haberler/5/yasam",
	"https://www.salom.com.tr/haberler/16/toplum",
	"https://www.salom.com.tr/haberler/15/dunya"
]

def save_article(link: str, category : str) -> None:
	print("Saving:", link)
	# Get page and turn into soup
	response = req.get(link)
	soup = bs(response.content, "html.parser")

	# Title of the article
	title = str(soup.find("h1", {"class": "hbr-dty-bslk mtop15 mbot15"}).text)

	# Paragraphs turned into a multi-line strings
	paragraphs = soup.find("div", {"class": "col-md-12 mbot15 hicerikdty"}).find_all("p")
	text = """"""
	for para in paragraphs:
		if len(para.text) > 5:
			text = text + str(para.text)
			text = text + "\n"

	# TTS voice file
	voice_file = tts.to_voice(text, title)

	# Create Article object and save it
	article = Article()
	article.title = title
	article.text = text
	article.link = link
	article.category = category
	article.voice_file = voice_file
	article.news_caster = "salom"	# This line is only true for salom web crawler.
	article.save()

def get_article_links(html_content) -> list:
	# Make soup and get articles which is where news blocks reside in
	soup = bs(html_content, "html.parser")
	articles = soup.find_all("article")

	article_links = []
	for article in articles:
		# Each article has 3 copies of the same link get the link of the first one
		article_links.append(str(article.find_all("a")[0]["href"]))
	
	return article_links

def crawl() -> None:
	# Go through all categories
	for category_link in list_of_categories:
		# Last crawled article from category
		category = category_link.split("/")[-1]
		latest_article = Article.objects.filter(category = category).order_by("creation_date").reverse().first()

		# New links to be crawled
		article_links = []

		# Up to 15 pages exists per category
		for page in range(1, 15):
			response = req.get(category_link + "?page=" + str(page))

			# If page exists, get article links
			links = get_article_links(response.content)

			# Only crawl until last crawled article
			break_flag = False
			if latest_article and latest_article.link in links:
				links = links[:links.index(latest_article.link)]
				break_flag = True
			
			# Add new links to the list
			article_links.extend(links)

			# Early exit when we have reached the latest article of category
			if break_flag:
				print("Reached previous news of " + category + ".")
				break
		
		# Get each article and save them in DB
		for link in article_links[::-1]:
			save_article(link, category)
