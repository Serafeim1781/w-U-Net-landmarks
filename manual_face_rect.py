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

listofvideos = [ "s2_l_bbim3a.25fps.mov", # "s2_p_swwx9p.25fps.mov", \
                 "s3_l_bbam2p.25fps.mov", # "s3_p_swwp8s.25fps.mov", \
                 "s4_l_bbai2p.25fps.mov", # "s4_p_swbxza.25fps.mov", \
                 "s5_l_bbib5p.25fps.mov", # "s5_p_swwe5n.25fps.mov", \
                 "s6_l_bbwo7s.25fps.mov", # "s6_p_swiv3a.25fps.mov", \
                 "s7_l_bbaf9a.25fps.mov", # "s7_p_swwk1n.25fps.mov", \
                 "s8_l_bbbm9n.25fps.mov", # "s8_p_swws4a.25fps.mov", \
                 "s9_l_bbbm9n.25fps.mov", # "s9_p_swws4a.25fps.mov", \
                 "s10_l_bbat9p.25fps.mov",# "s10_p_swib5n.25fps.mov", \
                 "s11_l_bbab2n.25fps.mov",# "s11_p_swwszs.25fps.mov", \
                 "s12_l_bbavza.25fps.mov",# "s12_p_swwl1n.25fps.mov", \
                 "s13_l_bbah3p.25fps.mov",# "s13_p_swwz5n.25fps.mov", \
                 "s14_l_bbau7n.25fps.mov",# "s14_p_sway9a.25fps.mov", \
                 "s15_l_bbab6a.25fps.mov",# "s15_p_swap2a.25fps.mov", \
                 "s16_l_bbam1a.25fps.mov",# "s16_p_swwv7n.25fps.mov", \
                 "s17_l_bbba3s.25fps.mov",# "s17_p_swwr9n.25fps.mov", \
                 "s18_l_bbatzp.25fps.mov",# "s18_p_swik4p.25fps.mov", \
                 "s19_l_bban1p.25fps.mov",# "s19_p_swwd2p.25fps.mov", \
                 "s20_l_bbwh7n.25fps.mov",# "s20_p_swwz5a.25fps.mov", \
                 "s21_l_bbbn9a.25fps.mov",# "s21_p_swwyzn.25fps.mov", \
                 "s22_l_bbbg4a.25fps.mov",# "s22_p_swws1n.25fps.mov", \
                 "s23_l_bbal9p.25fps.mov",# "s23_p_swwd1a.25fps.mov", \
                 "s24_l_bbbv5p.25fps.mov",# "s24_p_swby1a.25fps.mov", \
                 "s25_l_bbbv5p.25fps.mov",# "s25_p_swby1a.25fps.mov", \
                 "s26_l_bbanza.25fps.mov",# "s26_p_swiy3s.25fps.mov", \
                 "s27_l_bbbo5s.25fps.mov",# "s27_p_swwdzn.25fps.mov", \
                 "s28_l_bbbu8n.25fps.mov",# "s28_p_swwe4p.25fps.mov", \
                 "s29_l_bbaz8n.25fps.mov",# "s29_p_swwc7n.25fps.mov", \
                 "s30_l_bbbm4a.25fps.mov",# "s30_p_swwq7a.25fps.mov", \
                 "s31_l_bbib2p.25fps.mov",# "s31_p_swwz1a.25fps.mov", \
                 "s32_l_bbab5n.25fps.mov",# "s32_p_swwp9p.25fps.mov", \
                 "s33_l_bbih4a.25fps.mov",# "s33_p_swbjzn.25fps.mov", \
                 "s34_l_bbibzs.25fps.mov",# "s34_p_swwd8p.25fps.mov", \
                 "s35_l_bbbt6n.25fps.mov",# "s35_p_swwzza.25fps.mov", \
                 "s36_l_bbat1p.25fps.mov",# "s36_p_swijzn.25fps.mov", \
                 "s37_l_bbag9a.25fps.mov",# "s37_p_swap1s.25fps.mov", \
                 "s38_l_bbal9n.25fps.mov",# "s38_p_swwx7n.25fps.mov", \
                 "s39_l_bbab8s.25fps.mov",# "s39_p_swbq7a.25fps.mov", \
                 "s40_l_bbbc2s.25fps.mov",# "s40_p_swwr6n.25fps.mov", \
                 "s41_l_bbas4s.25fps.mov",# "s41_p_swio8s.25fps.mov", \
                 "s42_l_bbam1n.25fps.mov",# "s42_p_swiq4a.25fps.mov", \
                 "s43_l_bbao6a.25fps.mov",# "s43_p_swix8n.25fps.mov", \
                 "s44_l_bbaa5s.25fps.mov",# "s44_p_swbx2n.25fps.mov", \
                 "s45_l_bbwc6s.25fps.mov",# "s45_p_swin1n.25fps.mov", \
                 "s46_l_bbaf8s.25fps.mov",# "s46_p_swwl2a.25fps.mov", \
                 "s47_l_bbab6p.25fps.mov",# "s47_p_swbv8s.25fps.mov", \
                 "s48_l_bbba9a.25fps.mov",# "s48_p_swwj2n.25fps.mov", \
                 "s49_l_bban7a.25fps.mov",# "s49_p_swwq5s.25fps.mov", \
                 "s50_l_bbah8n.25fps.mov",# "s50_p_swiczp.25fps.mov", \
                 "s51_l_bbbg5s.25fps.mov",# "s51_p_swii2n.25fps.mov", \
                 "s52_l_bgbq4p.25fps.mov",# "s52_p_swwr3s.25fps.mov", \
                 "s53_l_bbaf8n.25fps.mov",# "s53_p_swwf6a.25fps.mov", \
                 "s54_l_bbaozp.25fps.mov",# "s54_p_swiy2p.25fps.mov", \
                 "s55_l_bbbhzn.25fps.mov",# "s55_p_srwp2s.25fps.mov"  
]

