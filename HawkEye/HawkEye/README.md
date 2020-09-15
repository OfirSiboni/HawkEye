# Hawk vision

This is the main repository for hawk the scriptable vision module for FRC teams.
Hawk is a collection of python and shell scripts that FRC teams can use to rapidly implement image processing algorithms for their robots.

# How does it work?
Firstly these scripts run on a single board computer like a raspberry pi.
The board is then connected to your robot using an ethernet cable, you also need to connect USB cameras to your board.
You then need a hawk controller and GRIP(https://github.com/WPIRoboticsProjects/GRIP).
Using these you can configure the video settings, constants and thersholds pipelines etc.
After that, you need to write your image processor functions in Python, and using the controller you can send the file to the single board computer.

# But wait what is the hawk controller?

It is a GUI frontend to hawk which is used to configure it.
GTK python GUI for linux and unix hosted here:
https://gitlab.com/steampunk_software1577/hawk-gtk-controller

And A Qt version for windows users hosted here:
https://gitlab.com/steampunk_software1577/hawk-qt-controller

For further details and instructions please refer to hawk-gtk-controller repository

# Installing
This software is developed and tested on the Raspberry Pi boards as such these boards are officially supported.
Premade images for the Raspberry boards can be downloaded here:
https://uploadfiles.io/jqkq11j2


For other board follow the instructions at creating_an_sd_image.

# License
The support scripts are not licensed because they are under 5 lines of code, as such they are not worth licensing

# Note
The project is in very early stages
Any help is welcomed!
Further more this project is designed specifically for the FRC competition and not for any other purpose!

# Contact
For any request or question you can either submit an issue or email at:

oren_daniel@protonmail.com --original author

steampunk.software@gmail.com
