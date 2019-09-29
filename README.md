# Voice-assistant
Voice assistant project based on speech recognition and text-to-speech synthesis. Done as part of the graduation thesis. The project is developed in Python3.

Web API choice
-----------------

## Web API choice
Voice-assistant (named Linda/Lindo) is Linux voice assistant based on the Speech recognition Python library. Speech recognition library supports multiple cloud API speech-to-text services. I tested some of them:
- Google speech-to-text
- Google Cloud
- IBM 
- Microsoft Azure
- Microsoft Bing (before deprecation)
- Wit.ai
- Houndify
- Pocket Sphinx

The best results were achieved with Google's services - Google and Google Cloud. The problem with Google Cloud is that it is not free - up to 60 minutes of converted audio data is free on monthly basis (at the moment of creation of this assistant - July/August 2019th). 

For basic usage of speech conversion to text, you need to install SpeechRecognition library
``pip3 install speech_recognition``.
To use Google Cloud API, you also need to install:
google-api-python-client library with the following command:
``pip3 install --upgrade google-api-python-client``
Possibly, you will need to install oauth2 library for authentication (`pip3 install ouath2`).

***NOTE:*** To try Pocket Sphinx module you should use the following pip command:
``pip3 install --upgrade pocketsphinx``
If you got dependencies errors (swig and pulse), use this:
``sudo apt-get install libpulse-dev``
``sudo apt-get install swig``

After this, try to install pocketsphinx. ***Lindo/a*** Voice assistant is built with Google speech-to-text service.


Installing
-----------------

