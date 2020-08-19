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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
yolo = YOLO()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect('/detect_mitsu')

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

def get_pos_list(name):
    file = request.files[name]
    save_file(file)
    return human_detect.analyse_upl_img(yolo, file.filename)

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

    return width, None

def crowded_people(pos_list1, pos_list2, pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta):
    app.logger.debug(pos_list1)
    app.logger.debug(pos_list2)

    count = len(pos_list1)
    for i in range(count):
        first_person = Person(pos_list1[i][0], pos_list2[i][0])
        for j in range(i + 1, count):
            second_person = Person(pos_list1[j][0], pos_list2[j][0])
            distance = distance_2_ppl_person(first_person, second_person, \
                pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)

            app.logger.debug(first_person)
            app.logger.debug(second_person)
            app.logger.debug(distance)

            if distance < 200:
                return True

    return False

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

        pos_list1 = get_pos_list('pic1')
        pos_list2 = get_pos_list('pic2')
        if len(pos_list1) <= 1 or len(pos_list2) <= 1:
            flash('2人以上写っている写真をアップロードしてください')
            return redirect(request.url)

        pic_length_in_pixel, focus_length = get_width_and_focus_length(request.files['pic1'].filename)
        if focus_length is None:
            flash('メタデータに焦点距離を含む写真をアップロードしてください')
            return redirect(request.url)

        result = crowded_people(pos_list1, pos_list2, pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)
        return render_template("result.html", mitsu=result)

    return render_template("detect_mitsu.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get('PORT', 5000)))