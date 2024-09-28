from core.analysis.fileManager import FileManager
from core.analysis.analysisDirector import AnalysisDirector
import core.logger as logger

class SoundLight():
    # DOCUMENT
    
    def __init__(self) -> None:
        self._fm = FileManager()
        self._ad = AnalysisDirector()

    def enableLogger(self, setting: bool) -> None:
        logger.enable = setting

    def addFileFromPath(self, path: str) -> None:
        self._fm.addFileFromPath(path)

    def selectFile(self, i: int) -> None:
        self._fm.selectFile(i)

    def analyze(self) -> None:
        self._ad.analyze()