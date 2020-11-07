# Connecting to Vintage Tektronix TDS 700 series Oscilloscopes with Python and Ethernet

In this repository is a python script, _TdsCapture.py_,  that uses the Prologix GPIB-ETHERNET (GPIB-LAN) Controller to perform  color or black and white screen captures of the TDS754A scope.   This script should work for all the color and black and white Tektronix scopes made during the same time period (i.e. TDS 500 series, TDS 600 series, and TDS 700 series).

The full description of the project and how to install is described in [www.surfncircuits.com](https://surfncircuits.com/?p=3626)

![Tektronix TDS754A Oscilloscope Front Panel](https://github.com/drkmsmithjr/TdsScopeCapture/blob/master/Scope-Image.jpg)

![Prologix GPIB-Ethernet Controller Attached to TDS754A Oscilloscope ](https://github.com/drkmsmithjr/TdsScopeCapture/blob/master/GPIB-Connection.jpg)

##Setup and required python 3 libraries
* 'pip3 install pyvisa'
* 'pip3 install pyvisa-py'
* 'pip3 install tqdm'
