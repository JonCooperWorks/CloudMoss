from flask import Flask, render_template, request, make_response, redirect
from werkzeug import secure_filename

import os
import datetime
import moss

#Application Setup
UPLOAD_DIR = 'uploads'
ALLOWED_EXTENSIONS = set(['zip', 'rar', 'tar.gz', 'tar.bz2'])

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

#Helper methods
def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'] or True

def filetype(filename):
    return filename.rsplit('.', 1)[1]


#Controllers
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['assignment']
        if f and valid_file(f.filename):
            filename = os.path.join(app.config['UPLOAD_DIR'], secure_filename(f.filename))
            f.save(filename)
            response_url = moss.get_results('python', 'py', app.config['UPLOAD_DIR'])
            return redirect(response_url)
        return render_template('failure.html')
    return render_template('upload.html')



#App runner
if __name__ == '__main__':
    app.run(debug=True)