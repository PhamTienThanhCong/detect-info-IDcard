#import
import glob
from IPython.display import Image
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2
import re
import shutil


def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    # lower case
    s = s.lower()
    return s


# read text

config = Cfg.load_config_from_name('vgg_transformer')

config['weights'] = './model/transformerocr.pth'
config['cnn']['pretrained']=False
config['predictor']['beamsearch']=False
config['device'] = 'cpu'
detector = Predictor(config)


def img_to_text(name_img):
    info = []
    j = 0
    image_paths = "./outputs/" + name_img + "/" + name_img + "_crops/*.png"
    image_paths = glob.glob(image_paths)
    for i in range(3,len(image_paths)):
        url = "./outputs/" + name_img + "/" + name_img + "_crops/crop_{}.png".format(i)
        img = cv2.imread(url)
        img = Image.fromarray(img)
        s = detector.predict(img)
        s1 = no_accent_vietnamese(s)
        if (i == 3):
            s1 = s1.replace('so', '')

        index = s1.find('ho ten')
        if index != -1:
            s = s[index + 7:]

        index2 = s1.find('sinh ngay')
        if index2 != -1:
            s = s[index2 + 10:]

        index3 = s1.find('gioi tinh')
        if index3 != -1:
            s = s[index3 + 10:]

        index4 = s1.find('nguyen quan')
        if index4 != -1:
            s = s[index4 + 12:]

        index5 = s1.find('noi dkhk thuong tru')
        if index5 != -1:
            s = s[index5 + 20:]

        # xóa dấu cách thừa ở đầu và cuối
        s = s.strip()
        # xóa dấu cách thừa ở giữa
        s = re.sub(' +', ' ', s)

        if (s != ''):
            info.append(s)

    if (len(info) <= 6):
        que_quan = info[3]
        noi_dk = ""
        for i in range(4, len(info)):
            noi_dk += info[i] + " "
    else:
        que_quan = info[3] + " " + info[4]
        noi_dk = ""
        for i in range(5, len(info)):
            noi_dk += info[i] + " "

    result = {
        "Mã số": info[0],
        "Họ tên": info[1],
        "Ngày sinh": info[2],
        "Nguyên Quán": que_quan,
        "Nơi ĐKHK thường trú": noi_dk
    }
    # xóa thư mục outputs/crop
    thu_muc = "./outputs/" + name_img + ""

    shutil.rmtree(thu_muc)

    return result