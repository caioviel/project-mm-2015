from threading import Thread, Event, Semaphore
import subprocess as sp
import logging

class AVConverter (Thread):
    CONVERTER_NAME  = 'avconv'
    pass

    def __init__(self, params, verbose=False):
        Thread.__init__(self)
        self.params = params
        self.verbose = verbose
        
        self.__subprocess = None
        self.__forced_stop = False
        self.err_mng = None
        self.__process_running = False
        self.__end_mutex = Semaphore()
        self.__exit_status = 0
        self.__avconv_finished = Event()
        self.__avconv_finished.clear()
            
    def run(self):
        cmd = [self.CONVERTER_NAME] + self.params
        logging.warning('Transcoding Command: ' + str(cmd))
        try:
            self.__process_running = True
            if self.verbose:
                self.__subprocess =  sp.Popen(cmd)
            else:
                self.__subprocess =  sp.Popen(cmd, stderr=sp.PIPE, stdout=sp.PIPE)
        except:
            logging.exception("Error on starting Transcoding Process")
        
        logging.debug("Threading Waiting for avconv die.")
        self.__subprocess.communicate()
        logging.debug("avconv died.")
        
        self.__end_mutex.acquire()
        self.__process_running = False
        self.__exit_status = self.__subprocess.returncode
        self.__end_mutex.release()
        
        self.__avconv_finished.set()
        
        logging.debug("Transcoding return code: %s", str(self.__exit_status))
        
        if not self.__forced_stop and self.__exit_status < 0:
            #Get the error message from pipe
            out_file = self._subprocess.stderr
            if out_file != None:
                line = out_file.readline()
                previous_line = line
                while line:
                    previous_line = line
                    line = out_file.readline()
                    previous_line = previous_line[:len(previous_line)-1]
            
                #error = err.Error(err.Error.RECORDING, [previous_line], 'avconv instance stooped abruptly')
                #if self.err_mng == None:
                    logging.error('avconv instance stopped abruptly')
                else:
                    pass
                #self.err_mng.report(error)
                
    def wait_finish(self):
        logging.debug("AVConverter.wait_finish()")
        self.__avconv_finished.wait()
                
    def stop(self, waiting=False):
        logging.debug("AVConverter.stop()")
        self.__end_mutex.acquire()
        if self.__process_running:
            import signal
            self.__forced_stop = True
            try:
                self.__subprocess.send_signal(signal.SIGTERM)
                #self._subprocess.wait()
            except:
                logging.exception("Error killing the recording process")
        self.__end_mutex.release()
        
        if waiting:
            self.wait_finish()
    

def test():
    conv = AVConverter(["-i", 
                        "/home/erick/Desktop/test_video/modulo1_slides.mpeg",
                        "-vcodec", "libx264", "-y",
                        "/home/erick/Desktop/test_video/teste.mp4"], True)
    conv.start()
    conv.wait_finish()
             
if __name__ == "__main__":
    test()