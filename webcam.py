import cv2
import halcon as ha
# cam = cv2.VideoCapture(0)



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
    color_space='rgb',
    generic=-1,
    external_trigger='false',
    camera_type='audio',
    device='video4',
    port=0,
    line_in=-1
)

img = ha.grab_image(framegrabber)
width, height = ha.get_image_size_s(img)

window = ha.open_window(
    row=0,
    column=0,
    width=width,
    height=height,
    father_window=0,
    mode='visible',
    machine=''
)
ha.disp_obj(img, window)

# while True:
#     img = ha.grab_image(framegrabber)
#     width, height = ha.get_image_size_s(img)

#     frame = ha.himage_as_numpy_array(img)
    
    # cv2.imshow("Image", frame)

    # key = cv2.waitKey(1)
    # if key == 27:
    #     break

# cam.release()
# cv2.destroyAllWindows()