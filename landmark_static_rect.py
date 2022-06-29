## Main modules import
import numpy as np
import os
## Visual modules import
import cv2
# from imutils.video import FileVideoStream # Probably not needed
from imutils import face_utils
import imutils
import dlib

face_rects= [ ( 's2' , [(181, 3) , (527, 408)] ),
              ( 's3' , [(210, 1) , (534, 372)] ),
              ( 's4' , [(194, 25), (528, 387)] ),
              ( 's5' , [(203, 32), (582, 432)] ),
              ( 's6' , [(205, 20), (570, 416)] ),
              ( 's7' , [(176, 14), (526, 423)] ),
              ( 's8' , [(106, 11), (475, 414)] ),
              ( 's9' , [(157, 3) , (502, 411)] ),
              ( 's10', [(258, 19), (580, 385)] ),
              ( 's11', [(212, 11), (557, 418)] ),
              ( 's12', [(210, 15), (549, 446)] ),
              ( 's13', [(227, 9) , (554, 414)] ),
              ( 's14', [(202, 3) , (572, 420)] ),
              ( 's15', [(192, 6) , (532, 386)] ),
              ( 's16', [(204, 6) , (559, 414)] ),
              ( 's17', [(194, 27), (543, 442)] ),
              ( 's18', [(207, 8) , (590, 473)] ),
              ( 's19', [(197, 12), (535, 421)] ),
              ( 's20', [(165, 7) , (514, 454)] ),
              ( 's21', [(213, 11), (548, 436)] ),
              ( 's22', [(203, 9) , (576, 433)] ),
              ( 's23', [(204, 4) , (572, 376)] ),
              ( 's24', [(204, 9) , (541, 442)] ),
              ( 's25', [(190, 21), (546, 456)] ),
              ( 's26', [(201, 24), (582, 454)] ),
              ( 's27', [(181, 6) , (582, 462)] ),
              ( 's28', [(231, 8) , (615, 438)] ),
              ( 's29', [(267, 5) , (622, 400)] ),
              ( 's30', [(198, 14), (528, 395)] ),
              ( 's31', [(215, 4) , (535, 325)] ),
              ( 's32', [(210, 13), (536, 404)] ),
              ( 's33', [(205, 2) , (577, 417)] ),
              ( 's34', [(204, 13), (574, 435)] ),
              ( 's35', [(172, 17), (532, 400)] ),
              ( 's36', [(184, 12), (533, 413)] ),
              ( 's37', [(178, 11), (534, 415)] ),
              ( 's38', [(175, 7) , (543, 411)] ),
              ( 's39', [(211, 13), (552, 427)] ),
              ( 's40', [(183, 4) , (530, 391)] ),
              ( 's41', [(203, 18), (514, 363)] ),
              ( 's42', [(171, 15), (527, 411)] ),
              ( 's43', [(159, 30), (528, 470)] ),
              ( 's44', [(225, 6) , (575, 399)] ),
              ( 's45', [(231, 15), (540, 426)] ),
              ( 's46', [(233, 17), (568, 420)] ),
              ( 's47', [(164, 16), (548, 418)] ),
              ( 's48', [(171, 16), (550, 414)] ),
              ( 's49', [(167, 15), (583, 457)] ),
              ( 's50', [(161, 16), (514, 429)] ),
              ( 's51', [(144, 27), (523, 473)] ),
              ( 's52', [(130, 26), (525, 479)] ),
              ( 's53', [(144, 12), (545, 475)] ),
              ( 's54', [(159, 14), (541, 440)] ),
              ( 's55', [(212, 21), (589, 439)] )
]


## Function definitions
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


def landmark_extraction(speaker):
    """ 
    Lip landmark extractor for lombard grid corpus 
    using opencv and dlib
    Keep in mind that it might not work on videos from other datasets
    """
    # dlib init face detector and face landmarks predictor
    face_detector = dlib.get_frontal_face_detector()
    landmarks_predictor = dlib.shape_predictor(os.path.join("/home/serafeim/audio-visual-thesis/shape_predictor","shape_predictor_68_face_landmarks_GTX.dat"))
    
    # We want only part of the landmarks, chin, lower nose, and mouth landmarks
    extr_indexes = list(range(6,13)) + list(range(32,37)) + list(range(49,68))
    points_per_frames = [] # The landmarks for each of the video frames

    
    for v in videos:
        
        vs = cv2.VideoCapture(video)
            
        ret, frame = vs.read() #Note: FileVideoStream adds extra None type frame at the end of the pipe.
        if ret == False:
            return False
            ## want to raise exeption 
        
        # use fix values, when face rectangle is known
        dets = [dlib.rectangle(190, 5, 505, 350)]

        landmarks = landmarks_predictor(frame, dets[0])
        points = face_utils.shape_to_np(landmarks)
        intrested_points = [points[i] for i in extr_indexes]
        
        for i, det in enumerate(dets):
            landmarks = landmarks_predictor(frame, det)
        
            points = face_utils.shape_to_np(landmarks)
        
            # extract points of interest
            intrested_points = [points[i] for i in extr_indexes]
            points_per_frames.append(intrested_points)
            #
            for (x,y) in intrested_points:
                frame = cv2.rectangle(frame, (dets[0].left(), dets[0].top()), (dets[0].right(), dets[0].bottom()),    #(left, top) and (right, bottom)
                                color=(0, 255, 0), thickness=3)
                frame = cv2.circle(frame, (x,y), radius=2, color=(255, 0, 0), thickness=-1)
        
        # return frame
        #save frame
    

if __name__ == "__main__":
    ## Parameters
    # path_video = '/home/serafeim/lombardgrid/front/s2'
    # video = os.path.join(path_video,'s2_l_bbim3a.mov')
    # path_video = '/home/serafeim/lombardgrid/front/s6'
    # video = os.path.join(path_video,'s6_l_bran5p.mov')
    dir_front = '/run/media/serafeim/1TB SSD/lombardgrid/front/'
    # display = True
    # static_face = False

    # dlib init face detector and face landmarks predictor
    face_detector = dlib.get_frontal_face_detector()
    landmarks_predictor = dlib.shape_predictor(os.path.join("/home/serafeim/audio-visual-thesis/shape_predictor","shape_predictor_68_face_landmarks_GTX.dat"))
    
    names   = [ n.split('.')[0] for n in os.listdir(dir_front) \
                                if n.endswith("25fps.mov")]
    names.sort()
    for n in names[0:6]:
        print(os.path.join(dir_front,n+".25fps.mov"))
        
    for n in names:
        frame = landmark_extraction(face_detector, landmarks_predictor, os.path.join(dir_front,n+".25fps.mov"))
        print (frame)
        if frame is False:
            exit()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(-1) & 0xFF
        if key == ord('q'):
             break
        # pp = input()
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