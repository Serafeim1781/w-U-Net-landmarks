# subprocess.run is called with shell=True 
# please review the code before running!!! 

# quick workaround for lack of bash fluency
# simple snipset loops throught all video files on dataset
# or asign the task to multiple processes if available
# and upsamples(w/motion interpolation) them to contastand 25fps
# using multiprocessing, subprocess and ffmpeg

from tqdm import tqdm # an alternative https://github.com/dubovikmaster/parallelbar
import subprocess
import os
from os.path import join
dir_front = "/run/media/serafeim/1TB SSD/lombardgrid/front"

def ffmpegMInterpolation( n):
    dir_front = "/run/media/serafeim/1TB SSD/lombardgrid/front"
    
    # ffmpeg command for video interpolation to 25 fps reminder the original videos have variable fps around 24
    # 
    # -i, the input video to procces 
    # -crf 10, lowering crf to minimize Generation loss
    # -vf, video filter to apply
    #     "minterpolation=fps=25", motion interpolation to 25 fps more ingo on parameters
    #     follow the link https://ffmpeg.org/ffmpeg-filters.html#minterpolate
    cmnd = "ffmpeg \
            -i \"{}.mov\" \
            -crf 10 \
            -vf \"minterpolate=fps=25:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1\" \
            \"{}.25fps.mov\""

    # CATION subprocess.run WITH shell=True !!!!!!!!!!
    # CATION subprocess.run WITH shell=True !!!!!!!!!!
    # CATION subprocess.run WITH shell=True !!!!!!!!!!
    video_file = join(dir_front, n)
    subprocess.run(cmnd.format(video_file, video_file), shell=True,\
                   check=True)#, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL) 
    # and output rediction to /dev/null for quiet

if __name__== "__main__":

    # ignore the ones allready proccesed, if there are any..
    ignore  = [ n.split('.')[0] for n in os.listdir(dir_front) if n.endswith("25fps.mov") ]
    # extend the ignore list to include known faulty (invalid/silent) videos 
    ignore.extend( [ "s28_l_gik8a_WRONG_#sil", "s27_l_bah2s_WRONG_#sil", \
                 "s32_l_pwip9p", "s32_p_bwwj2n", "s33_l_pwajza", \
                 "s33_p_sgwq2s" ] )
    
    # List every non proccessed valid video. 
    names   = [ n.split('.')[0] for n in os.listdir(dir_front) \
                                if not n.endswith("25fps.mov") and n.endswith(".mov") ]
    # Using ignore as filter
    names   = [ n for n in names if n not in ignore ]


    if os.cpu_count() <= 2:
        # too few cores, no benefits for multiprocessing
        for n in tqdm(names, len(names)):
            ffmpegMInterpolation(n)
    
    else:
        # More than 2 cores, so there could be a benefit 
        import multiprocessing

        # Initialize the workers. Two less than the system available cores...
        p = multiprocessing.Pool(os.cpu_count() - 2)
        # Schedule work to workers
        p.imap_unordered(ffmpegMInterpolation, names, 100)
        
        # Wait for job to finish
        p.close()
        p.join()

