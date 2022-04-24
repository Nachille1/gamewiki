import os

import flask
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)

# Create a directory in a known location to save files to.
uploads_dir = os.path.join('', 'static/img')
# os.makedirs(uploads_dir)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # save the single "profile" file
        profile = request.files['profile']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        # save each "charts" file
        for file in request.files.getlist('charts'):
            file.save(os.path.join(uploads_dir, secure_filename(file.name)))


    return render_template('index.html')

app.run()