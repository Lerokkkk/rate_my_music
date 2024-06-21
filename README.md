# Rate My Music
---
Rate My Music is a Django web application that allows you to rate musical compositions. Administrators and registered users can add artists and tracks. Added object users are moderated by the administrator before publication.

# Technologies Used:
- Django
- HTML
- CSS
- JavaScript
- SQLite
- django-haystack: modular search for Django
- Whoosh: full-text indexing and searching

Functional
---
- Evaluation of musical compositions
- Adding songs and musicians
- Moderation of objects
- Site search 
- Showing the best composition and the newest composition on the main page

# Installation:
## 1. Cloning a repository

`https://github.com/Lerokkkk/rate_my_music.git`

`CD rate my music`
## 2. Create Virtual Environment:
`python -m venv venv`
## 3. Activate Virtual Environment:
`venv\Scripts\activate`
## 4.Install Dependcies:
`pip install -r requirements.txt`
## 5. Run Migrations:
`python manage.py migrate`
## 6.Create Superuser:
`python manage.py createsuperuser`
## 7. Run server:
`python manage.py runserver`
