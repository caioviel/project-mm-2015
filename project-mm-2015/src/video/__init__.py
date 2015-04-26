import videocut, videonorm, avconv
import time

normalize_video_lenght = videonorm.normalize_video_lenght

cut_video_segment = videocut.cut_video_segment

cap = avconv.AVConverter(["-y",
                          "-s",
                          "hd480",
                          "-f",
                          "video4linux2",
                          "-i",
                          "/dev/video0",
                          "-f",
                          "alsa",
                          "-i",
                          "hw:1,0",
                          "-ar",
                          "48000",
                          "-ac",
                          "2",
                          "-c:a",
                          "libvo_aacenc",
                          "-c:v",
                          "libx264",
                          "-qscale",
                          "1",
                          "/home/caioviel/Desktop/capturedfile.mp4"], True)


cap.start()
time.sleep(15)
cap.stop()
