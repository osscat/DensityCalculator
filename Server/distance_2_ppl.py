from person import Person
from math import atan, cos, sqrt, pow
import math

def distance_from_camera(person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta):
    return focus_length * camera_mov_delta /  \
        (cmos_length / pic_length_in_pixel * person.pixel_delta())

def angle_from_centre(person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta):
    centre = pic_length_in_pixel / 2
    distance_from_centre_pixel = abs(centre - person.coordinates[0])
    distance_from_centre_mm = cmos_length /pic_length_in_pixel * distance_from_centre_pixel
    return atan(distance_from_centre_mm / focus_length)

def distance_2_ppl_person(first_person, second_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta):
    distance_from_camera_p1 = distance_from_camera(first_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta)
    distance_from_camera_p2 = distance_from_camera(second_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta)

    angle_from_centre_p1 = angle_from_centre(first_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta)
    angle_from_centre_p2 = angle_from_centre(second_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta)

    angle_btw_people = angle_from_centre_p1 + angle_from_centre_p2
    distance_btw_people = math.sqrt(pow(distance_from_camera_p1, 2) + \
        pow(distance_from_camera_p2, 2) \
        - 2 * distance_from_camera_p1 * distance_from_camera_p2 * cos(angle_btw_people))
    return distance_btw_people

def distance_2_ppl(first_person, second_person, pic_length_in_pixel, cmos_length, 
    focus_length, camera_mov_delta):

    pixel_delta_p1 = first_person[0] - first_person[1]
    pixel_delta_p2 = second_person[0] - second_person[1]

    distance_from_camera_p1 = focus_length * camera_mov_delta /  \
        (cmos_length / pic_length_in_pixel * pixel_delta_p1)
    distance_from_camera_p2 = focus_length * camera_mov_delta /  \
        (cmos_length / pic_length_in_pixel * pixel_delta_p2)
    
    distance_from_centre_pixel_p1 = first_person[2] - first_person[3]
    distance_from_centre_pixel_p2 = second_person[2] - second_person[3]
    
    distance_from_centre_mm_p1 = cmos_length /pic_length_in_pixel * distance_from_centre_pixel_p1
    distance_from_centre_mm_p2 = cmos_length /pic_length_in_pixel * distance_from_centre_pixel_p2
    
    angle_from_centre_p1 = math.atan(distance_from_centre_mm_p1 / focus_length)
    angle_from_centre_p2 = math.atan(distance_from_centre_mm_p2 / focus_length)

    angle_btw_people = angle_from_centre_p1 + angle_from_centre_p2 
    distance_btw_people = math.sqrt(math.pow(distance_from_camera_p1, 2) + \
        math.pow(distance_from_camera_p2, 2) \
        - 2 * distance_from_camera_p1 * distance_from_camera_p2 * math.cos(angle_btw_people))

    return distance_btw_people

if __name__ == '__main__':
    # person[0] = coordinate1
    # person[1] = coordinate2
    # person[2] = coordinate3
    # person[3] = coordinate4

    first_person = (261.5, 127, 320, 261.5)
    second_person = (489, 402, 489, 320)
    pic_length_in_pixel = 640
    cmos_length = 4.8
    focus_length = 4
    camera_mov_delta = 70

    print(distance_2_ppl(first_person, second_person, \
        pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta))

    # personクラスを使った計算
    first_person = Person(261.5, 127)
    second_person = Person(489, 402)

    print(distance_2_ppl_person(first_person, second_person, \
        pic_length_in_pixel, cmos_length, focus_length, camera_mov_delta))