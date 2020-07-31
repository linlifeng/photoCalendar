from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, json

PHOTO_FOLDER = '/Users/lifenglin/dev/sites/photoCalendar/lelecenter/static/photos/'
DIARY_FOLDER = '/Users/lifenglin/dev/sites/photoCalendar/lelecenter/static/diary/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER
app.config['DIARY_FOLDER'] = DIARY_FOLDER


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route("/uploadbox/<date>", methods=['GET'])
def uploadbox(date):
    return render_template("upload_modal.html", date=date)


@app.route("/write_diary/<date>", methods=['GET'])
def write_diary(date):
    m = date[:2]
    d = date[2:4]
    y = date[-4:]
    formatted_date = y + '-' + m + '-' + d
    return render_template("write_diary.html", date=formatted_date)


@app.route("/diary/<date>", methods=['GET'])
def render_diary(date):
    diary_f_name = DIARY_FOLDER + date + '.json'
    photo_f_name = date + '.jpg'
    diary = json.load(open(diary_f_name))
    content = diary['content']
    date = diary['date']
    return render_template("diary.html", content=content, photo=photo_f_name, date=date)


def upload_and_save_image_file(request):
    file = request.files['image']
    y, m, d = request.form['date'].split('-')
    date = m + d + y
    filename = date + '.jpg'  # rename uploaded file to the date format so that it can be recognized.
    thumbnameFilename = 'thumb-' + filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    ## making thumbnail
    # importing Image class from PIL package
    from PIL import Image
    # creating a object
    image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    MAX_SIZE = (200, 200)
    image.thumbnail(MAX_SIZE)
    # creating thumbnail
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnameFilename))

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
            # print("found file")
            # # filename = secure_filename(file.filename)
            # print(dir(request))
            # print(request.form['date'])
            # y, m, d = request.form['date'].split('-')
            # date = m + d + y
            # filename = date + '.jpg' # rename uploaded file to the date format so that it can be recognized.
            # thumbnameFilename = 'thumb-' + filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ## making thumbnail
            # # importing Image class from PIL package
            # from PIL import Image
            # # creating a object
            # image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # MAX_SIZE = (200, 200)
            # image.thumbnail(MAX_SIZE)
            # # creating thumbnail
            # image.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnameFilename))
            # ## end making thumbnail
            upload_and_save_image_file(request)
    return render_template("index.html")

@app.route("/generate_diary", methods=['POST'])
def generate_diary():
    output = {}
    content = request.form['content']

    y, m, d = request.form['date'].split('-')
    date = m + d + y
    out_filename = app.config['DIARY_FOLDER'] + date + '.json'
    outf = open(out_filename, 'w')

    output['content'] = content
    output['date'] = date
    outf.write(json.dumps(output))

    file = request.files['image']
    if file and allowed_file(file.filename):
        upload_and_save_image_file(request)
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = 'some secret key'
    app.run(debug=True, host='0.0.0.0')
