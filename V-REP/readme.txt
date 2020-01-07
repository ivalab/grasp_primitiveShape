This is the Ubuntu release V3.6.2, rev. 0, 64bit

****************************
****************************
FROM THE COMMAND LINE, run

$ ./vrep.sh 

to launch V-REP
****************************
****************************



**********************************
Various issues you might run into:
**********************************

1. When trying to start V-REP, following message displays: "Error: could not find or correctly load the V-REP library"
	a) Make sure you started V-REP with "./vrep.sh" FROM THE COMMAND LINE
	b) check what dependency is missing by using the file "libLoadErrorCheck.sh"

2. You are using a dongle license key, but V-REP displays 'No dongle was found' at launch time.
	a) See below



***************
Using a dongle:
***************

a) $ lsusb
b) Make sure that the dongle is correctly plugged and recognized (VID:1bc0, PID:8100)
c) $ sudo cp 92-SLKey-HID.rules /etc/udev/rules.d/
d) Restart the computer
e) $ ./vrep.sh

