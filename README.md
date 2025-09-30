# IT Asset Management
Simple IT Asset Management web app using Flask and SQLite.

## Features
- Add / Edit / Delete assets
- Search assets by hostname or IP
- Import/Export CSV

## Tech
- Python 3.8+
- Flask
- SQLite

## Quick start (local)
1. Create virtual env: `python -m venv venv && source venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Initialize DB: `python init_db.py`
4. Run: `python app.py`
5. Open http://127.0.0.1:5000/
