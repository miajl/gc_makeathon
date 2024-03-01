import pupil_apriltags as pa
import cv2
import csv
import queue, threading

class BufferlessVideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put((ret, frame))

  def read(self):
    return self.q.get()
  def clean(self):
     self.cap.release()


class AprilDetector():
    def __init__(self, camera_address, key_fname, box_loc_fname):
        self.cam = BufferlessVideoCapture(camera_address)
        check, frame = self.cam.read()
		
        self.obj_keys = {}
        obj_keys_reader = csv.reader(open(key_fname))
        for row in obj_keys_reader:
            self.obj_keys[int(row[0])] = row[1]
			
        self.box_locs = {}

        box_loc_reader = csv.reader(open(box_loc_fname))
        i = 0
        for row in box_loc_reader:
            self.box_locs[i] = {}
            self.box_locs[i]["top"] = int(row[0])
            self.box_locs[i]["bottom"] = int(row[1])
            self.box_locs[i]["left"] = int(row[2])
            self.box_locs[i]["right"] = int(row[3])
            i += 1
			
        # options = apriltag.DetectorOptions(families = "tag36h11")
        # self.detector = apriltag.Detector(options)
        self.detector = pa.Detector(
            families="tag36h11",
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0
            )
		
    def add_lines(self, frame):
        for value in self.box_locs.values():
            cv2.rectangle(frame, (value["left"], value["top"]), (value["right"], value["bottom"]), (0, 0, 255), 2)
	

    def display_results(self, results, desired_item_id, frame):
        
        for r in results:
            if r.tag_id == desired_item_id:
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
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
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(frame, self.obj_keys[r.tag_id], (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # cv2.putText(frame, str(r.tag_id), (ptA[0], ptA[1] - 15),
            # 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # show the output image after AprilTag detection
        self.add_lines(frame)    
        cv2.imshow("image", frame)
    
    def item_in_box(self, center):
        (cX, cY) = (int(center[0]), int(center[1]))

        for i in range(len(self.box_locs.keys())):
            if cX > self.box_locs[i]["left"] and cX < self.box_locs[i]["right"] and cY > self.box_locs[i]["top"] and cY < self.box_locs[i]["bottom"]:
                return i 
            
        return -1
    def get_location(self, results, tag_id):
        for r in results:
            if (r.tag_id == tag_id):
                return self.item_in_box(r.center)
        return -2



    def find_tags(self):
        check, frame = self.cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame, self.detector.detect(gray)

    def get_item_loc_by_key(self, desired_item):
        # ret val zero or greater is box location
        # -1: found the item, but it is not in any box location
        # -2: Did not find the item
        # -3: desired item does not match any in the key dictionary
        frame, results = self.find_tags()
        obj_id = -3
        for obj_key in self.obj_keys.keys():
            if self.obj_keys[obj_key] == desired_item:
                obj_id = obj_key
       
        retval = self.get_location(results, obj_id)
        self.display_results(results, obj_id, frame)
        if obj_id == -3:
           return obj_id
        return retval
    def clean(self):
       self.cam.clean()
       cv2.destroyAllWindows()
    
             
         
key_fname = "tag_dict.csv"
box_loc_fname = "eggs.csv"
desired_items = ["Eggs", "Bread", "Tequila", "Beer"]
# camera_name = "/dev/video4"
camera_name = 0

ad = AprilDetector(camera_name, key_fname, box_loc_fname)
i = 0
while True:
    i += 1
    i %= 4
    retval = ad.get_item_loc_by_key(desired_items[i])
    
    print("Item " + desired_items[i] + " in location " + str(retval))

    key = cv2.waitKey(0)
    if key == 27:
        break
