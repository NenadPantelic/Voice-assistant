# Voice assistant Lindo
Voice assistant project based on speech recognition and text-to-speech synthesis. Done as part of the graduation thesis. The project is developed in Python3. Voice-assistant (named Lindo) is a Linux voice assistant based on the Speech recognition Python library. Speech recognition library supports multiple cloud API speech-to-text services. I tested some of them:

- Google speech-to-text
- Google Cloud
- IBM 
- Microsoft Azure
- Microsoft Bing (before deprecation)
- Wit.ai
- Houndify
- Pocket Sphinx

The best results were achieved with Google's services - Google and Google Cloud. The problem with Google Cloud is that it is not free - up to 60 minutes of converted audio data is free on monthly basis (at the moment of creation of this assistant - July/August/September 2019th).
For the basic usage of speech conversion to text, you need to install SpeechRecognition library.
```sh
pip3 install SpeechRecognition
```
Currently, Lindo/a  supports English and Serbian language (my native language). If you want to add some operating language, feel free to do that.

# Installation
The voice assistant offers services that require the assistance of other modules, libraries, and APIs. All of them are listed in the requirements.txt file. Most of them could be installed with pip. This project was developed under the Linux operating system, but also tested on Windows 10 OS. So, some comments are provided in requirements.txt. If you want clear, all-at-once installation, remove comments from requirements.txt and use: 
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

After dependencies installation, try to install pocketsphinx. Most of the other API services are available to use without any additional installation. Also, most of them (the "web" ones), requires credentials in the form of the API key. For further instructions refer to this page: <https://github.com/Uberi/speech_recognition>

# Functionalities

Functionalities that Lindo/a provides:
- get weather forecast at some location
- get top movies by IMDB (Internet Movie Database) - up to 250
- get details about some movie from IMDB
- get summary about some term on Wikipedia
- send an email to some address
- translate some text (from any supported language to any other)
- search and open some page on Google
- open social network account page
- control OS (in development)
- control any actuator with Arduino (tested on light bulb)


# How it works?

There are many use-cases for both languages. Generally, it is important to know how commands recognition works.  When you say some command, the recognizer returns the text (recognized from the speech) and that text is being processed. At first, any punctuation marks are removed. After that usual words that can be found in communication to Lindo/a are removed (these words are stored in __data/words/words-<en/sr>.json__ based on language choice).  
The most important thing when determining which command user wants is the existence of keywords in the command. Keywords for every non-setup command can be found in __data/keywords/keywords-<en/sr>.json__. So, when the user says something and text is processed as was described, based on keywords in that command, the command with the highest score is chosen (score is calculated for every command based on words that determines that command, and the one with the highest score is chosen). As we will see, there are commands where keywords are removed from the text and that text is used as an argument in the appropriate method call.
Based on the rest of the words, the command is being determined. Command's structure can be found in __data/commands/commands.json__. Explanation of the structure goes next:
- command_id : id of the command
- service: name of the service
- method: name of the executing method
- has_args: boolean flag (does method accepts arguments or not)
- arg_type: type of the argument (if has_args is true)
- need_input: boolean, does method needs keyboard input, if the input should be very precise (e.g. email address when sending an email)
- process_input_text: boolean, if the text that was got from speech should be processed (if keywords should be removed from text).
- input_processing_method: method that should process text before it goes to the executing method as an argument
- tag: mark of command; from the set {initial, final, invalid, ambiguous}
- is_ready: boolean, only commands with is_ready true are executed
- next_command_id: command that goes after current command
- messages: a dictionary that holds messages when command is successfully executed, and when execution failed (with language choice)
- descriptions: descriptions of the command on every possible operating language

## How command is determined?
In this subsection, it will be described how to say commands, so that assistant recognizes them without doubt. 
As it was described in the previous subsection when you say some command, the text is processed and the command is determined. It is very important whether process_input_text is true or not.  For command where process_input_text is true, recognized text (after obligatory processing - removal of usual words and punctuation), is being processed so keywords are removed.  Everything that "survives" this processing is being regarded as an argument to the execution method. 
One example could look like this:
Let's say you want to know what is the weather forecast in Denver (USA).  We will use english-case scenario. Command that does that has true value for process_input_text. Keywords for this command are:  

"words":{
   "how":0.2,
   "what":0.2,
   "what's":0.2,
   "whats":0.2,
   "is":0.1,
   "will":0.1,
   "be":0.1,
   "weather":0.4,
   "forecast":0.4,
   "like": 0.15,
   "temperature":0.3,
   "humidity":0.3,
   "pressure":0.3,
   "wind":0.3,
   "clouds":0.3,
   "snow":0.3,
   "rain":0.3,
   "location":0.2,
   "place":0.2,
   "city":0.2
}  

Every word in this group has some value, and it represents it's score coefficient. For every command in __data/keywords/keywords-<en/sr>.json__, score is calculated on principle, for every known word in word list for that command calculate how many times word repeats and multiply with it's score, then sum it all up and get total score for that command. Command with the highest score wins. Now, let's get back to our example - weather forecast in Denver. 
If we say: ***What's the weather like at location Denver*** - will successfully return forecast details.
On the other side: ***What's the weather like around Denver*** will return notification that weather forecast details cannot be fetched.  

