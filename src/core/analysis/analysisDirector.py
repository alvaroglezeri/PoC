from abc import ABC, abstractmethod
from core.exceptions import DuplicateElementException, NotFoundException
from core.analysis.fileManager import FileManager
from core.analysis.songData import SongData
from core.analysis.step1 import KeyAnalysis, BeatAnalysis
from core.logger import DCL, CATEGORY

class Subscriber(ABC):
    #DOCUMENT

    type Notification = dict[str, object]
    
    @abstractmethod
    def update(data: Notification) -> None:
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

    def _notify(self, msg: Subscriber.Notification) -> None:
        for subscriber in self._subscribers:
            subscriber.update(msg)

    def analyze(self) -> None:
        #DOCUMENT
        
        self._notify({"step": "1", "msg": "Loading file..."})
        self._loadFile()
        self._notify({"step": "1", "msg": "Loaded file."})
        self._notify({"step": "2", "msg": "Analyzing key..."})
        self._keyAnalysis()
        self._notify({"step": "2", "msg": "Analized key."})
        self._notify({"step": "3", "msg": "Analyzing beat..."})
        self._beatAnalysis()
        self._notify({"step": "3", "msg": "Analized beat."})
        self._notify({"finished": True})
    
    def _loadFile(self) -> None:
        # Step 1: Load file
        file = self._fm.getSelectedFile()
        
        if file is None:
            self._notify({"step": "1", "msg": "No file selected"})
            DCL.log(CATEGORY.ERROR, "AnalysisDirector.analyze", f'No file selected!')
            raise NotFoundException(f'No file selected!')
        else:
            self._selected = file
            self._notify({"step": "1", "msg": f'Selected {file.getTitle()}'})
            DCL.log(CATEGORY.INFO, "AnalysisDirector.analyze", f'Analyzing {file.getTitle()}')

    def _keyAnalysis(self) -> None:
        # Step 2: Key analysis
        
        key: str = KeyAnalysis.getKey(self._selected.getFile())
        self._notify({"step": "2", "msg": f'Got key: {key}'})
        DCL.log(CATEGORY.INFO, "AnalysisDirector._keyAnalysis", f'Found key: {key}')
          
    def _beatAnalysis(self) -> None:
        # Step 3: Beat analysis
        
        bpm, confidence = BeatAnalysis.getBeat(self._selected.getFile())
        self._notify({"step": "3", "msg": f'Got bpm: {bpm}'})
        DCL.log(CATEGORY.INFO, "AnalysisDirector._beatAnalysis", f'Found bpm: {bpm} with {confidence*100//1}% confidence.')