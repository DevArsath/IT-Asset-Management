from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3, csv, io

DB = 'assets.db'
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    q = request.args.get('q','')
    conn = get_db()
    cur = conn.cursor()
    if q:
        cur.execute("SELECT * FROM assets WHERE hostname LIKE ? OR ip LIKE ?",
                    (f'%{q}%', f'%{q}%'))
    else:
        cur.execute("SELECT * FROM assets")
    rows = cur.fetchall()
    conn.close()
    return render_template('index.html', assets=rows, q=q)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        hostname = request.form['hostname']
        ip = request.form['ip']
        location = request.form['location']
        department = request.form['department']
        processor = request.form['processor']
        conn = get_db()
        conn.execute("INSERT INTO assets (hostname, ip, location, department, processor) VALUES (?,?,?,?,?)",
                     (hostname, ip, location, department, processor))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('form.html', action='Add', asset={})

@app.route('/edit/<int:aid>', methods=['GET','POST'])
def edit(aid):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        hostname = request.form['hostname']
        ip = request.form['ip']
        location = request.form['location']
        department = request.form['department']
        processor = request.form['processor']
        cur.execute("UPDATE assets SET hostname=?, ip=?, location=?, department=?, processor=? WHERE id=?",
                    (hostname, ip, location, department, processor, aid))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM assets WHERE id=?", (aid,))
    asset = cur.fetchone()
    conn.close()
    return render_template('form.html', action='Edit', asset=asset)

@app.route('/delete/<int:aid>', methods=['POST'])
def delete(aid):
    conn = get_db()
    conn.execute("DELETE FROM assets WHERE id=?", (aid,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/export')
def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT hostname,ip,location,department,processor FROM assets")
    rows = cur.fetchall()
    mem = io.StringIO()
    writer = csv.writer(mem)
    writer.writerow(['hostname','ip','location','department','processor'])
    for r in rows:
        writer.writerow(r)
    mem.seek(0)
    return send_file(io.BytesIO(mem.getvalue().encode('utf-8')), download_name='assets.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
