import os

#dir_path = os.path.dirname(os.path.realpath(__file__))
#FIXME: Research ArgumentParser

from ui.cli.cli import Cli
cli = Cli()
#cli.setPath(dir_path)
cli.run()


