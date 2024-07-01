from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQLite database
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, filename TEXT)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Save filename to database
        c.execute('INSERT INTO images (filename) VALUES (?)', (filename,))
        conn.commit()

        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads')
def uploaded_file():
    c.execute('SELECT filename FROM images')
    images = c.fetchall()
    return render_template('uploads.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
