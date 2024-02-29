import cv2
import csv

csvfile = open('box_locs_shelf.csv', 'w', newline='')
pos_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

camera_address = "/dev/video4"
cam = cv2.VideoCapture(camera_address)
check, frame = cam.read()
cv2.imshow('image', frame)

csv_out = "webcam_regions.csv"

i = 0

n_boxes = 6

while i < n_boxes:
    check, frame = cam.read()
    r = cv2.selectROI('calibration_tool', frame, False, False)

    left = str(r[0])
    top = str(r[1])
    right = str(int(r[0] + r[2]))
    bottom = str(int(r[1] + r[3]))

    pos_writer.writerow([top, bottom, left, right])

    i += 1


csvfile.close()
cam.release()
cv2.destroyAllWindows()