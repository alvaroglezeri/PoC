from io import BufferedReader
from math import ceil

from core.logger import DCL, CATEGORY

class SongData():
    def __init__(self, file: BufferedReader, path: str, fileData = None) -> None:
        self._file = file
        self._path = path
        self._fileData = fileData

    def __eq__(self, other): 
        if not isinstance(other, SongData):
            return False
        else:
            return self.__hash__() == other.__hash__()
        
    def __hash__(self):
        return hash(self.getPath())
    
    def __repr__(self):
        return f'Song: {self.getFileDataSummary()}'
    
    def getTitle(self) -> str:
        try:
            return self._fileData.title
        except:
            return '(No name)'
   
    def getFile(self) -> BufferedReader:
       return self._file
   
    def getPath(self) -> str:
        return self._path
    
    def getFileDataSummary(self) -> str:
        """
        DOCUMENT
        """
        def secToMin(seconds) -> str:
            min = int(seconds // 60)
            sec = ceil(seconds - min*60)
            return f'{min}:{sec}'
        
        try:
            title: str = self._fileData.title
            author: str = self._fileData.albumartist
            length: str = secToMin(self._fileData.duration)
            return f'{title} - {author} ({length})'
        except Exception as e:
            DCL.log(CATEGORY.ERROR, "songData.getFileData()", e)
            return f'Unknown song - Unknown artist ({self.getPath()})'
    
    