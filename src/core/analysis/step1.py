import allin1.analyze
import allin1.sonify
import allin1.visualize
import librosa
import numpy as np
from typing import BinaryIO
from deeprhythm import DeepRhythmPredictor
import allin1


class KeyAnalysis():
    
    # Define the mapping of chroma features to keys
    CHROMA_TO_KEY = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    @staticmethod
    def getKey(file: BinaryIO) -> str:
        """
        DOCUMENT
        https://medium.com/@oluyaled/detecting-musical-key-from-audio-using-chroma-feature-in-python-72850c0ae4b1
        """   
        # Load the audio file from the beginning: https://github.com/bastibe/python-soundfile/issues/333
        # PROBLEM: Take note of this
        file.seek(0)  
        y, sr = librosa.load(file)

        # Compute the Chroma Short-Time Fourier Transform (chroma_stft)
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

        # Calculate the mean chroma feature across time
        mean_chroma = np.mean(chromagram, axis=1)

        # Find the key by selecting the maximum chroma feature
        estimated_key_index = np.argmax(mean_chroma)
        estimated_key = KeyAnalysis.CHROMA_TO_KEY[estimated_key_index]

        return estimated_key
    
    
class BeatAnalysis():
    @staticmethod
    def getBeat_deeprhythm(file: BinaryIO) -> tuple[float, float, list[float]]:
        file.seek(0)
        model = DeepRhythmPredictor(quiet=True)

        #As the audio is loaded with Librosa, it supports loading an BinaryIO file
        bpm, confidence = model.predict(file, include_confidence=True)

        file.seek(0)
        y, sr = librosa.load(file)
        _, beats = librosa.beat.beat_track(y=y, bpm = bpm)
        beats = librosa.frames_to_time(beats, sr=sr)

        return bpm, confidence, beats

    @staticmethod
    def getBeat_AIO(filepath: str) -> tuple[float, list[float]]:
        # FIXME: AIO does not support BinaryIO objects.
        try:
            print(f'Analyzing...')
            result: allin1.typings.AnalysisResult = allin1.analyze(filepath, out_dir='./output')
            print(f'Sonifying...')
            sonified = allin1.sonify(result, multiprocess=False, out_dir='./output')
            print(f'Visualizing...')
            figure = allin1.visualize(result, multiprocess=False, out_dir='./output')
        except Exception as e:
            print(e)
            raise
        return result        
    
    @staticmethod
    def getBeat_librosa(file: BinaryIO) -> float:
        # Load the audio file        
        file.seek(0)
        y, sr = librosa.load(file)

        bpm, beats = librosa.beat.beat_track(y=y ,sr=sr)

        pulse = librosa.beat.plp(y=y, sr=sr)
        beats_plp = np.flatnonzero(librosa.util.localmax(pulse))

        data: dict = {
            'beat_track': (bpm, beats), 
            'plp': (beats_plp)
        }

        return data 
    
    
    
    
    