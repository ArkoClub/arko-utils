import os
import sys
from pathlib import Path

__all__ = ("IS_RUNNING_IN_PYCHARM", "IS_WINDOWS", "PROJECT_ROOT")

IS_RUNNING_IN_PYCHARM = "PYCHARM_HOSTED" in os.environ
IS_WINDOWS = sys.platform == "win32"

PROJECT_ROOT = Path(os.curdir).resolve().absolute()
