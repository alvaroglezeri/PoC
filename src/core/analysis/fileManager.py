from core.analysis.songData import SongData
from tinytag.tinytag import TinyTag,TinyTagException, Wave
from pathlib import Path
import ffmpeg
from core.logger import DCL, CATEGORY
from core.exceptions import DuplicateElementException, NotFoundException, CodecConversionExeption, InvalidFileException

SUPPORTED_FORMATS: dict[str, tuple[str, TinyTag]] = {
        'wav': ('wav', Wave)
    }

_DEFAULT_FORMAT: str = 'wav'

class FileManager():    

    def __new__(cls):
        """
        Singleton implementation
        """
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)
            cls.instance.__setup__()
        return cls.instance

    def __setup__(self) -> None:
        # DOCUMENT
        self._files: list[SongData] = list()
        self._selected: SongData = None
        self._convert: bool = True
        # Tuple containing extension and codec class
        self._conversionFormat: tuple[str, TinyTag] = SUPPORTED_FORMATS["wav"]

    def __init__(self) -> None:
        # Empty __init__, so to not rebuild the singleton
        return

    def __del__(self) -> None:
        try:
            for file in self._files:
                DCL.log(CATEGORY.INFO, "FileManager.__del__", f'Closing "{file.getPath()}"...')
                #f: BufferedReader
                file._file.close()
        except:
            pass

    def getLoadedFiles(self) -> list[SongData]:
        return list(self._files)

    def getFilesSummary(self) -> list[str]:
        summary = []

        file: SongData
        for file in self._files:
            summary.append(file.getFileDataSummary())
        return summary
    
    def setConvert(self, mode: bool) -> None:
        DCL.log(CATEGORY.INFO, "FileManager.setConvert", f'Filetype conversion is {"enabled" if mode else "disabled"}')
        self._convert = mode

    def setConversionFormat(self, formatName: str) -> None:
        if str in SUPPORTED_FORMATS:
            self._conversionFormat = SUPPORTED_FORMATS[formatName]
        else:
            self._conversionFormat = SUPPORTED_FORMATS[_DEFAULT_FORMAT]

    def loadFileFromPath(self, path: str) -> None:
        """
        DOCUMENT

        Loads the file and its metadata with tinytag and magic.
        """
        
        DCL.log(CATEGORY.INFO, "FileManager.loadFileFromPath", f'Loading "{path}"...')
        try:
            # FileManager manages the life cycle of the files.
            file = open(path, "rb") # with open(path, "rb") as file:
            
            songTags: TinyTag = TinyTag.get(file_obj=file)
            songTags.codec = {"name": songTags.__class__.__qualname__, "class": songTags.__class__}    # Obtaining file codec from the actual class parsed
            
            # Converting file format to .wav
            DCL.log(CATEGORY.INFO, "FileManager.loadFileFromPath", f'Detected codec: {songTags.codec["name"]}')
            if songTags.codec["class"] != self._conversionFormat[1] and self._convert:
                newPath = self._convertFile(path)
                DCL.log(CATEGORY.INFO ,"FileManager.loadFileFromPath", f'Converted file to {self._conversionFormat[1].__qualname__}')
                raise CodecConversionExeption()
                
            # Building SongData object
            songData: SongData = SongData(file, path, songTags)

            if songData not in self._files:
                self._files.append(songData)
                DCL.log(CATEGORY.SUCCESS, "FileManager.loadFileFromPath", f'Loaded "{path}".')
            else:
                    DCL.log(CATEGORY.ERROR, "FileManager.loadFileFromPath", f'File "{path}" already exists.')
                    raise DuplicateElementException(f'This file is already loaded.')    
        except CodecConversionExeption:
            # If the codec is invalid, we drop the current file and open the new, converted file
            file.close()
            DCL.log(CATEGORY.WARN, "FileManager.loadFileFromPath", f'Reloading file...')
            self.loadFileFromPath(newPath)           
        except DuplicateElementException as dee:
            DCL.log(CATEGORY.ERROR, "FileManager.loadFileFromPath", dee)
            raise dee
        except TinyTagException as tte:
            # PROBLEM: What if the file is not audio?
            DCL.log(CATEGORY.ERROR, "FileManager.loadFileFromPath", f'TinyTag error: {tte}')
            raise InvalidFileException(f'Invalid file because: "{tte}"')
        except Exception as e:
            DCL.log(CATEGORY.ERROR, "FileManager.loadFileFromPath", e)
            raise e

    def _convertFile(self, path) -> str:
        #DOCUMENT
        DCL.log(CATEGORY.WARN, "FileManager._convertFileFromPath", f'Converting file to {self._conversionFormat[1].__qualname__}...')

        #print(Path(path).anchor)
        #print(Path(path).parents[0])

        newPath = f'{Path(path).parents[0]}/{Path(path).stem}.{self._conversionFormat[0]}'
        # PROBLEM: A lot of ffmpeg options were tried to solve 'Format not recognized' errors, until the seek(0) was discovered.
        ffmpeg.input(path, v="quiet").output(newPath).overwrite_output().run()
        
        return newPath

    def hasSelectedFile(self) -> bool:
        return self._selected is not None
             
    def selectFile(self, n) -> None:
        try:
            self._selected = self._files[n]
            DCL.log(CATEGORY.SUCCESS, "FileManager.selectFile", f'Selected "{self._selected.getPath()}"')
        except Exception as e:
            DCL.log(CATEGORY.ERROR, "FileManager.selectFile", e)
            raise NotFoundException()

    def getSelectedFile(self) -> SongData | None:
        if self._selected is not None:
            return self._selected
        else:
            return None

    

