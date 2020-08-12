import os, human_detect
from flask import Flask, flash, request, redirect, \
    url_for, render_template
from yolo_tiny import YOLO
from distance_2_ppl import distance_2_ppl_person
from person import Person

UPLOAD_FOLDER = '/code/image_in/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
yolo = YOLO()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return 'Hello World!\n'

@app.route('/post-picture', methods=['GET', 'POST'])
def post_picture():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'pic1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pic1']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            save_file(file)
            human_detect.analyse_upl_img(yolo, file.filename)    
            return '成功\n'

    return render_template("client.html")

def save_file(file):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

def valid_file(name):
    if name not in request.files:
        return False
    file = request.files[name]
    if file.filename == '':
        return False
    if file and allowed_file(file.filename):
        return True
    else:
        return False

@app.route('/detect_mitsu', methods=['GET', 'POST'])
def detect_mitsu():
    if request.method == 'POST':
        if not valid_file('pic1') or not valid_file('pic2'):
            flash('写真を2つアップロードしてください')
            return redirect(request.url)

        file1 = request.files['pic1']
        file2 = request.files['pic2']
        save_file(file1)
        save_file(file2)
        pos1 = human_detect.analyse_upl_img(yolo, file1.filename)
        pos2 = human_detect.analyse_upl_img(yolo, file2.filename)
        if len(pos1) <= 1 or len(pos2) <= 1:
            flash('2人以上写っている写真をアップロードしてください')
            return redirect(request.url)

        first_person = Person(pos1[0][0], pos2[0][0])
        second_person = Person(pos1[1][0], pos2[1][0])
        pic_length_in_pixel = 640
        cmos_length = 4.8
        focus_length = 4
        camera_mov_delta = 70

        distance = distance_2_ppl_person(first_person, second_person, \
            pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)
        return '2人の距離は' + str(distance)

    return render_template("detect_mitsu.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get('PORT', 5000)))