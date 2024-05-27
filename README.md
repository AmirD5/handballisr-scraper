# HandballISR Scraper

This project scrapes sports news from the Handball Israel website and stores it in a SQLite database.

## Project Structure

- `scraper.py`: Scrapes sports news articles from the Handball Israel website.
- `database.py`: Manages the SQLite database operations (creation, insertion, retrieval).
- `test_scraper.py`: Contains tests for `scraper.py` using `pytest`.
- `test_database.py`: Contains tests for `database.py` using `pytest`.

## Requirements

- Python3
- `requests` library
- `beautifulsoup4` library
- `pytest` library for running tests

## Setup

 **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/handballisr_scraper.git
   cd handballisr_scraper
