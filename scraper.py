import requests
from bs4 import BeautifulSoup
import logging
from database import create_database, save_to_database, fetch_all_headlines

logging.basicConfig(level=logging.DEBUG)


def get_response():
    url = 'https://www.handballisr.co.il/'  # The website to scrape
    response = requests.get(url)  # Sends GET request
    if response.status_code != 200:
        logging.error(f"Response Error: {response.status_code}")
        return None
    logging.info("Request successful")
    return response


# will scrape all the news on the home page of Handballisr websites
def scrape_sports_news():
    response = get_response()
    if not response:
        return

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_heads = soup.find_all('a', tabindex=True)

    seen_headlines = set(fetch_all_headlines())

    for head in articles_heads:
        headline_tag = head.find('h2')
        if not headline_tag:
            continue
        headline = headline_tag.get_text(strip=True)
        if headline in seen_headlines:
            logging.error(f"Article already in database: {headline}")
            continue

        article_url = head.get('href')
        if not article_url.startswith('http'):
            article_url = 'https://www.handballisr.co.il/' + article_url

        article_summary = scrape_summary_from_url(article_url)
        save_to_database(headline, article_summary, article_url)


# to scrape an article summary from the page the url from the base websites lead to
def scrape_summary_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Article not available"
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    summary_tag = soup.find('h2')
    return summary_tag.get_text(strip=True) if summary_tag else "No summary available"


if __name__ == '__main__':
    create_database()
    scrape_sports_news()
