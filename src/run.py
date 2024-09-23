from core.analysis.fileManager import FileManager
from core.analysis.analysisDirector import AnalysisDirector
import os

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # logger.ENABLE = False
    fm: FileManager = FileManager()
    ad: AnalysisDirector = AnalysisDirector()

    fm.addFileFromPath(r"resources\tinytag_structure.json") 
    #fm.addFileFromPath(r"resources\CamelPhat, Yannis, Foals - Hypercolour.mp3") 

    fm.selectFile(0)
    ad.analyze()
    
    #fm.selectFile(1)
    #ad.analyze()