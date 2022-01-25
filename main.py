from datetime import datetime
from distutils.log import debug
from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector

app = Flask(__name__)

date = datetime.today().strftime('%Y-%m-%d')

db = connector.connect(
    host    = 'localhost',
    user    = 'root',
    passwd  = '',
    database= 'aplikasi'
)

if db.is_connected():
    print('open connection successful')

@app.route('/daftar-app/')
def daftar():
    cursor = db.cursor()
    cursor.execute('select * from link ORDER BY nama ASC')
    result = cursor.fetchall()
    cursor.close()
    return render_template('daftar.html', hasil = result)

@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute('select * from link ORDER BY id DESC ')
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', hasil = result)

@app.route('/admin/')
def admin():
    cursor = db.cursor()
    cursor.execute('select * from link ORDER BY id DESC')
    result = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', hasil = result)

@app.route('/admin/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/about-us/')
def about_us():
    return render_template('about-us.html')

@app.route('/contact-us/')
def contact_us():
    return render_template('contact-us.html')

@app.route('/tutorial/')
def tutorial():
    return render_template('tutorial.html')

@app.route('/admin/proses_tambah/', methods=['POST'])
def proses_tambah():
    nama = request.form['nama']
    direct = request.form['direct']
    google = request.form['google']
    mediafire = request.form['mediafire']
    zippyshare = request.form['zippyshare']
    password = request.form['password']
    cur = db.cursor()
    cur.execute('INSERT INTO link (tanggal, nama, direct, google, mediafire, zippyshare, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', (date, nama, direct, google, mediafire, zippyshare, password))
    db.commit()
    return redirect(url_for('admin'))

@app.route('/admin/ubah/<id>', methods=['GET'])
def ubah_data(id):
    cur = db.cursor()
    cur.execute('select * from link where id=%s', (id,))
    res = cur.fetchall()
    cur.close()
    return render_template('ubah.html', hasil=res)

@app.route('/admin/proses_ubah/', methods=['POST'])
def proses_ubah():
    id = request.form['id']
    nama = request.form['nama']
    direct = request.form['direct']
    google = request.form['google']
    mediafire = request.form['mediafire']
    zippyshare = request.form['zippyshare']
    password = request.form['password']    
    cur = db.cursor()
    cur.execute("UPDATE link SET tanggal=%s, nama=%s, direct=%s, google=%s, mediafire=%s, zippyshare=%s, password=%s  WHERE id=%s", (date, nama, direct, google, mediafire, zippyshare, password, id))
    db.commit()
    return redirect(url_for('admin'))

@app.route('/admin/hapus/<id>', methods=['GET'])
def hapus_data(id):
    cur = db.cursor()
    cur.execute('DELETE from link where id=%s', (id,))
    db.commit()
    return redirect(url_for('admin'))

replace_character = '-'
def fix_string(s):
    return s.replace(' ', replace_character)

@app.route('/<judul>')
def berita(judul):
    fix_string(judul)
    cursor = db.cursor()
    cursor.execute('select * from link where nama=%s', (judul,))
    result = cursor.fetchall()
    cursor.close()
    return render_template('app.html', hasil = result, JudulAwal=judul, aplikasi = judul)


if __name__ == '__main__':
    app.run(debug=True)