from abc import ABC, abstractmethod
from enum import Enum

enable: bool = True
class CATEGORY(Enum):
    ERROR = 'FAIL'
    INFO = 'INFO'
    WARN = 'WARN'
    SUCCESS = 'SUCC'
#CATEGORY = Enum('Category', ['ERROR', 'INFO', 'WARN', 'SUCCESS', 'DEBUG'])

#DOCUMENT
class Logger(ABC):
    def __new__(cls):
        """
        Singleton implementation
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance
    
    @abstractmethod
    def log(msg: any) -> None:
        pass

    @abstractmethod
    def log(location: str, msg: any) -> None:
        pass
    
    @abstractmethod
    def log(category: CATEGORY, location: str, msg: any) -> None:
        pass

    @staticmethod
    def isEnabled() -> bool:
        pass

class DCL(Logger):
    """
    Debug Console Logger
    
    DOCUMENT
    """
    @staticmethod
    def log(msg: any) -> None:
        if enable:
            print(f'[DEBUG]: {msg}') 
        
    @staticmethod
    def log(location: str, msg: any) -> None:
        if enable:
            print(f'[DEBUG] at {location}: {msg}')
            
    @staticmethod
    def log(category: CATEGORY, location: str, msg: any) -> None:
        if enable:
            print(f'[DEBUG:{category.value}] at {location}: {msg}')

    @staticmethod
    def isEnabled() -> bool:
        return enable
    

