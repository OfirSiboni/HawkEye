![logo](HawkEye.png)
# HawkEye
a lightweight vision system made for FRC teams. Using Machine learning and Deep learning for best results.

## Get Started
To get started, you need to have these requirements:
- Raspberry Pi 3B+ or higher.
- SD card with more than 4 GB of memory(16 GB is recommended)
- raspbian(latest is better)
- this repository in your raspi, installation process mentioned later.
- Stable Wifi connection to your robot. In case that you are not using HawkEYE for FRC purposes, LAN or Wifi connection is okay as well.
- FRC-Legal USB Camera, Default is PSeye, but you can change it manually.

## Installation instructions
  1. Install Raspbian latest version - can be found [here](https://www.raspberrypi.org/downloads/raspbian/).
  2. Install all the [require pip packages](requirements.txt)
  3. fetch the last version of HawkEYE(NOTE: if there is still no public version, you can download the last commit)
  4. Download the last version of [HawkEYE Client For Windows](https://github.com/OfirSiboni/HawkEYE-Client/releases) for your computer.
  5. You are done! you can run HawkEYE freely and change it for your use. Run using `bash hawkeye` to run the `hawkeye.sh` file to run hawkeye properly.
## Usage instructions
HawkEYE's usage is very simple. Once you run the `main.py` file, you can browse to `yourIP:1181`(Default is `192.168.1.6:1181`) and you can see camera input and control.
To manage your HawkEYE system and change it's system options, you need to download HawkEYE client(currently only for Windows, More versions will come up later.)
and follow it's instructions(it's pretty simple, But there will be full instructions for your comfort). you can always connect to your raspi via SSH and check it's status.
## Client
Yes! HawkEYE does have a client for Windows only at this time. You can watch and download from [here](https://github.com/OfirSiboni/HawkEYE-Client/releases)
With HawkEYE client you can set and review all HawkEYE settings, and it's necessary to use it during your experience with HawkEYE. 
## Bugs and Issues
If you experience any issues, please let me know in the [Issues](https://github.com/OfirSiboni/HawkEye/issues) section or [Mail](mailto:ofirsiboni01@gmail.com)
