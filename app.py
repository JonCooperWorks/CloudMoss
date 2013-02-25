'''
CloudMoss - Check against moss in the cloud.
'''

from flask import Flask, render_template, request, redirect, abort
from werkzeug import secure_filename

import os
import datetime
import moss
import zipfile

#Application Setup
app = Flask(__name__)
app.config['UPLOAD_DIR'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['zip']) #Support for other file types coming soon.
app.config['SUPPORTED_LANGUAGES'] = set(['java', 'python'])

#Helper methods
def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def filetype(filename):
    return filename.rsplit('.', 1)[1]


#Controllers
@app.route('/', methods=['GET', 'POST'])
@app.route('/<language>', methods=['GET', 'POST'])
def upload(language='python'):
    if language not in app.config['SUPPORTED_LANGUAGES']:
        abort(404)
    if request.method == 'POST':
        f = request.files['assignment']
        if f and valid_file(f.filename):
            language_dir = os.path.join(os.getcwd(), os.path.join(app.config['UPLOAD_DIR'], language))
            filename = os.path.join(language_dir, secure_filename(f.filename))
            f.save(filename)
            with zipfile.ZipFile(filename) as zip_file:
                zip_file.extractall(path=language_dir)
                os.unlink(filename)
            response_url = moss.get_results(language, app.config['UPLOAD_DIR'])
            if 'Checking files' in response_url:
                return render_template('failure.html')
            return redirect(response_url)
        return render_template('failure.html')
    return render_template('upload.html', language=language)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view/<language>')
def view(language):
    response_url = moss.get_results(language, app.config['UPLOAD_DIR'])
    return redirect(response_url)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

#App runner
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)