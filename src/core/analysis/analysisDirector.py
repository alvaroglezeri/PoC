from abc import ABC, abstractmethod
from core.exceptions import DuplicateElementException, NotFoundException
from core.analysis.fileManager import FileManager
from core.analysis.songData import SongData
from core.analysis.step1 import KeyAnalysis, BeatAnalysis
from core.logger import DCL, CATEGORY

class Subscriber(ABC):
    #DOCUMENT

    @abstractmethod
    def notify(data) -> None:
        pass

class AnalysisDirector():
    #DOCUMENT

    def __init__(self) -> None:
        self._subscribers: list[Subscriber] = []
        self._fm: FileManager = FileManager()
        self._key: KeyAnalysis = KeyAnalysis
        self._selected: SongData = None
        
    def subscribe(self, subscriber: Subscriber) -> None:
        #DOCUMENT
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
        else:
            raise DuplicateElementException(f'Already subscribed')

    def _notify(self, msg: any) -> None:
        # FIXME: What is the message to share?
        for subscriber in self._subscribers:
            subscriber.notify(msg)

    def analyze(self) -> None:
        #DOCUMENT
        
        self._loadFile()
        self._keyAnalysis()
        self._beatAnalysis()
    
    def _loadFile(self) -> None:
        # Step 1: Load file
        file = self._fm.getSelectedFile()
        
        if file is None:
            DCL.log(CATEGORY.ERROR, "AnalysisDirector.analyze", f'No file selected!')
            raise NotFoundException(f'No file selected!')
        else:
            self._selected = file
            DCL.log(CATEGORY.INFO, "AnalysisDirector.analyze", f'Analyzing {file.getTitle()}')

    def _keyAnalysis(self) -> None:
        # Step 2: Key analysis
        
        key: str = KeyAnalysis.getKey(self._selected.getFile())
        DCL.log(CATEGORY.INFO, "AnalysisDirector._keyAnalysis", f'Found key: {key}')
          
    def _beatAnalysis(self) -> None:
        # Step 3: Beat analysis
        
        bpm: float = BeatAnalysis.getBeat(self._selected.getFile())
        DCL.log(CATEGORY.INFO, "AnalysisDirector._beatAnalysis", f'Found FAKE bpm: {bpm}')