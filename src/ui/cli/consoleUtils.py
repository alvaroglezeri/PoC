import os

class ConsoleUtils:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def nl():
        print()

    @staticmethod
    def print(msg):
        print(msg)

    @staticmethod
    def input():
        return input('[>] ')
    
    @staticmethod
    def input(msg):
        return input(f'[>] {msg} ')

    @staticmethod
    def printSuccess(msg, title=None):
        if title:
            print(f'[✓] {title}:{msg}')
        else:
            print(f'[✓] {msg}')

    @staticmethod
    def printError(msg, title=None):
        if title:
            print(f'[x] {title}:{msg}')
        else:
            print(f'[x] {msg}')

    @staticmethod
    def printInfo(msg, title=None):
        if title:
            print(f'[i] {title}:{msg}')
        else:
            print(f'[i] {msg}')

    @staticmethod
    def printWarn(msg, title=None):
        if title:
            print(f'[!] {title}:{msg}')
        else:
            print(f'[!] {msg}')


