# BattlemapSearcher-Flask

## Overview

BattlemapSearcher-Flask is a single page application designed to search for battlemaps.

![BattlemapsSearcher](https://raw.githubusercontent.com/miki4920/BattlemapSearcher-Flask/main/BattlemapsSearcher.gif)

The project is divided into two main parts:

1. **Web Scraper**: This part of the project is responsible for scraping Reddit according to specified subreddits. The main script for this part is `main.py` located in the `webscrapper` folder.

2. **Website**: This part of the project is a search engine for the maps scraped by the web scraper. The main script for this part is `app.py`.

Both parts of the project require pipenv to run.

## Setup

### Prerequisites

- Python 3.10 or higher
- Pipenv

### Environment Variables

The following environment variables are required to run the project:

- `IP`: IP of the database (MySQL by default, however change can be made in config)
- `USERNAME`: Database account username
- `PASSWORD`: Database account password
- `SCHEMA_NAME`: Name of the database schema

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/miki4920/BattlemapSearcher-Flask.git
    ```

2. Navigate to the project directory:
    ```bash
    cd BattlemapSearcher-Flask
    ```

3. Install the project dependencies using pipenv:
    ```bash
    pipenv install
    ```

4. Set the required environment variables.

5. Run the web scraper:
    ```bash
    pipenv run python webscrapper/main.py
    ```

6. Run the website:
    ```bash
    pipenv run python app.py
    ```

## Usage

After setting up the project, you can use the website to search for battlemaps. The web scraper will periodically scrape Reddit for new maps according to the specified subreddits. Warning, the API used is pushshift.io, which has a tendency to not work.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.
