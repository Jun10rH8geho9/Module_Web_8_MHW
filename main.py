from mongoengine import connect
from models import Author, Quote
import redis
import re
from redis_lru import RedisLRU
import sys

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
cache = RedisLRU(redis_client)

@cache
def search_quotes(command):

    # Перетворення скорочених команд name:st та tag:li у повні
    command = command.replace('name:', 'name:').replace('tag:', 'tag:')

    # Перевірка наявності результату у кеші Redis
    cached_result = redis_client.get(command)
    if cached_result:
        return cached_result.decode('utf-8').split(',')

    if command.startswith('name:'):
        author_name = command.split(':', 1)[1].strip()
        if len(author_name) == 2:
            author = Author.objects(fullname__istartswith=author_name).first()
        else:
            author = Author.objects(fullname__iregex=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            result = [quote.quote for quote in quotes]
            # Перевірка, чи відповідають дані в кеші поточному запиту
            if not cached_result or cached_result.decode('utf-8').split(',') != result:
                # Зберігання результату у кеші Redis
                redis_client.setex(command, 60, ','.join(result))
            return result
        else:
            return ["Цитат для автора не знайдено: {}".format(author_name)]
        
    elif command.startswith('tag:'):
        tag = command.split(':', 1)[1].strip()
        quotes = Quote.objects(tags__iregex=tag)
        result = [quote.quote for quote in quotes]
        # Зберігання результату у кеші Redis
        redis_client.setex(command, 60, ','.join(result))
        return result
    elif command == 'exit':
        sys.exit("Exiting...")
    else:
        return ["Неправильна команда.Використовуйте 'name:', 'tag:', 'tags:', or 'exit'."]

def main():
    connect(db='My_homework_DB', host="mongodb+srv://web_8MHW:oulGmMDL5ksPq6fz@hedgehog.rsn29se.mongodb.net/My_homework_DB?retryWrites=true&w=majority&appName=hedgehog")
    while True:
        # Треба ввести. Наприклад: name: Steve Martin або скорочений варіант name:st. З тегами так само
        command = input("Введіть команду(name/tag/tags):")
        result = search_quotes(command)
        for quote in result:
            print(quote)

if __name__ == "__main__":
    main()