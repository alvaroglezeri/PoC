import os
# Define the __all__ variable
__all__ = ["analysis", "exceptions", "logger"]

print(f'Loading package "{__name__}":')
print(f' > Root package: {__package__}')
print(f' > {os.path.dirname(__file__)}')
for m in __all__:
    print(f'   ┣ {m}')
print()

# Import the submodules
from . import analysis
from . import exceptions
from . import logger