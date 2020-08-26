import os
from flask import Flask, flash, request, redirect, \
    url_for, render_template
from yolo_tiny import YOLO
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.MpoImagePlugin import MpoImageFile
from distance_2_ppl import distance_2_ppl
from person import Person

UPLOAD_FOLDER = '/code/image_in/'
OUTPUT_FOLDER = '/code/image_out/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['JSON_AS_ASCII'] = False
yolo = YOLO()

@app.route('/')
def index():
    return redirect('/detect_mitsu')

@app.route('/app/save_picture', methods=['POST'])
def save_picture():
    app.logger.debug(request)
    if len(request.files) < 1:
        return {'message': 'ファイルをアップロードしてください'}
    
    for f in request.files.values():
        f.save(UPLOAD_FOLDER + f.filename)

    return {'message': '保存しました'}

@app.route('/api/detect_mitsu', methods=['POST'])
def api_detect_mitsu():
    try:
        result, distance = do_detect_mitsu()
        return {
            'mitsu': result,
            'distance': distance
        }
    except RuntimeError as err:
        return {'error': str(err)}

@app.route('/detect_mitsu', methods=['GET', 'POST'])
def detect_mitsu():
    if request.method == 'POST':
        try:
            result, distance = do_detect_mitsu()
            return render_template("result.html", mitsu=result, distance='{:.2f}'.format(distance))
        except RuntimeError as err:
            flash(str(err))
            return redirect(request.url)

    return render_template("detect_mitsu.html")

def do_detect_mitsu():
    camera_mov_delta = get_float('move')
    if camera_mov_delta == 0:
        raise RuntimeError('カメラの移動距離を入力してください')

    cmos_length = get_float('cmos')
    if cmos_length == 0:
        raise RuntimeError('撮像素子サイズを入力してください')

    if not valid_file('pic1') or not valid_file('pic2'):
        raise RuntimeError('写真を2つアップロードしてください')

    pos_list1 = get_pos_list(request.files['pic1'])
    pos_list2 = get_pos_list(request.files['pic2'])
    if len(pos_list1) <= 1 or len(pos_list2) <= 1:
        raise RuntimeError('2人以上写っている写真をアップロードしてください')

    pic_length_in_pixel, focus_length = get_width_and_focus_length(request.files['pic1'])
    if focus_length is None:
        raise RuntimeError('メタデータに焦点距離を含む写真をアップロードしてください')

    return crowded_people(pos_list1, pos_list2, pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)

def get_float(name):
    if name not in request.form:
        return 0
    return float(request.form[name])

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_pos_list(file):
    image = Image.open(file)
    r_image, pos_list = yolo.detect_human(image)
    return pos_list

def get_width_and_focus_length(file):
    image: MpoImageFile = Image.open(file)
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
    distance_list = []
    for i in range(count):
        first_person = Person(pos_list1[i][0], pos_list2[i][0])
        for j in range(i + 1, count):
            second_person = Person(pos_list1[j][0], pos_list2[j][0])
            distance = distance_2_ppl(first_person, second_person, \
                pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta)

            distance_list.append(distance)

            app.logger.debug(first_person)
            app.logger.debug(second_person)
            app.logger.debug(distance)

            if distance < 200:
                return True, distance

    return False, min(distance_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get('PORT', 5000)))