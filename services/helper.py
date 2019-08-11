"""

#from pydub import AudioSegment
#AudioSegment.ffmpeg = r"C:\Users\EricM\Documents\Voice-assistant\ffmpeg-20190811-2828f5b-win64-static\bin\ffmpeg.exe"
#AudioSegment.converter = r"C:\Users\EricM\Documents\Voice-assistant\ffmpeg-20190811-2828f5b-win64-static\bin\ffmpeg.exe"
import os
from playsound import playsound

#playsound(r'C:\Users\EricM\Documents\Voice-assistant\temporary.mp3')
def speed_swifter(sound, speed=1.0):
    return sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})


in_path = r'C:\Users\EricM\Documents\Voice-assistant\temporary.mp3'
ex_path =r"C:\Users\EricM\Documents\Voice-assistant"
ex2_path = r"C:\Users\EricM\Documents\Voice-assistant"



from pydub import AudioSegment
sound = AudioSegment.from_file(r'C:\Users\EricM\Documents\Voice-assistant\temporary.mp3')

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


slow_sound = speed_change(sound, 0.75)
slow_sound.export(os.path.join(ex_path, 'slower.mp3'), format="mp3")

fast_sound = speed_change(sound, 1.2)
fast_sound.export(os.path.join(ex2_path, 'faster.mp3'), format="mp3")
"""

