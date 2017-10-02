Developer: Sai Raghavendra Sankrantipati

Installation Instruction:
  Install PyQt4 and designer
  1. SUDO APT-GET INSTALL PYTHON3-PYQT4
  2. SUDO APT-GET INSTALL QT4-DESIGNER
  Install Adafruit_DHT library
  1.git clone https://github.com/adafruit/Adafruit_Python_DHT.git
  2.cd Adafruit_Python_DHT
  3. sudo apt-get update
  4. sudo apt-get install build-essential python-dev python-openssl
  5. sudo python setup.py install
  
Project Additions:
   1. Process bars are added for displaying Temperature and Humidity (A download bar). % in temperature indicates degree centigrade.
   2. A graph is plotted by collecting 100 samples updating every 5 seconds. So, only last 100 samples are stored.
   3. A button for average of the above collected samples.
   4. A button to add alarm for high limit to tempearture. A window is popped up when refresh button is pushed and temperature is above the limit.

