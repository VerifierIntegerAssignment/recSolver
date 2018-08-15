import subprocess, threading

class Command(object):
    
    output=None
    err=None
    
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            #print 'Thread started'
	    try :
            	self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            	self.output, self.err = self.process.communicate()
            	if self.output is not None and self.output.strip()=='':
                	self.output=None
            #print 'Thread finished'
       	    except Exception as e:
       	    	self.output='Memory Error'

	if self.output=='Memory Error':
		self.output='Termination Failed'
        	return self.output
        
	
	thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            #print 'Terminating process'
            self.process.terminate()
            thread.join()
            self.output='Termination Failed'
        return self.output

#command = Command("./input_program")
#print command.run(timeout=30)
#command.run(timeout=1)
