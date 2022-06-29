# Log video and audio file info
#   video: name, duration in secconds, fps, total frames
#   audio: name, duration in secconds, total samples, and "total samples"/"total frames" ration
#   also lists the corrupted files, 

from numpy import append
import librosa
import cv2
import subprocess
import os
from os.path import join


if __name__ == "__main__": 
    dir_audio = "/run/media/serafeim/1TB SSD/lombardgrid/audio"
    dir_front = "/run/media/serafeim/1TB SSD/lombardgrid/front"

    titles = ["name", "no#", "seconds", "fps", "samples", "frames", "ratio"]
    print("\"name\",\"no#\", \"seconds\", \"fps\", \"samples\", \"frames\", \"ratio\"")
    names   = [ n.split('.')[0] for n in os.listdir(dir_audio) if n.endswith(".wav") ]
    corrupt = []
    no      = []
    dure    = []
    # srate   = []
    fps     = []
    samples = []
    frames  = []
    ratio   = []

    # cmd = "ffmpeg -i \"{}.mov\" -map 0:v:0 -c copy -f null -y /dev/null 2>&1 | grep -Eo 'frame= *[0-9]+ *' | grep -Eo '[0-9]+' | tail -1"

    for i, n in enumerate(names):
        # f = subprocess.run(cmd.format(join(dir_front, n)), shell=True, stdout=subprocess.PIPE)
        # try:
        #     l = int(f.stdout.decode("utf-8"))
        # except:
        #     corrupt.append(n)
        #     continue
        cap = cv2.VideoCapture(join(dir_front, n+".25fps.mov"))
        if not cap.isOpened():
            corrupt.append(n)
            continue
        d   = librosa.get_duration(filename = join(dir_audio, n+".wav"))
        sr  = librosa.get_samplerate(join(dir_audio, n)+".wav")
        f   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fs  = cap.get(cv2.CAP_PROP_FPS)
        s   = d * sr
        r   = s/f
        no.append(i)
        dure.append(d)
        # srate.append(sr)
        fps.append(fs)
        samples.append(s)
        frames.append(f)
        ratio.append(r)
        print (f"\"{n}\", {i}, {d}, {fs}, {s}, {f}, {r}")

    print(f"seconds max: {max(dure)}, min:{min(dure)}")
    print(f"fps     max: {max(fps)}, min:{min(fps)}")
    print(corrupt)