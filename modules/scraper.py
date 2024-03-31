from newspaper import Article
import sys

def scrape(url):
    article = Article(url)
    article.download()
    article.parse()
    
    date = article.publish_date
    authors = article.authors
    raw_article = article.text
    title = article.title
    
    return date, raw_article, title, authors
