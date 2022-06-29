## Main modules import
import numpy as np
import os
import time
## Visual modules import
import cv2
# from imutils.video import FileVideoStream # Probably not needed 
from imutils import face_utils
import imutils
import dlib

# dlib init face detector and face landmarks predictor
face_detector = dlib.get_frontal_face_detector()
landmarks_predictor = dlib.shape_predictor(os.path.join("/home/serafeim/audio-visual-thesis/shape_predictor","shape_predictor_68_face_landmarks_GTX.dat"))
## Function definitions
class easy_transformation():
    def __init__(self) -> None:
        self._o=1
    def apply_to_img(self):
        pass
    def apply_to_points(self):
        pass
    def apply_reverse_to_img(self):
        pass
    def apply_reverse_to_points(self):
        pass

BGR_2_RGB = lambda a : a[:,:,::-1] # transformation from BGR to RGB

RECT_DLIB_2_CV = lambda a : [(a[0][0],a[1][1]),(a[1][0],[0][1])] # transformation from dlib rect to cv... LBRT_2_LTRB

def point_remap_after_resize(points, w, h, n_w=None, n_h=None):
    """This function remaps the points to correct the coordinates after the resize of the image
        argument points: a list of coordinates for the old image
        argument w: the ration new_width/old_width (or the old width of the image if n_w is set)
        argument h: the ration new_height/old_height (or optional the old height of the image if n_w is set)
        optional argument n_w: new width
        optional argument n_h: new hight
    """
    w_ratio = w if n_w is None else n_w/w
    h_ratio = h if n_h is None else n_h/h
    for (x, y) in points:
        x, y = w_ratio*x, h_ratio*y


def landmark_extraction(face_detector, landmarks_predictor, video, op=None):
    """ 
    Lip landmark extractor for lombard grid corpus 
    using opencv and dlib
    Keep in mind that it might not work on videos from other datasets
    """
    # start_time = time.time()
    # open video stream for video file. Use of default queue_size.
    # We want only part of the landmarks, chin, lower nose, and mouth landmarks
    extr_indexes = list(range(6,11)) + list(range(31,36)) + list(range(48,68))
    points_per_frames = [] # The landmarks for each of the video frames
    default_dets = [dlib.rectangle(190, 5, 505, 350)]

    stream = cv2.VideoCapture(video)
    # while 
    # print("Total of frames: {} or {}".format(count_frames(video, override=True),count_frames(video, override=False)))

    # vs = FileVideoStream(path=video, transform=None, queue_size=128).start()
    # while vs.more():# and counter<68:
        
    #     frame = vs.read() #Note: FileVideoStream adds extra None type frame at the end of the pipe.
    #     if frame is not None:

    #         if static_face:
    #             # use fix values, when face rectangle is known
    #             dets = [dlib.rectangle(190, 5, 505, 350)]
    #         else:
    #             # dlib facedetector for unknown images 
    #             # resize, and convert input frame to grayscale
    #             # img = imutils.resize(frame, width=500)
    #             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #             # facedetector works better on grayscale
    #             # smaller size images makes it faster in cost of not recognizing smaller faces(under 80x80px)
    #             # img = BGR_2_RGB(frame)
    #             # dets = face_detector(img, 1) 
    #             dets = face_detector(gray, 1) 

    #         landmarks = landmarks_predictor(frame, det)
    #         points = face_utils.shape_to_np(landmarks)
    #         intrested_points = [points[i] for i in extr_indexes]
            
            # print(dets)
            # for i, det in enumerate(dets):
            #     landmarks = landmarks_predictor(frame, det)
            
            #     points = face_utils.shape_to_np(landmarks)
            #     for (x,y) in points:
            #         frame = cv2.circle(frame, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
            
            #     # extract points of interest
            #     intrested_points = [points[i] for i in extr_indexes]
            #     points_per_frames.append(intrested_points)
            #     #
            #     for (x,y) in intrested_points:
            #         frame = cv2.rectangle(frame, (dets[0].left(), dets[0].top()), (dets[0].right(), dets[0].bottom()),    #(left, top) and (right, bottom)
            #                         color=(0, 255, 0), thickness=3)
            #         frame = cv2.circle(frame, (x,y), radius=2, color=(255, 0, 0), thickness=-1)
            # if display and frame is not None:
            #     # win.set_image(frame)
            #     # win.add_overlay(landmarks)
            #     cv2.imshow("Frame", frame)
            #     key = cv2.waitKey(-1) & 0xFF
            #     if key == ord('q'):
            #         break
    # print(time.time()-start_time)

    # cv2.destroyAllWindows()


#save frame
# cv2.imwrite('/path/to/destination/image.png',image)
if __name__ == "__main__":
    ## Parameters
    # path_video = '/home/serafeim/lombardgrid/front/s2'
    # video = os.path.join(path_video,'s2_l_bbim3a.mov')
    # path_video = '/home/serafeim/lombardgrid/front/s6'
    # video = os.path.join(path_video,'s6_l_bran5p.mov')
    dir_front = '/run/media/serafeim/1TB SSD/lombardgrid/front'
    # display = True
    # static_face = False

    # dlib init face detector and face landmarks predictor
    face_detector = dlib.get_frontal_face_detector()
    landmarks_predictor = dlib.shape_predictor(os.path.join("/home/serafeim/audio-visual-thesis/shape_predictor","shape_predictor_68_face_landmarks_GTX.dat"))
    
    names   = [ n.split('.')[0] for n in os.listdir(dir_front) \
                                if n.endswith("25fps.mov")]
    for n in names:
        landmark_extraction(face_detector, landmarks_predictor, os.path.join(dir_front,n+".25fps.mov"))
    # if os.cpu_count() <= 4:
    #     # too few cores, no benefits for multiprocessing
    #     # FileVideoStream already needs one extra thread
        
    
    # else:
    #     # More than 2 cores, so there could be a benefit 
    #     import multiprocessing

    #     # Initialize the workers. Half the system available cores FileVideoStream already needs one extra thread...
    #     p = multiprocessing.Pool(os.cpu_count()/2)
    #     # Schedule work to workers
    #     p.imap_unordered(, names, 100)
        
    #     # Wait for job to finish
    #     p.close()
    #     p.join()