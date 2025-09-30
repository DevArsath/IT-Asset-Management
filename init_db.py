import sqlite3
DB='assets.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT,
    ip TEXT,
    location TEXT,
    department TEXT,
    processor TEXT
)
''')
conn.commit()
conn.close()
print('Database initialized:', DB)
