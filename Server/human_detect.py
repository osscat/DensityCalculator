from yolo_tiny import YOLO, detect_video
from PIL import Image
import numpy as np

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(f"./image_in/{img}")
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image, human_pos_list = yolo.detect_human(image)
            print(human_pos_list)
            r_image.save(f"./image_out/{img}")
            r_image.show()
    yolo.close_session()

def analyse_upl_img(yolo, filename):
    image = Image.open(f"./image_in/{filename}")
    r_image, human_pos_list = yolo.detect_human(image)
    print(human_pos_list)
    r_image.save(f"./image_out/{filename}")
    return human_pos_list


if __name__ == '__main__':
    detect_img(YOLO())