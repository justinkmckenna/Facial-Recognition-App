from flask import Flask, render_template, request
import os
import face_recognition
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']

    for the_file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, the_file)
        try:
            if os.path.isfile(file_path):
                if "hC!+y^2`hu}Y:B" not in file_path:
                    os.unlink(file_path)
        except Exception as e:
            print(e)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    popeImage = face_recognition.load_image_file('./static/hC!+y^2`hu}Y:B.jpg')
    popeFaceEncoding = face_recognition.face_encodings(popeImage)[0]

    unknownImage = face_recognition.load_image_file(file)
    faceLocations = face_recognition.face_locations(unknownImage)
    if len(faceLocations) == 0:
        return render_template('error.html', filename = filename)
    unknownFaceEncoding = face_recognition.face_encodings(unknownImage)[0]

    results = face_recognition.compare_faces([popeFaceEncoding], unknownFaceEncoding)
    if results[0]:
        return render_template('success.html', filename = filename)
    else:
        return render_template('failure.html', filename = filename) 

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)