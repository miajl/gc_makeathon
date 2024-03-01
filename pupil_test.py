import cv2
import pupil_apriltags as pa

frame = cv2.imread("imgs/ss_tags.png")
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

detector = pa.Detector(
            families="tag36h11",
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0
            )

results = detector.detect(gray)
color = (0, 255, 255)

print(results)

for r in results:

    # extract the bounding box (x, y)-coordinates for the AprilTag
    # and convert each of the (x, y)-coordinate pairs to integers
    (ptA, ptB, ptC, ptD) = r.corners
    ptB = (int(ptB[0]), int(ptB[1]))
    ptC = (int(ptC[0]), int(ptC[1]))
    ptD = (int(ptD[0]), int(ptD[1]))
    ptA = (int(ptA[0]), int(ptA[1]))
    # draw the bounding box of the AprilTag detection
    cv2.line(frame, ptA, ptB, color, 2)
    cv2.line(frame, ptB, ptC, color, 2)
    cv2.line(frame, ptC, ptD, color, 2)
    cv2.line(frame, ptD, ptA, color, 2)
            # draw the center (x, y)-coordinates of the AprilTag
    (cX, cY) = (int(r.center[0]), int(r.center[1]))
    cv2.circle(frame, (cX, cY), 5, color, -1)
            # draw the tag family on the image
    cv2.putText(frame, str(r.tag_id), (ptA[0], ptA[1] - 15),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # cv2.putText(frame, str(r.tag_id), (ptA[0], ptA[1] - 15),
            # 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # show the output image after AprilTag detection
   
    cv2.imshow("image", frame)

cv2.waitKey(0)

