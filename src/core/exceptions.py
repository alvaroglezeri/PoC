class DuplicateElementException(Exception):
    def __init__(self, msg=f'This element is already registered.'):    
        super().__init__(msg)

class NotFoundException(Exception):
    def __init__(self, msg=f'This element cannot be found.'):            
        super().__init__(msg)

class InvalidFileException(Exception):
    def __init__(self, msg=f'This file is invalid.'):            
        super().__init__(msg)

class CodecConversionExeption(Exception):
    def __init__(self, msg=f'A codec conversion must be performed.'):
        super().__init__(msg)
    