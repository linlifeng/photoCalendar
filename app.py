from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

PHOTO_FOLDER = '/Users/lifenglin/dev/sites/photoCalendar/lelecenter/static/photos/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER



@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/upload_image", methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            print("!!!!!!!!!!!no file in payload@@@@@@@@@@@@@")
            print(request.files)
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("found file")
            # filename = secure_filename(file.filename)
            print(dir(request))
            print(request.form['date'])
            y, m, d = request.form['date'].split('-')
            date = m + d + y
            filename = date + '.jpg' # rename uploaded file to the date format so that it can be recognized.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template("index.html")


if __name__ == "__main__":
    app.secret_key = 'some secret key'
    app.run(debug=True, host='0.0.0.0')
