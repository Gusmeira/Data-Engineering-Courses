import requests as r
from bs4 import BeautifulSoup
import re
import pandas as pd

response = r.get('https://books.toscrape.com/')
print('Status:', response, '\n')
soup = BeautifulSoup(response.content, 'html.parser')

book_tags = soup.find_all('article', attrs={'class':'product_pod'})
# print(book_tags)

def extract_book_data(book_tag):
    title = book_tag.find('h3').find('a')['title']

    def price_num(price):
        return float(re.sub(r'[^0-9.]', '', price))
    price = book_tag.find('p', attrs={'class':'price_color'}).text
    price = price_num(price)

    def rating_map(rating):
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5,
        }
        return rating_map[rating]
    rating = book_tag.find('p', attrs={'class':'star-rating'})['class'][1]
    rating = rating_map(rating)

    return {
        'title': title,
        'price': price,
        'rating': rating
    }

book_data = [extract_book_data(book_tag) for book_tag in book_tags]
df = pd.DataFrame(book_data)
df.to_json('Projects/Books_API.json' ,orient='records', indent=2)