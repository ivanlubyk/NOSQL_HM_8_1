
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from mongoengine import connect
import json
from models import Author, Quote

connect(host="mongodb+srv://web12_user:641641@cluster12.bopqszz.mongodb.net/?retryWrites=true&w=majority")

# Завантаження даних про авторів з JSON-файлів та збереження їх у базі даних

def load_authors_data():
    with open('my_data/authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            born_date = datetime.datetime.strptime(author_data['born_date'], '%B %d, %Y').date()
            author = Author(
                fullname=author_data['fullname'],
                born_date=born_date,
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

# Завантаження даних про цитати з JSON-файлів та збереження їх у базі даних
def load_quotes_data():
    with open('my_data/quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                tags = quote_data['tags']
                quote = Quote(
                    tags=tags,
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

# Пошук цитат за тегом, за ім'ям автора або набором тегів
def search_quotes():
    while True:
        command = input("Введіть команду (name: Автор, tag: Тег, tags: Тег1,Тег2, ..., exit для виходу): ")
        if command.startswith('name: '):
            author_name = command.split('name: ')[1]
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                print_quotes(quotes)
            else:
                print("Автор не знайдений")
        elif command.startswith('tag: '):
            tag = command.split('tag: ')[1]
            quotes = Quote.objects(tags__contains=tag)
            print_quotes(quotes)
        elif command.startswith('tags: '):
            tags = command.split('tags: ')[1].split(',')
            quotes = Quote.objects(tags__all=tags)
            print_quotes(quotes)
        elif command == 'exit':
            break
        else:
            print("Невідома команда!")

# Виведення цитат на екран
def print_quotes(quotes):
    print("Знайдені цитати:")
    for quote in quotes:
        print(f"Автор: {quote.author.fullname}")
        print(f"Цитата: {quote.quote}")
        print()

# Завантаження даних та пошук цитат
def main():
    load_authors_data()
    load_quotes_data()
    search_quotes()

if __name__ == '__main__':
    main()