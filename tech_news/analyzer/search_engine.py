from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    dict_list = search_news({"title": {"$regex": title, "$options": "i"}})
    return [(news["title"], news["url"]) for news in dict_list]


# Requisito 7
def search_by_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        date_formated = date.strftime("%d/%m/%Y")
        dict_list = search_news({"timestamp": date_formated})
        return [(news["title"], news["url"]) for news in dict_list]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    dict_list = search_news({"tags": {"$regex": tag, "$options": "i"}})
    return [(news["title"], news["url"]) for news in dict_list]


# Requisito 9
def search_by_category(category):
    dic_list = search_news({"category": {"$regex": category, "$options": "i"}})
    return [(news["title"], news["url"]) for news in dic_list]
