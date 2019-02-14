# climate-station
Functionalities of these files are the following:

  -Main.py: Code written in Python that reads sensor's measures and uploads the data to two ThingSpeak channels. In free ThingSpeak channels only 15s sample time is available; to measure in 10s two channels are used with 20s sample time.
  
  -EstacionMeteorologica.html: Data from both ThingSpeak channels are dowloaded. After data reconstruction (separated in two channels) graphs are done by Google Charts in which variables' evolution is shown.
  
  -AnalisisDatos.m: Using Matlab data is downloaded from ThingSpeak and analyzed. A simple fuzzy control is implemented.

