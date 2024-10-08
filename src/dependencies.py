from importlib.metadata import version
print(version('numpy'))

#------------------------

print(f'Importing numpy... ', end='')
try:
    import numpy
    print(f'Done')
except Exception as e:
    print(f'Error importing "numpy"')
    print(e)

print(f'Importing librosa... ', end='')
try:
    import librosa
    print(f'Done')
except Exception as e:
    print(f'Error importing "librosa"')
    print(e)

print(f'Importing tinytag... ', end='') 
try:
    import tinytag
    print(f'Done')
except Exception as e:
    print(f'Error importing "tinytag"')
    print(e)

print(f'Importing typing... ', end='')
try:
    import typing
    print(f'Done')
except Exception as e:
    print(f'Error importing "typing"')
    print(e)

print(f'Importing ffmpeg... ', end='')
try:    
    import ffmpeg
    print(f'Done')
except Exception as e:
    print(f'Error importing "ffmpeg"')
    print(e)

print(f'Importing Cython... ', end='')
try:    
    import Cython
    print(f'Done')
except Exception as e:
    print(f'Error importing "Cython"')
    print(e)

print(f'Importing madmom... ', end='')
try:    
    import madmom
    print(f'Done')
except Exception as e:
    print(f'Error importing "madmom"')
    raise e

print(f'Importing deeprhythm... ', end='')
try:    
    import deeprhythm
    print(f'Done')
except Exception as e:
    print(f'Error importing "deeprhythm"')
    print(e)

