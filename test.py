from notifu import notifu

def cbmsg(subject, msg):
	print subject+": "+msg

n = notifu()
n.connect()
n.login("user", "pw")
n.setMessageCallback(cbmsg)
n.sendMessage("soeren", "TEST LIB", "TEST LIB PYTHON")
n.startReading()
import time
time.sleep(2)
n.stop()

