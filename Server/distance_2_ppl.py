from person import Person
from math import atan, cos, sqrt, pow

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

def distance_2_ppl(first_person, second_person, pic_length_in_pixel, cmos_length, 
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
    distance_btw_people = sqrt(pow(distance_from_camera_p1, 2) + \
        pow(distance_from_camera_p2, 2) \
        - 2 * distance_from_camera_p1 * distance_from_camera_p2 * cos(angle_btw_people))
    return distance_btw_people