Explanation:  

Phrase ***What's the weather like at location Denver*** is processed (obligatory) so we get ***what's weather location denver***. After that,  keywords are removed, so we get only ***denver*** and that is sent to the appropriate method as an argument.  

Phrase ***What's the weather like around Denver*** will follow the same procedure, but the result that will be given to the method as an argument is ***around denver*** and that will cause unsuccessful operation. If we add word ***"around"*** in the keywords list for this command, it will also be removed, and only location name (***denver***)  will be used as an argument.

# Usage

To start Lindo voice assistant, type:
```
python3 main.py
```

The first command the application starts with is the initial command. The initial command is to greet the user and ask him or her to select the operating language. The initial message looks like this:  

***en: Hi, I’m Lindo voice assistant. Choose the operating language. The default option is English!***
***sr: Zdravo, ja sam Lindo glasovni asistent. Izaberite operativni jezik. Podrazumevani jezik je engleski!***

The user selects one of the offered languages (English or Serbian), and if he tries to select one of the non-existent languages, he will receive an error:  


***en: I have some problems with the language setting. Be kind to try again. The only options are English and Serbian. Speak clear and loud!***  
***sr: Imam problema sa postavkom jezika. Jedine opcije su engleski i srpski. Budi ljubazan da probaš opet. Govori jasno i glasno!***  

The user is then expected to repeat the command, ie. chooses the operating language.

After the message, the user should select one of the operating languages (English or Serbian). When selecting a language, any form of command that contains a language name is valid. Therefore, for the choice of English it is important that the command contains any of these words: ***english, default, engleski, podrazumevan (podrazumevani, podrazumevana)***. To select Serbian, the command should contain one of the words: ***serbian, srpski***.

For example, these commands could be:  

***en: Hi Lindo, I'm choosing English!***  
***sr: Zdravo Lindo, moj izbor je srpski!***  

To change the operating language, keywords are:
***promeni, izbor, zameni, jezik, operativni, novi и switch, change, replace, language, operating, new***

According to the keywords, these could be commands:
- ***Promeni operativni jezik.***
- ***Zameni operativni jezik.***
- ***Switch the operating language.***
- ***Change the operating language.***

## Usage examples

After clarifying how Lindo works, a demonstration of functionality follows. In each of the examples of functionality, a list of keywords for that functionality command, will be provided. The following is a list of common words by Lindo, for English and Serbian.  

***English:***

```json
{
   "usual_words":[
      "lindo", "linda", "please", "should", "could","tell", "say", "listen", "speak", "help", "hello", "hi", "bye", "good bye",
      "yo", "the", "a", "an"
   ],
   "conjunctions":[
      "and", "or", "nor", "for", "but", "yet", "so"
   ],
   "pronouns":[
      "i", "you", "he", "she", "it", "we", "they", "me", "them",    "her", "his"
   ],
   "prepositions":[
      "at", "in", "to", "of", "by"
   ]
}
```

***Serbian:***

```json
{
   "usual_words":[
      "lindo", "linda", "molim", "treba", "možeš", 
      "hoćeš", "reći", "reci", "kaži", "slušaj", 
      "govori", "pomozi", "pomogneš", "kažeš",
      "zdravo", "ćao", "pozdrav", "ej", "hej"
   ],
   "conjunctions":[
      "i", "ili", "ni", "za", "ali", "već", "pa", "niti" 
    ],
   "pronouns":[
      "ja", "ti", "on", "ona", "ono", "mi", "oni", "mene", "tebe",
      "tobom", "njega", "njih", "nju",
   ],
   "prepositions":[
      "kod", "u", "na", "ka", "od", "sa"
   ]
}
```

## Examples:



## Special cases

There are cases when special commands are called:
- initial command (says greeting text and asks for the input text)
- setting language (sets the operating language)
- switch language (switches the operating language)
- ambiguous command (scenario when multiple commands have the same score):
   - ***en: I’m sorry, but I’m not sure what you want. Your command is ambiguous. There are a few options. Try again,            please!***,
   - ***sr: Žao mi je, ali nisam siguran šta želite. Vaša komanda nije jednoznačna. Postoji više mogućih opcija. Probajte        ponovo!***
    
- invalid command (command cannot be determined precisely)
- final command (last calling command)

Also, there may be situations where speech recognition returns an error:
- speech cannot be processed:
   - ***en: Speech cannot be analyzed or recognized!***,
   - ***sr: Vaš govor ne može biti obraden ili prepoznat!***
- API problems:
   - ***en: Request error problem. Check API limits and connectivity status!***,
   - ***sr: Problemi sa slanjem zahteva. Proverite API limit i status mreže!***
## Aditional notes

- To use arduino service, you must connect arduino with your computer (serial port's parameters are set in config/config.py); uncomment arduino service line in service pool in main.py
- operating system control is under construction. Linux commands execution are tested as the proof-of-concept, but the goal is to also add Windows commands, so until then OS service is not used.
