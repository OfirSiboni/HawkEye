# HawkEye
lightweight vision made for FRC teams. Using Machine learning and Deep learning for best results.

## Get Started
In order to get started, you need to have these requirements:
- Raspberry Pi 3B+ or higher.
- SD card with more than 4 GB of memory(16 GB is recommended)
- raspbian(latest is better)
- this repository in your raspi, installation proccess mentioned later.
- Stable Wifi connection to your robot. In case that you are not using HawkEYE for FRC purposes, LAN or Wifi connection is okay as well.
- FRC-Legal USB Camera, Default is PSeye, but you can change it manually.

## Installation instructions
  1. Install Raspbian latest version - can be found [here](https://www.raspberrypi.org/downloads/raspbian/).
  2. Install all the require pip packages(a completed list of the requirements will be posted later)
  3. fetch the last version of HawkEYE(NOTE: if there is still no public version, you can download the last commit)
  4. Download the last version of [HawkEYE Client For Windows](https://github.com/OfirSiboni/HawkEYE-Client/releases) for your computer.
  5. You are done! you can run HawkEYE freely and change it for your own use. Run using `python3 ~/HawkEYE/source/main.py`
## Usage insturctions
HawkEYE's usage is very simple. Once you runned the `main.py` file , you can browse to `yourIP:1181`(Default is `192.168.1.6:1181`) and you can see camera input and control.
In order to manage your HawkEYE system and change it's system options, you need to download HawkEYE client(currently only for Windows, More versions will come up later.)
and follow it's instructions(it's pretty simple, But there will be full instructions for your comfort). you can always connect to your raspi via SSH and check it's status.
