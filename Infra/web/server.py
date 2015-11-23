from __future__ import absolute_import

import os, sys
import uuid
import logging
from werkzeug import secure_filename
from flask import Flask, url_for, json, request, make_response, render_template, jsonify

# Relative imports
# sys.path.append('../shared')
sys.path.append('./tasks')
import celery
import count

## Web server
app = Flask(__name__)

## Variables
app.config['UPLOAD_FOLDER'] = '/usr/src/app/data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])

# Logging
#file_handler = logging.FileHandler('app.log')
#app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

## Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def make_tree(path):
    tree = dict(name=path, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree

@app.route('/')
def api_root():
    return 'Imagenet API server'

@app.route('/count')
def count_words():
    job = count.count_words_at_url.delay('http://netflix.com')

    resp = jsonify(id=job.id)
    resp.mimetype='application/json'
    resp.status_code = 201

    return resp

@app.route('/job/<job_id>')
def get_job_for_id(job_id):
    job = celery.result.AsyncResult(job_id)
    resp = make_response()
    if job:
        if job.ready():
            resp = jsonify(
                status=job.state,
                result=job.result
                )
            resp.status_code = 200
        else:
            resp = jsonify(
                status=job.state
            )
    else:
        resp.status_code = 404

    return resp

@app.route('/files')
def list_files():
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'])
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)

@app.route('/upload', methods = ['POST'])
def upload():
    resp = make_response()
    file = request.files['file']

    # print pprint.pformat(request.environ, depth=5)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp.status_code = 201
    else:
        resp.status_code = 413
    
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    host = '0.0.0.0'
    print("Started app", port, host)
    app.run(
        host=host,
        port=port,
        debug=True
    )
