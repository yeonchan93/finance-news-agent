import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class FinancialNewsScraper:
    def __init__(self):
        self.us_url = "https://finance.yahoo.com/news/"
        self.jp_url = "https://japannews.yomiuri.co.jp/business/economy/"
        self.kr_url = "https://news.mt.co.kr/newsList.html?comd=7&pDepth=stock&pDepth1=sNews&pDepth2=Ftotal"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def scrape_us_articles(self) -> List[Dict]:
        """Scrape financial news articles from Yahoo Finance"""
        response = requests.get(self.us_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        for heading in soup.find_all('h3', class_='clamp yf-1y7058a'):
            title = heading.get_text(strip=True)
            summary = None
            next_elem = heading.find_next_sibling()
            while next_elem:
                if next_elem.name == 'p':
                    summary = next_elem.get_text(strip=True)
                    break
                next_elem = next_elem.find_next_sibling()
            if title:
                articles.append(
                    {
                        'title': title,
                        'summary': summary,
                    }
                )
        return articles
    
    def scrape_jp_articles(self) -> List[Dict]:
        """Scrape financial news articles from Yomiuri Shimbun"""
        response = requests.get(self.jp_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        for heading in soup.find_all('h2'):
            title = heading.get_text(strip=True)
            summary = None
            next_elem = heading.find_next_sibling()
            while next_elem:
                if next_elem.name == 'h3':
                    summary = next_elem.get_text(strip=True)
                    break
                next_elem = next_elem.find_next_sibling()
            if title:
                articles.append(
                    {
                        'title': title,
                        'summary': summary,
                    }
                )
        return articles
    
    def scrape_kr_articles(self) -> List[Dict]:
        """Scrape financial news articles from Money Today"""
        response = requests.get(self.kr_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        content = soup.find('ul', class_='conlist_p1')
        for heading in content.find_all('li', class_='bundle'):
            title_source = heading.find('strong', class_='subject')
            title = title_source.get_text(strip=True)
            summary_source = heading.find('p', class_='txt')
            summary = summary_source.get_text(strip=True)
            articles.append(
                {
                    'title': title,
                    'summary': summary,
                }
            )
        return articles
