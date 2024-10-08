import dependencies
from core.soundlight import SoundLight
import os
import warnings

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sl = SoundLight()

            sl.addFileFromPath(r"resources/Oden & Fatzo, Camden Cox - Lady Love.mp3") 
            sl.selectFile(0)
            sl.analyze()
            
            #sl.addFileFromPath(r"resources/CamelPhat, Yannis, Foals - Hypercolour.wav") 
            #sl.selectFile(1)
            #sl.analyze()
    except:
        pass