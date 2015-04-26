#!/usr/bin/env python

import logging
import subprocess as sp

def cut_video_segment(i_file, o_file, begin_time, end_time, verbose=False):
    cmd = ['avconv',
           '-ss', "%.2fs" % begin_time,
           '-i', i_file, 
           '-c:v', 'copy',
           '-c:a', 'copy',
           '-same_quant',
           '-t', "%.2fs" % (end_time - begin_time),
           '-y',
           o_file
           ]
    
    if verbose:
        print cmd
    logging.info(cmd)
    
    subprocess = None
    try:
        if verbose:
            subprocess =  sp.Popen(cmd)
        else:
            subprocess =  sp.Popen(cmd, stderr=sp.PIPE, stdout=sp.PIPE)
    except:
        logging.exception("Error recording.")
        if verbose:
            print 'Error trying to initiate the process'
        return -1
        
    logging.debug("Performing the video cutting...")
    if verbose:
        print "Performing the video cutting...\n"
    subprocess.communicate()
    logging.debug("Cutting finished.")
    if verbose:
        print "Cutting finished.."
    
    return subprocess.returncode

class Test():
    pass

def main():
    import sys
    options = Test()
    options.i_file = "/home/caioviel/teste.avi"
    options.o_file = "teste3.avi"
    options.begin_time = 20
    options.end_time = 40
    options.verbose = False
    result = cut_video_segment(options.i_file, options.o_file, 
                      options.begin_time, options.end_time,
                      options.verbose)
    
    sys.exit(result)
    
def test():
    pass
if __name__ == "__main__":
    #test()
    main()