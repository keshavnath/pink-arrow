# uas-rec
My Repository for the UAS Software Recruitment Task

**Python-OpenCV Script to detect a _Red Arrow_ from the webcam feed, and determine the angle from the vertical.**

To use, simply run the python script on a device with a webcam.
Three videos will be visible:- Frame (Final Result with Circle and Angle), Mask and Coloured Mask.
**To exit the script and shut the videos, simply press the 'Q' Key.**

Make sure Arrow is red (most shades can be detected perfectly), and try to ensure that the Webcam does not auto-focus some other object (like faces) as it can cause color change

_Script.py is well-documented with comments. All lines and segments of code have been explained._

> Uses Contours and HSV-Masks to detect Red Arrows.

> Uses Erosion, Opening and Closing Morphology for Noise Reduction.

> Uses fitEllipse to detect center and Angle from vertical

> Draws a circle around the arrow and shows Angle from vertical.


_OBSOLETE_ - practice1.py -> Practice of rotation and scaling of a template/image
