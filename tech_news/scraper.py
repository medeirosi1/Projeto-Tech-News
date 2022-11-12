import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    header = {"user-agent": "Fake user-agent"}
    try:
        response = requests.get(url, headers=header, timeout=1)
        response.raise_for_status()
        time.sleep(1)
    except (requests.HTTPError, requests.ConnectionError, requests.Timeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    # return selector.css(".cs-overlay a::attr(href)").getall()
    return selector.css(".cs-overlay-link::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css(".next::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".entry-title::text").get()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".url.fn.n::text").get()
    comments_count = selector.css("h5.title-block::text").re_first(r"\d+")
    summary = selector.css(".entry-content > p:nth-of-type(1) ::text").getall()
    tags = selector.css("a[rel=tag]::text").getall()
    category = selector.css(".label::text").get()

    return {
        "url": url,
        "title": title.strip(),
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": int(comments_count) if comments_count else 0,
        "summary": "".join(summary).strip(),
        "tags": tags,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    htlm_content = fetch("https://blog.betrybe.com")
    news_url = scrape_novidades(htlm_content)
    next = scrape_next_page_link(htlm_content)
    news_list = []

    while len(news_list) < amount:
        for url in news_url:
            news_list.append(scrape_noticia(fetch(url)))
            if len(news_list) == amount:
                break
        htlm_content = fetch(next)
        news_url = scrape_novidades(htlm_content)
        next = scrape_next_page_link(htlm_content)

    create_news(news_list)
    return news_list
