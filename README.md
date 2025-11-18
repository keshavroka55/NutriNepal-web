# NutriNepal Web App

A **Calorie Tracking (Kcal) web application** built while learning Django. This project allows users to track daily calorie intake, manage nutrition, and connect healthy habits with technology. It includes both **Django default authentication** and **Google login** for user convenience.

---

## Features

- Track daily calorie intake with food entries & weight tracking 
- Add, edit, and delete food entries  
- View total calories consumed per day  
- **User authentication**: Django default login/register + **Google login**  
- Simple and clean user interface  
- Responsive design (works on desktop and mobile)  

---

## Skills Learned

By building this project, I learned and implemented:  

1. **Django Web Development**  
   - Models, Views, Templates, Forms  
   - CRUD operations  
   - User authentication and session management  

2. **Google OAuth (Continue with Google)**  
   - Integrated Google login alongside Django default auth using `django-allauth`  
   - Learned OAuth flow: redirect, token exchange, and user creation  

3. **Frontend Skills**  
   - CSS and Bootstrap for responsive UI  
   - Template inheritance and static files management  

4. **Deployment Skills (Linux + DigitalOcean)**  
   - Setting up Ubuntu server on DigitalOcean  
   - Installing Python, virtual environments, and dependencies  
   - Running Django project with **Gunicorn** (WSGI server)  
   - Configuring **Nginx** as a reverse proxy  
   - Using **systemd** for service management  
   - Firewall setup and basic security  

5. **Version Control & Project Management**  
   - Git for code versioning and deployment  
   - Organizing project structure professionally  

**Mnemonic to remember deployment stack:**  
**“LPGNFS” → Linux, Python/Django, Gunicorn, Nginx, Firewall, Systemd**  

---

## Tech Stack

- **Backend**: Django  
- **Database**: SQLite  
- **Templates**: Django Templates  
- **Styling**: CSS / Bootstrap  
- **Authentication**: Django Auth + Google OAuth (`django-allauth`)  
- **Deployment**: Gunicorn + Nginx on Linux server (DigitalOcean)  

---

## Getting Started (Git Bash)

1. **Clone the repository**

   ```bash
   git clone https://github.com/keshavroka55/NutriNepal-web.git
   cd NutriNepal-web

