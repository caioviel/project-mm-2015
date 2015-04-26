#!/usr/bin/env python

import cv2.cv as cv

PROGRAM_NAME = "videonorm"

#TODO: Tratar questao do framerate diferente.

def reduce_video(capture, writer, final_frames_number, skip_step, verbose=False):
    current_frame = 0
    removed_frames = 0
    while current_frame < final_frames_number:
        if verbose:
            my_string = "%.2f" % ( float(current_frame)/final_frames_number*100 )
            print current_frame, '/', final_frames_number, my_string + "%\r",
        
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
            
        cv.WriteFrame(writer, frame)
        current_frame += 1
            
        if current_frame % skip_step == 0:
            removed_frames += 1
            frame = cv.QueryFrame(capture)
            if frame is None:
                break
            
    return removed_frames
    
def expand_video(capture, writer, final_frames_number, duplicate_step, verbose=False):
    current_frame = 0
    added_frames = 0
    while current_frame < final_frames_number:
        if verbose:
            my_string = "%.2f" % ( float(current_frame)/final_frames_number*100 )
            print current_frame, '/', final_frames_number, my_string + "%\r",
        
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
            
        cv.WriteFrame(writer, frame)
        current_frame += 1
            
        if current_frame % duplicate_step == 0:
            added_frames += 1
            current_frame += 1
            cv.WriteFrame(writer, frame)
            
    return added_frames

def normalize_video_lenght(i_name, o_name, fps, length, verbose=False):
    capture = cv.CaptureFromFile(i_name)
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    original_fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    original_frames_number = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT )
    final_frames_number = int(fps*length)
    
    if verbose:
        print '\ninput video: ', i_name
        print 'size: %s:%s' % (width, height), ' fps:', original_fps, 'frames:', \
                original_frames_number, 'estimated length:', float(original_frames_number)/original_fps
        
        print '\noutput video: ', o_name
        print 'size: %s:%s' % (width, height), ' fps:', fps, 'frames:', \
                final_frames_number, 'estimated length:', float(final_frames_number)/fps, '\n'
            
    my_fourcc = cv.CV_FOURCC('m', 'p', 'g', '2')
    writer = cv.CreateVideoWriter(o_name, my_fourcc, fps, (width, height))
    
    diff = final_frames_number - original_frames_number
    step = operation = None
    if diff > 0:    
        step = int(original_frames_number / diff)
        operation = expand_video
    elif diff < 0:
        step = int(final_frames_number / abs(diff))
        operation = reduce_video
    
    if step == 0:
        print 'The desired final length is too short'
        return 1
        
    result = operation(capture, writer, final_frames_number, step, verbose)
    if verbose:
        print 'A total of', result, 'frames were removed/duplicated from the original video.'
        return 0

    
def create_args_parser():
    from optparse import OptionParser
    
    required_args = ("i_file", "o_file")
    
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", type="string", dest="i_file",
                  help="the input video file to be normalized")
    
    parser.add_option("-o", "--output", action="store", type="string", dest="o_file",
                  help="the output video file to be generated")  
    
    parser.add_option("-r", "--framerate", action="store", type="int", dest="fps", default="24",
                  help="frames per second of the output video")
    
    parser.add_option("-l", "--length", action="store", type="float", dest="length",
                  help="the estimated duration for the output video")  
    
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
    
    return parser, required_args


def test():
    i_file = '/home/erick/tvmonitor/SBT_-_2014-02-28T15:49:23.814352_-_0a8cf79c-a0a9-11e3-8def-5cf9ddee136d.mp4'
    o_file = '/home/erick/Desktop/teste.mpeg'
    lenght = 11.009065
    print lenght 
    fps = 24
    normalize_video_lenght(i_file, o_file, fps, lenght, True)
    
def main():
    import sys
    
    parser, required_args = create_args_parser()
    options, _ = parser.parse_args()
    for arg in required_args:
        if getattr(options, arg) == None:
            print "Argument missing. Please try: '%s --help' for instructions" % PROGRAM_NAME
            sys.exit(0)

    
    result = normalize_video_lenght(options.i_file, options.o_file, 
                                    options.fps, options.length, 
                                    options.verbose)
    sys.exit(result)

if __name__ == "__main__":
    test()
    #main()