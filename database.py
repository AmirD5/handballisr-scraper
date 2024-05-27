import sqlite3
import logging

logging.basicConfig(level=logging.INFO)


# connection to sqlite3 to the db
def connect_to_db():
    conn = sqlite3.connect('sports_news.db')
    conn.execute("PRAGMA encoding = 'UTF-8'")
    c = conn.cursor()
    return c, conn


# creating a table called articles for the scraping
def create_database():
    c, conn = connect_to_db()
    c.execute('CREATE TABLE IF NOT EXISTS articles (headline TEXT, summary TEXT, url TEXT)')
    conn.commit()
    conn.close()
    logging.info("Database and table created successfully.")


# saves information scraped from the website into the db
def save_to_database(headline, summary, url):
    c, conn = connect_to_db()
    c.execute("INSERT INTO articles (headline, summary, url) VALUES (?, ?, ?)",
              (headline, summary, url))
    conn.commit()
    conn.close()
    logging.info(f"Saved article: {headline}")


# returns all the articles
def fetch_all_articles():
    c, conn = connect_to_db()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()
    return articles


# returns a specific headline from the table
def fetch_article_by_headline(headline):
    c, conn = connect_to_db()
    c.execute("SELECT * FROM articles WHERE headline=?", (headline,))
    article = c.fetchone()
    conn.close()
    return article


# returns all the headlines from the table
def fetch_all_headlines():
    c, conn = connect_to_db()
    c.execute("SELECT headline FROM articles")
    headlines = [row[0] for row in c.fetchall()]
    conn.close()
    return headlines


if __name__ == '__main__':
    create_database()
    # Example to fetch all articles
    articles = fetch_all_articles()
    for article in articles:
        print(article)
        print('\n')
