# Nani Digitals — Deployment Guide

## Local Development
```bash
cd nani_studio
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python seed.py
python app.py
```
Open http://127.0.0.1:5000

## PythonAnywhere Deployment
1. Upload all files to PythonAnywhere
2. Create a new Python web app (Flask)
3. Set the WSGI file to point to `wsgi.py`
4. Set the source directory to your project folder
5. Run `pip install -r requirements.txt`
6. Set environment variable `SECRET_KEY` in Web tab
7. Reload the web app

## Render Deployment
1. Push code to GitHub
2. Create a new Web Service on Render
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn wsgi:application`
5. Add `gunicorn` to requirements.txt
