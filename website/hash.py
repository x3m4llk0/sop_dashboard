import os
import random
import string
import django
from django.conf import settings
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  # Замените "myproject.settings" на имя вашего модуля настроек Django
django.setup()

def django_hash(text):
    hashed_text = make_password(text)
    return hashed_text

new_password = ''

for x in range(10): #Количество символов (16)
    new_password = new_password + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))

# Генерируем случайный пароль
hashed_text = django_hash(new_password)

print("Транспортный пароль:", new_password)
# Выводим хэш пароля
print("Хэш:", hashed_text)