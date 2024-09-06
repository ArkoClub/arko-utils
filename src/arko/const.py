import os
import sys

__all__ = ("IS_RUNNING_IN_PYCHARM", "IS_WINDOWS")

IS_RUNNING_IN_PYCHARM = "PYCHARM_HOSTED" in os.environ
IS_WINDOWS = sys.platform == "win32"
