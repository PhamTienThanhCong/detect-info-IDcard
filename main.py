# import libraries
from datetime import datetime
from functions import *
from detect_text_img import detect_text_img
from img_to_text import img_to_text
from flask import Flask, request, jsonify

# create flask app
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    # read file and save
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        new_name = datetime.now().strftime("%Y%m%d%H%M%S")
        new_name_1 = "./data_upload/raw/" + new_name + '.jpg'
        uploaded_file.save(new_name_1)
    else:
        return jsonify({"message": "khong co file duoc chon"})

    image = utils.read_image(new_name_1)
    img_crop = detect_id_cart(image)
    
    if img_crop is not None:
        new_name_2 = "./data_upload/crop/" + new_name + '.jpg'
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
        # save image
        cv2.imwrite(new_name_2, img_crop)
        
        detect_text_img(new_name_2, new_name)

        data = img_to_text(new_name)

        return jsonify(data)
    else:
        return jsonify({"message": "hinh anh ban chup khong phu hop"})

# set up basic view
@app.route('/')
def index():
    # get view index from file index.html
    return open('index.html').read()

# run sever
if __name__ == '__main__':
    app.run(debug=True, port=5000)

