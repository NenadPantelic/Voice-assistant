# Voice assistant Lindo/a
Voice assistant project based on speech recognition and text-to-speech synthesis. Done as part of the graduation thesis. The project is developed in Python3. Voice-assistant (named Linda/Lindo) is a Linux voice assistant based on the Speech recognition Python library. Speech recognition library supports multiple cloud API speech-to-text services. I tested some of them:

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
```sh
pip3 install speech_recognition
```
Currently, Lindo/a  supports English and Serbian language (my native language). If you want to add some operating language, feel free to do that.

# Installation
The voice assistant offers services that require the assistance of other modules, libraries, and APIs.All of them are listed in the requirements.txt file. Each of them could be installed with pip. This project was developed under the Linux operating system, but also tested on Windows 10 OS. So, some comments are provided in requirements.txt. If you want clear, all-at-once installation, remove comments from requirements.txt and use: 
```
pip3 install -r requirements.txt
```

API keys are provided in config/config.py file and can be used (for some time surely). Concretely Open Weather Map and OMDB require an API key for authentication. Also, test email address credentials (for mail sending service) are provided.

## Use another Web API speech-to-text service


As previously mentioned, voice recognition is performed with the SpeechRecognition library that supports multiple API services for speech-to-text conversion. ***Lindo/a*** voice assistant is built with Google's speech-to-text service (abbr. stt). In most of its behavior, this application is modular and easy to change and maintain. So, practically, you can change the stt service, If you want so. To use Google Cloud API, you also need to install google-api-python-client library with the following command:
```
pip3 install --upgrade google-api-python-client
```  
Possibly, you will need to install the oauth2 library for authentication:
```
pip3 install ouath2
```

***NOTE:*** To try Pocket Sphinx module use the following pip command:  
```
pip3 install --upgrade pocketsphinx
```
If you got dependencies errors (swig and pulse), use this:
```
$ sudo apt install libpulse-dev swig
```

After dependencies installation, try to install pocketsphinx. Most of the other API services are available to use without any additional installation. Also, most of them (the "web" ones), requires credentials in the form of the API key. For further instructions refer to this page: <https://github.com/Uberi/speech_recognition/edit/master/README.rst>

# Usage

