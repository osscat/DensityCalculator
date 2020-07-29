from yolo import YOLO, detect_video
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

def analyse_upl_img(filename):
    yolo = YOLO()
    image = Image.open(f"./image_in/{filename}")
    r_image, human_pos_list = yolo.detect_human(image)
    print(human_pos_list)
    r_image.save(f"./image_out/{filename}")
    yolo.close_session()


def distance_2_ppl(first_person, second_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta):
    pixel_delta
    distance_from_camera
    distance_from_centre_pixel
    distance_from_centre_mm
    angle_from_centre
    return distance_btw_people


if __name__ == '__main__':
    detect_img(YOLO())