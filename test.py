from notifu import notifu

def cbmsg(subject, msg):
	print subject+": "+msg

n = notifu()
n.connect()
n.login("soeren", "gelnhausen")
n.setMessageCallback(cbmsg)
n.sendMessage("soeren", "TEST LIB", "TEST LIB PYTHON")
n.startReading()
import time
time.sleep(5)
n.stop()

