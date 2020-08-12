import os, human_detect
from flask import Flask, flash, request, redirect, \
    url_for, render_template
from yolo_tiny import YOLO
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.MpoImagePlugin import MpoImageFile
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

def get_float(name):
    if name not in request.form:
        return 0
    return float(request.form[name])

def get_width_and_focus_length(filename):
    image: MpoImageFile = Image.open(f"./image_in/{filename}")
    width = image.size[0]

    exif = image.getexif()
    # tag_idはExif情報のキー、valueはExif情報の値。
    # tag_idはstr型ではないので、TAGS.getメソッドによってstr型に変換する
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'FocalLength':
            return width, value

@app.route('/detect_mitsu', methods=['GET', 'POST'])
def detect_mitsu():
    if request.method == 'POST':
        camera_mov_delta = get_float('move')
        if camera_mov_delta == 0:
            flash('カメラの移動距離を入力してください')
            return redirect(request.url)

        cmos_length = get_float('cmos')
        if cmos_length == 0:
            flash('撮像素子サイズを入力してください')
            return redirect(request.url)

        if not valid_file('pic1') or not valid_file('pic2'):
            flash('写真を2つアップロードしてください')
            return redirect(request.url)

        file1 = request.files['pic1']
        file2 = request.files['pic2']
        save_file(file1)
        save_file(file2)

        pos1 = human_detect.analyse_upl_img(yolo, file1.filename)
        pos2 = human_detect.analyse_upl_img(yolo, file2.filename)
        app.logger.debug(pos1)
        app.logger.debug(pos2)
        if len(pos1) <= 1 or len(pos2) <= 1:
            flash('2人以上写っている写真をアップロードしてください')
            return redirect(request.url)

        first_person = Person(pos1[0][0], pos2[0][0])
        second_person = Person(pos1[1][0], pos2[1][0])
        pic_length_in_pixel, focus_length = get_width_and_focus_length(file1.filename)

        distance = distance_2_ppl_person(first_person, second_person, \
            pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)
        return '2人の距離は {:.2f} cm'.format(distance)

    return render_template("detect_mitsu.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get('PORT', 5000)))