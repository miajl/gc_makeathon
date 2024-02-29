import apriltag
import cv2
import csv
import halcon as ha

obj_keys = {}
obj_keys_reader = csv.reader(open("tag_dict.csv"))
for row in obj_keys_reader:
	obj_keys[int(row[0])] = row[1]

framegrabber = ha.open_framegrabber(
    name='Video4Linux2',
    horizontal_resolution=1,
    vertical_resolution=1,
    image_width=0,
    image_height=0,
    start_row=0,
    start_column=0,
    field='progressive',
    bits_per_channel=-1,
    color_space='gray',
    generic=-1,
    external_trigger='false',
    camera_type='audio',
    device='video4',
    port=0,
    line_in=-1
)

img = ha.grab_image(framegrabber)
img_width, img_height = ha.get_image_size_s(img)

box_locs = {}

box_loc_reader = csv.reader(open("box_locs.csv"))
i = 0
for row in box_loc_reader:
	box_locs[i] = {}
	box_locs[i]["top"] = int(float(row[0]) * img_height)
	box_locs[i]["bottom"] = int(float(row[1]) * img_height)
	box_locs[i]["left"] = int(float(row[2]) * img_width)
	box_locs[i]["right"] = int(float(row[3]) * img_width)
	i += 1
print(obj_keys)
print(box_locs)



options = apriltag.DetectorOptions(families = "tag36h11")
detector = apriltag.Detector(options)

def add_lines(frame):
	for value in box_locs.values():
		cv2.rectangle(frame, (value["left"], value["top"]), (value["right"], value["bottom"]), (0, 0, 255), 2)

def display_results(results, frame):
	for r in results:
		# extract the bounding box (x, y)-coordinates for the AprilTag
		# and convert each of the (x, y)-coordinate pairs to integers
		(ptA, ptB, ptC, ptD) = r.corners
		ptB = (int(ptB[0]), int(ptB[1]))
		ptC = (int(ptC[0]), int(ptC[1]))
		ptD = (int(ptD[0]), int(ptD[1]))
		ptA = (int(ptA[0]), int(ptA[1]))
		# draw the bounding box of the AprilTag detection
		cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
		cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
		cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
		cv2.line(frame, ptD, ptA, (0, 255, 0), 2)
		# draw the center (x, y)-coordinates of the AprilTag
		(cX, cY) = (int(r.center[0]), int(r.center[1]))
		cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
		# draw the tag family on the image
		tagFamily = r.tag_family.decode("utf-8")
		cv2.putText(frame, obj_keys[r.tag_id], (ptA[0], ptA[1] - 15),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		# cv2.putText(frame, str(r.tag_id), (ptA[0], ptA[1] - 15),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	# show the output image after AprilTag detection
	add_lines(frame)
	cv2.imshow("Image", frame)
	return
def clean(self)

# def item_in_box(center):
# 	(cX, cY) = (int(center[0]), int(center[1]))

# 	for i in range(len(box_locs.keys())):
# 		if cX > box_locs[i]["left"] and cX < box_locs[i]["right"] and cY > box_locs[i]["top"] and cY < box_locs[i]["bottom"]:
# 			return i 
		
# 	return -1


# def get_locations(tag_id):
# 	for r in results:
# 		if (r.tag_id == tag_id)
# 			return item_in_box(r.center)		
# 	return -2



while True:

	# check, frame = cam.read()
    img = ha.grab_image(framegrabber)

    frame = ha.himage_as_numpy_array(img)
	
    # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    
    # results = detector.detect(frame)

    # display_results(results, frame)
	# get_locations(results)
	
    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
	
    if key == 27:
        break
	

