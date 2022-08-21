import os
import sys
from pathlib import Path

os.environ['PYTHONPATH'] = f":{str(Path(os.path.abspath(__file__)).parents[1])}"