# List for the reference points
refPt = []

def click_rect(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		# draw a rectangle around the region of interest
		cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("frame", frame)


# dlib init face detector and face landmarks predictor
face_detector = dlib.get_frontal_face_detector()
landmarks_predictor = dlib.shape_predictor(os.path.join("/home/serafeim/audio-visual-thesis/shape_predictor","shape_predictor_68_face_landmarks_GTX.dat"))
## Function definitions
BGR_2_RGB = lambda a : a[:,:,::-1] # transformation from BGR to RGB
# transormation more any 2 point rect reference to dlib rect... (Left,Top),(Right, Bottom)
RECT_2_DLIB_RECT = lambda a : [(min(a[0][0],a[1][0]), min(a[0][1],a[1][1])), (max(a[0][0],a[1][0]),max(a[0][1],a[1][1]))]
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


def get_first_frame(face_detector, video, op=None):
    """ 
    print first frame and 
    show it with the 
    """
    vs = cv2.VideoCapture(video)
        
    ret, frame = vs.read() #Note: FileVideoStream adds extra None type frame at the end of the pipe.
    if ret == False:
        return False
        ## want to raise exeption 
    
    # resize, and convert input frame to grayscale
    # smaller size images makes it faster but with the risk of not recognizing smaller faces(under 80x80px)
    # img = imutils.resize(frame, width=500)
    # img = BGR_2_RGB(frame)
    # dets = face_detector(img, 1) 
    # facedetector works better on grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dets = face_detector(gray, 1) 

    frame = cv2.rectangle(frame, (dets[0].left(), dets[0].top()), (dets[0].right(), dets[0].bottom()),    #(left, top) and (right, bottom)
                    color=(0, 255, 0), thickness=3)
    vs.release()
    return frame

    # cv2.destroyAllWindows()


if __name__ == "__main__":
    ## Parameters
    dir_front = '/run/media/serafeim/1TB SSD/lombardgrid/25fps/'

    # cv2 window setup 
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click_rect)

    # dlib init face detector and face landmarks predictor
    face_detector = dlib.get_frontal_face_detector()
    
    for n in listofvideos:
        frame = get_first_frame(face_detector, os.path.join(dir_front, n))
        
        # emulating do while behavior
        cv2.imshow("frame", frame)
        key = cv2.waitKey(-1) & 0xFF
        if key == ord('s'):
            rec = RECT_2_DLIB_RECT(refPt)
            print(f"'{n}':{refPt}vs{refPt}")
        while key != ord('s') and key != ord('q'):
            frame = get_first_frame(face_detector, os.path.join(dir_front, n))
            cv2.imshow("frame", frame)
            key = cv2.waitKey(-1) & 0xFF
            if key == ord('s'):
                rec = RECT_2_DLIB_RECT(refPt)
                print(f"'{n}':{rec}vs{refPt}")
        
        if key == ord('q'):
            break
        
