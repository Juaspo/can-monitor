# can-monitor
Monitor can messages

To run GUI through SSH (Putty):

RPi:
Links:
https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/


Install X window
[sudo apt-get update]
[sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox]

(may be needed)
[sudo apt-get -y install nodm matchbox-window-manager]

Windows:
Install Xming on windows https://sourceforge.net/projects/xming/files/latest/download
Run Xming before starting SSH session.
Enable X11 forwarding Connection - SSH - Enable X11 forwarding
