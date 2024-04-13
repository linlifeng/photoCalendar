from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, redirect, Response, make_response
from werkzeug.utils import secure_filename
import os, json, glob, pdfkit
from flask_weasyprint import HTML, CSS, render_pdf

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

USERS = {
    "linlifeng": '123456',
    "testuser": '123456',
    "lawrence": 'linxiubo'
}
# these users should all be lower cased, as later it will only check lower case for simplicity.
# passwords of course are still case sensitive

app = Flask(__name__)
PHOTO_FOLDER = app.root_path + '/static/photos/'
DIARY_FOLDER = app.root_path + '/static/diary/'
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER
app.config['DIARY_FOLDER'] = DIARY_FOLDER
SITE_PASSWORD = '123456'
TMP_FOLDER = '/tmp/'




@app.route("/login_page/")
def login_page():
    return render_template("login.html")


@app.route("/", methods=['GET', 'POST'])
def login():
    if not request.form:
        return login_page()
    username = request.form['username']
    password = request.form['password']
    if username.lower() in USERS and password == USERS[username]:
        return render_template("user_index.html", greetings="", authenticated=True, user=username)
    else:
        return login_page()


# this would bypass the login step
@app.route("/secretBackDoor", methods=['GET', 'POST'])
def default_home():
    return render_template("index.html", greetings="", authenticated=True)
# end


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/write_diary/<user>/<date>", methods=['GET'])
def write_diary(date, user):
    m = date[:2]
    d = date[2:4]
    y = date[-4:]
    formatted_date = y + '-' + m + '-' + d
    json_file_name = DIARY_FOLDER + user + '/' + date + '.json'
    if os.path.exists(json_file_name):
        existing_content = json.load(open(json_file_name))
        content = existing_content['content']
    else:
        content = ''
        date = 'default_photo'
    return render_template("write_diary.html", date=formatted_date, alt_date=date, content=content, user=user)


@app.route("/<user>/<date>/render_diary", methods=['GET'])
def render_diary(date, user):
    diary_f_name = DIARY_FOLDER + user + '/' + date + '.json'
    photo_f_name = user + '/' + date + '.jpg'
    if not os.path.exists(PHOTO_FOLDER + photo_f_name):
        photo_f_name = 'default_photo.jpg'
    diary = json.load(open(diary_f_name))
    content = diary['content']
    date = diary['date']
    return render_template("diary.html", content=content, photo=photo_f_name, date=date, user=user)


@app.route("/diary/<user>/<date>", methods=['GET'])
def show_diary_modal(date, user):
    diary_f_name = DIARY_FOLDER + user + '/' + date + '.json'
    if not os.path.exists(diary_f_name):
        print("new:",date)
        return write_diary(date, user)
    else:
        return render_diary(date, user)


def fill_default_image(request):
    user = request.form['user']
    y, m, d = request.form['date'].split('-')
    date = m + d + y
    filename = date + '.jpg'  # rename uploaded file to the date format so that it can be recognized.
    thumbnameFilename = 'thumb-' + filename

    # ## making thumbnail using just a white pixel (to fill the cell)
    os.system('ln -s %s %s'%(PHOTO_FOLDER + 'white_pixel.png', os.path.join(app.config['UPLOAD_FOLDER'] + user, thumbnameFilename)))
    os.system('ln -s %s %s'%(PHOTO_FOLDER + 'default_photo.jpg', os.path.join(app.config['UPLOAD_FOLDER'] + user, filename)))
    return '', 204


def upload_and_save_image_file(request):
    file = request.files['diary_image_upload_input']
    user = request.form['user']

    y, m, d = request.form['date'].split('-')
    date = m + d + y
    filename = date + '.jpg'  # rename uploaded file to the date format so that it can be recognized.
    thumbnameFilename = 'thumb-' + filename

    file.save(os.path.join(app.config['UPLOAD_FOLDER'] + user, filename))
    # the photo can be very big. Downsize to save space
    from PIL import Image, ExifTags
    image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'] + user, filename))
    MAX_SIZE = (1200, 800)
    THUMB_SIZE = (200, 200)

    # pillow will mess up the photo rotation if this is not down:
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation': break
    if image._getexif():
        exif = dict(image._getexif().items())
        if orientation not in exif:
            pass
        elif exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    # end restoring rotation issue

    if image.mode in ("RGBA", "P"): image = image.convert("RGB") #'a' is not allowed in PNG
    image.thumbnail(MAX_SIZE)
    os.system('rm %s'% os.path.join(app.config['UPLOAD_FOLDER'] + user, filename))
    image.save(os.path.join(app.config['UPLOAD_FOLDER'] + user, filename))
    # create thumbnail
    image.thumbnail(THUMB_SIZE)
    # print("saving to %s and %s" % (filename, thumbnameFilename))
    os.system("rm %s" % os.path.join(app.config['UPLOAD_FOLDER'] + user, thumbnameFilename))
    image.save(os.path.join(app.config['UPLOAD_FOLDER'] + user, thumbnameFilename))

    ## replace the background photo with today's new photo.
    from datetime import datetime
    today = datetime.today().date()
    thisyear = today.year
    thismonth = today.month
    thisday = today.day
    if int(y) == int(thisyear) and int(m) == int(thismonth) and int(d) == thisday:
        os.system('cp %s %s' % (PHOTO_FOLDER + user + '/' + filename,
                                PHOTO_FOLDER + user + '/image.jpg'))
    ## end replace background.


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/upload_image", methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            upload_and_save_image_file(request)
    return '', 204



