from vision_lib_funcs import AprilDetector
import cv2

# when running the setup of the program
key_fname = "tag_dict.csv" # matches april tag ids to food names
box_loc_fname = "eggs.csv" # camera calibration
camera_name = "/dev/video4" # camera name to pull from

ad = AprilDetector(camera_name, key_fname, box_loc_fname)


# then during the program ask the detector for item locations
item_loc1, frame = ad.get_item_loc_by_key("Tequila")
print(item_loc1)
cv2.imshow("image", frame)
cv2.waitKey(0)
# if it isn't found it will return a negative
item_loc2, frame = ad.get_item_loc_by_key("Bread")
print(item_loc2)
cv2.imshow("image", frame)

ad.clean()