import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'Loading {__name__}...')

print(f' 𝈩 Base path: {BASE_PATH}')
print(f' 𝈩 Package name: {__package__}')
#sys.path.append(BASE_PATH)