@app.route("/generate_diary", methods=['POST'])
def generate_diary():
    output = {}
    content = request.form['content']
    username = request.form['user']
    y, m, d = request.form['date'].split('-')
    date = m + d + y
    out_filename = app.config['DIARY_FOLDER'] + username + '/' +date + '.json'
    outf = open(out_filename, 'w')

    output['content'] = content
    output['date'] = date
    outf.write(json.dumps(output))

    file = request.files['diary_image_upload_input']
    if file and allowed_file(file.filename):
        upload_and_save_image_file(request)
    else:
        fill_default_image(request)
    return '', 204


@app.route("/<user>/search", methods=['POST','GET'])
def search_diary(user):
    key = request.args['search']
    # user = request.args['search']

    search_result = '<table id="search_result_table">'

    if not key:
        return render_template("user_index.html", authenticated="True", user=user)
    import subprocess
    try:
        result = subprocess.check_output('grep -i "%s" %s*' % (key, DIARY_FOLDER + user + '/'), shell=True)
    except subprocess.CalledProcessError:
        search_result += "<tr><td>%s is not found in any entries.</tr></td>" % key
        search_result += '<tr><td><img src="/static/interface_assets/close.png" ' \
                         'style="width:60px;"' \
                         'onclick="hideSearchResult()"></td></tr>'
        search_result += '</table>'
        return render_template("user_index.html", search_result=search_result, authenticated=True, user=user)

    result_list = result.decode('utf-8').split('\n')
    # search_result = ''
    import re
    for hit in result_list:
        file = hit.replace(DIARY_FOLDER, '').split(':')[0]
        print(hit)
        date = file.split('.')[0].replace(user+'/', '')
        m = date[:2]
        d = date[2:4]
        y = date[4:]
        formatted_date = '-'.join([y, m, d])

        if date:
            hit_content = ':'.join(hit.replace(DIARY_FOLDER + user, '').split(':')[1:])
            hit_content = json.loads(hit_content)['content']
            hit_content = re.sub('<[^<]+>', "", hit_content)
            if len(hit_content) > 50:
                hit_content = hit_content[:50] + '...'
            link = '<a onclick="showDiary(\'%s\', \'%s\')">%s</a><br/>' % (date, user, formatted_date)
            print(link)
            row='<tr><td>' + link + '</td><td>' + hit_content + '</td></tr>'
            search_result += row
    search_result += '<tr><td><img src="/static/interface_assets/close.png" ' \
                     'style="width:60px;"' \
                     'onclick="hideSearchResult()"></td></tr>'
    search_result += '</table>'
    return render_template("user_index.html", search_result=search_result, authenticated=True, user=user)


@app.route("/export_all_diaries", methods=['POST'])
def export_all_diaries():
    user_name = request.form.get('user_name')
    files_location = DIARY_FOLDER + user_name

    diary_list = glob.glob(files_location + '/*')

    html_content = ''
    for file_location in diary_list:
        f = open(file_location)
        pdf_content = ''
        for l in f:
            pdf_content += l.rstrip()
        f.close()

        pdf_content = json.loads(pdf_content)
        if 'date' in pdf_content:
            html_content += '<h2>%s</h2>' % pdf_content['date']
        if 'content' in pdf_content:
            html_content += '<p>%s</p>' % pdf_content['content']

        html_content += '<img class="diary_image" src="/static/photos/%s/%s.jpg" />' % (user_name, pdf_content['date'])


    html = HTML(string=html_content)
    css = CSS(string='''
        @font-face {
            font-family: Gentium;
            src: url(http://example.com/fonts/Gentium.otf);
        }
        h1 { font-family: Gentium }
        .diary_image { width: 100%; }
        ''')

    return render_pdf(html, stylesheets=[css])




@app.route("/export_diary_by_date", methods=["POST"])
def export_diary_by_date():
    user_name = request.form.get('user_name')
    date = request.form.get('date')
    if '-' in date:
        yyyy, mm, dd = date.split("-")
        date = mm+dd+yyyy
    file_location = DIARY_FOLDER + user_name + '/' + date + '.json'
    if not os.path.exists(file_location):
        return render_pdf(HTML(string="No diary entry for this day: %s" % date))
    pdf_content = ''
    f = open(file_location)
    for l in f:
        pdf_content += l.rstrip()
    f.close()

    pdf_content = json.loads(pdf_content)
    html_content = '<h2>%s</h2>' % date
    for key in pdf_content:
        if key == 'content':
            html_content += '<p>%s</p>' % pdf_content[key]
    html_content += '<img class="diary_image" src="/static/photos/%s/%s.jpg" />' % (user_name, date)


    ## testing weasyprint
    # html = HTML(string='<h1>The title</h1>')
    html = HTML(string=html_content)
    css = CSS(string='''
        @font-face {
            font-family: Gentium;
            src: url(http://example.com/fonts/Gentium.otf);
        }
        h1 { font-family: Gentium }
        .diary_image { width: 100%; }
        ''')

    return render_pdf(html, stylesheets=[css])


if __name__ == "__main__":
    app.secret_key = 'some secret key'
    app.run(debug=True, host='0.0.0.0', port=8080)
