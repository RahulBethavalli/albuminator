# Launch with
#
# gunicorn -D --access-logfile server.log --timeout 60 server:app

import os
import zipfile
import io
import pathlib
import shutil

from model import *

from flask import Flask, flash, request, redirect, render_template, url_for, send_file
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024

app.secret_key = 'required for flashing sessions'

path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')

DOWNLOAD_FOLDER = os.path.join(path, 'sorted_folder')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        process_uploaded_files()
        #return redirect('/')
        return redirect('/sorted_files')
    
@app.route('/sorted_files')
def sorted_file_display():
    base_path = pathlib.Path(DOWNLOAD_FOLDER)
    #data = io.BytesIO()
    #with zipfile.ZipFile(data, mode='w') as z:
    #    for f_name in base_path.iterdir():
    #        z.write(f_name)
    #data.seek(0)
    shutil.make_archive('sorted' , 'zip' , base_path)
    return send_file('sorted.zip' , as_attachment = True)
    #return send_file(
    #    data,
    #    mimetype='application/zip',
    #    as_attachment=True,
    #    attachment_filename='data.zip'
    #)

def process_uploaded_files():
    create_sorted_folder()

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)


