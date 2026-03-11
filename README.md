# Employee Management System (EMS)

A web-based **Employee Management System** built with **Django 6.0** and **Django REST Framework (DRF)**, featuring JWT authentication, API documentation with **drf-yasg**, and filtering support.  

---

## Features

- User authentication with **JWT** (via `djangorestframework_simplejwt`)  
- RESTful APIs for managing employees  
- Dynamic API documentation with **Swagger UI** (`drf-yasg`)  
- Filtering and searching using `django-filter`  
- Environment configuration via `.env` file  
- Compatible with **Python 3.12**  

---



# ------------------------------------------
# Employee Management System (EMS) Full Setup
# ------------------------------------------

# 1️⃣ Clone repository
git clone <your-repo-url>
cd emp_management

# 2️⃣ Create virtual environment
python -m venv venv

# 3️⃣ Activate virtual environment
venv\Scripts\activate

# 4️⃣ Upgrade pip and ensure setuptools/wheel (fix pkg_resources issues)
python -m pip install --upgrade pip
python -m pip install --upgrade --force-reinstall setuptools wheel

# 5️⃣ Install project requirements
pip install -r requirements.txt

# 5a️⃣ If drf-yasg error occurs, install manually
pip install drf-yasg>=1.21.5

# 6️⃣ Make migrations and migrate database
python manage.py makemigrations
python manage.py migrate

# 7️⃣ Run project-specific init migrations (if any)
python manage.py init_migrations

# 8️⃣ Start Django development server
python manage.py runserver

# 9️⃣ Access application in browser
Write-Host "✅ Project is running at http://127.0.0.1:8000/"

After starting the server, you can view interactive API documentation:
http://127.0.0.1:8000/api/docs/ 






