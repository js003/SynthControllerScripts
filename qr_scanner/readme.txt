Install uvc: 
Needed:
sudo apt install libusb-1.0-0-dev
sudo apt install nasm

Follow instructions:
https://github.com/pupil-labs/pyuvc

Don't forget to install pyuvc itself:
git clone https://github.com/pupil-labs/pyuvc.git
cd pyuvc
sudo python3 setup.py install

Install Opencv:
sudo apt install python3-opencv

Install qr reader:
sudo apt install libzbar0 libzbar-dev
pip3 install pyzbar
