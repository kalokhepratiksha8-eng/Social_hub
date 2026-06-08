# SnapGram — Mini Instagram
A full-stack Instagram clone built with Django + MySQL.

## Features
- 📸 Photo posts with captions
- 💬 Comments on posts
- ❤️ Like / unlike posts
- 👥 Follow / unfollow users
- 📖 Story bar on feed
- 🔍 Explore & search users
- 🔔 Notifications (likes, comments, follows)
- 👤 User profiles with bio, avatar, location
- 📱 Mobile-first responsive design

## Tech Stack
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)

---

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip

### 2. Install MySQL & create database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE snapgram_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'snapgram_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL ON snapgram_db.* TO 'snapgram_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Clone / unzip the project
```bash
cd snapgram/
```

### 4. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```
> **Note for Windows**: If `mysqlclient` fails, try:
> `pip install mysqlclient --only-binary=:all:`
> Or install MySQL Connector: `pip install mysql-connector-python` and change ENGINE in settings.py to `django.db.backends.mysql`

### 6. Configure database
Edit `backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'snapgram_db',
        'USER': 'root',           # ← your MySQL user
        'PASSWORD': 'your_password',  # ← your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 7. Run migrations
```bash
python manage.py migrate
```

### 8. Create superuser (for admin panel)
```bash
python manage.py createsuperuser
```

### 9. Run the server
```bash
python manage.py runserver
```

### 10. Open in browser
- **App**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

---

## Project Structure
```
snapgram/
├── backend/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                     # Main app
│   ├── models.py             # Profile, Post, Comment, Like, Follow, Story
│   ├── views.py              # Page views
│   ├── api_views.py          # REST API views
│   ├── urls.py               # Page URLs
│   ├── api_urls.py           # API URLs (/api/...)
│   └── admin.py
├── frontend/
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── feed.html
│   │   ├── profile.html
│   │   ├── post_detail.html
│   │   ├── explore.html
│   │   ├── notifications.html
│   │   ├── create_post.html
│   │   ├── edit_profile.html
│   │   ├── login.html
│   │   └── register.html
│   └── static/
│       ├── css/main.css
│       └── js/main.js
├── database/
│   └── schema.sql            # MySQL schema reference
├── manage.py
└── requirements.txt
```

## REST API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/feed/ | Authenticated user's feed |
| GET/POST | /api/posts/ | List all / create post |
| GET/DELETE | /api/posts/{id}/ | Get / delete post |
| GET/POST | /api/posts/{id}/comments/ | List / add comments |
| GET | /api/users/{username}/profile/ | Get user profile |

## Media Files
Uploaded images are stored in `/media/` directory:
- Avatars: `/media/avatars/`
- Post images: `/media/posts/`
- Stories: `/media/stories/`
