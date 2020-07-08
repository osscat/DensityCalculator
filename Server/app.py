import os, human_detect
from flask import Flask, flash, request, redirect, \
    url_for, render_template

UPLOAD_FOLDER = '/code/image_in/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            human_detect.analyse_upl_img(file.filename)    
            return '成功\n'

    return render_template("client.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get('PORT', 5000)))