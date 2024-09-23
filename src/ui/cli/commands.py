from abc import ABC, abstractmethod
from ui.cli.consoleUtils import ConsoleUtils
from core.analysis.fileManager import FileManager
from core.analysis.songData import SongData
from core.analysis.analysisDirector import AnalysisDirector
from core.exceptions import NotFoundException

class Command(ABC):
    
    @abstractmethod
    def getDescription(self) -> str:
        pass

    @abstractmethod
    def getKey(self) -> str:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass


class Exit(Command):
    
    def getDescription(self) -> str:
        return f'Exits out of the program'
    
    def getKey(self) -> str:
        return 'exit'
    
    def execute(self) -> None:
        exit()

   
class AddFile(Command):

    def __init__(self) -> None:
        self._fm = FileManager()
        self._c = ConsoleUtils

    def getDescription(self) -> str:
        return f'Adds a file to the file manager.'
    
    def getKey(self) -> str:
        return 'add'
    
    def execute(self) -> None:
        self._c.clear()
        self._c.printInfo(f'Adding file')
        path = self._c.input(f'Type or paste file path: ')
        self._c.nl()

        file: object
        try:
            self._fm.addFileFromPath(path)
        except OSError as ose:
            self._c.printError(f'The file "{path}" could not be loaded:')
            self._c.printInfo(ose.strerror)
        except Exception as e:
            self._c.printError(f'There was an error adding the file: {e}')
        else:
            self._c.printSuccess(f'File loaded correctly.')
   

class SelectFile(Command):
    def __init__(self) -> None:
        self._fm = FileManager()
        self._c = ConsoleUtils

    def getDescription(self) -> str:
        return f'Opens a file from the file manager.'
    
    def getKey(self) -> str:
        return 'open'

    def execute(self) -> None:
        self._c.clear()
        self._c.printInfo(f'Selecting file.')

        if self._fm.hasSelectedFile():
            self._c.printInfo(f'The file "{self._fm.getSelectedFile().getFileDataSummary()}" is already selected.')
        else:
            self._c.printInfo(f'No file is currently selected.')
        
        self._printAvailable()

        self._c.nl()
        if self.nFiles != 0:
            fileN = int(self._c.input(f'Select file number:'))

            if type(fileN) is not int:
                raise Exception(f'Invalid value. Input only the file number.')
            
            try:
                self._fm.selectFile(fileN - 1) # The list in the UI starts with 1
                selectedFile: SongData = self._fm.getSelectedFile().getFileDataSummary()
                
                if selectedFile is None:
                    raise NotFoundException()
                
                fileSummary = self._fm.getSelectedFile().getFileDataSummary()
                self._c.printSuccess(f'Selected "{fileSummary}".')
            except NotFoundException:
                self._c.printWarn(f'The file could not be selected.')
            except Exception as e:
                self._c.printError(f'An error has occurred: {type(e)}.')
                self._c.print(e)

    def _printAvailable(self) -> None:
        self.files = self._fm.getFilesSummary()
        self.nFiles = len(self.files)

        if self.nFiles != 0:
            self._c.printInfo(f'There are {self.nFiles} files available:')
            self._c.nl()
            i=1
            for file in self.files:
                self._c.print(f'  ({i}): {file}')
                i += 1
        else:
            self._c.printWarn(f'There are no files available.')

 
class AnalyzeFile(Command):
    def __init__(self) -> None:
        self._fm = FileManager()
        self._ad = AnalysisDirector()
        self._c = ConsoleUtils

    def getDescription(self) -> str:
        return f'Analyzes the selected file.'
    
    def getKey(self) -> str:
        return 'analyze'
    
    def execute(self) -> None:
        self._c.clear()
        self._c.printInfo(f'Analyzing file')
        self._c.nl()

        file: SongData = self._fm.getSelectedFile()
        finished: bool
        
        if file is None:
            self._c.printWarn(f'No file is selected.')
            return
        
        while not finished:

            status = self._ad.getCurrentInfo()
            self._c.printInfo(f'Status: {status}')
            pass


