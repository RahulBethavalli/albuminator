# Launch with
#
# gunicorn -D --access-logfile server.log --timeout 60 server:app

import os
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024

app.secret_key = 'required for flashing sessions'

path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        return redirect('/')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)


