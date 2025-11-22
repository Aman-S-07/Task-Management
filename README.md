# Task Management System (Django)

A full-featured **Task Management Web Application** built using Django.  
This project provides user authentication, OTP email verification, task creation, deadlines, attempts tracking, and a clean responsive UI.

---

## 🚀 Features

### ✅ Authentication & Security  
- User Registration with OTP Email Verification  
- Login / Logout  
- Strong password hashing  
- Profile update (image, number, name)  

### 🧑‍💻 Task Management  
- Create tasks  
- Edit tasks  
- Delete tasks  
- Attempts tracking  
- Re-attempt cycle  
- Task status workflow  

### 🎨 UI/UX  
- Custom responsive templates  
- Sidebar navigation  
- Profile dashboard  
- Toast messages for actions  

### ⚙ Tech Stack  
- **Backend:** Django 4.x  
- **Database:** SQLite  
- **Frontend:** HTML, CSS  
- **Server:** Django / Gunicorn  
- **Static Files:** Whitenoise  
- **Env Management:** python-dotenv, decouple  

---

## 📁 Project Structure
```
Task-Management/
│
├── Hello/ # Django project settings
├── home/ # Main app (models, views, forms)
├── templates/ # HTML UI
├── static/ # CSS, JS, images
├── media/ # User uploaded images
├── requirements.txt # Dependencies
├── manage.py

```

---

## 🔧 Installation & Setup (Local Machine)

Follow these steps to run the project locally:

---

### 1️⃣ Clone Repo

```
git clone https://github.com/Aman-S-07/Task-Management.git
cd Task-Management
```
### 2️⃣ Create Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
### 3️⃣ Install Requirements
```
pip install -r requirements.txt
```
### 4️⃣ Create .env File
Inside Hello/.env create:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
ADMIN_EMAILS=your_email@gmail.com
DATABASE_URL=sqlite:///db.sqlite3
⚠ Important: For Gmail, you must use an “App Password” (your normal Gmail password will NOT work).
```

### 5️⃣ Run Migrations
```
python manage.py migrate
```
#### 6️⃣ Create Superuser (Admin)
```
python manage.py createsuperuser
```
Admin Panel →
```
http://127.0.0.1:8000/admin/
```

### 7️⃣ Run Development Server
```
python manage.py runserver
```
Open App:
```
http://127.0.0.1:8000/
```
### 📸 Static & Media Setup
Static files:
```
python manage.py collectstatic
```
Media uploads →
```
media/profile_pics/
```

### 🗂 Models Overview
User Profile Model
```
First Name
Last Name
Username
Email
Mobile Number
Profile Image
Task Model
Title
Description
Status
Attempts
Re-Attempt Timestamp
```

### 🔥 Optional: Run Using Gunicorn (Production)
```
gunicorn Hello.wsgi
```
### 🤝 Contributing
```
Pull requests are welcome.
For major changes, please create an issue first.
```
📄 License
This project is open source and free to use.
