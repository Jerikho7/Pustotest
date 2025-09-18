# 📬 Игровой сервис

## 📌 Описание проекта

#### Веб-приложение для логирования играков, получения поинтов и бустов за вхождение. Получение призов при прохождении уровней игры. Выгрузка в csv данных игроков.

#### Условия тестового: https://axiomatic-mine-6ba.notion.site/Python-916c8e3d5d6c4006b4b83a0081dc03a8

#### Автор: Осипова Евгения Юрьевна.

---

## 🚀 Запуск проекта (локально)  
  
1. Клонировать репозиторий:  
   ```bash  
   git clone https://github.com/Jerikho7/Pustotest.git
   cd pustotest

2. Установка Poetry и зависимостей.
  ```bash
  pip install poetry
  ```
Затем:  
  ```bash    
  poetry install.
  ```
3. Активация виртуального окружения
```bash
poetry shell  
```  
4. Применение миграций и создание администратора  
```bash  
python manage.py migrate

```
5. Запуск проекта  
```bash
python manage.py runserver  
```



