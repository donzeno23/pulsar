#   ____   _    _   _       ____      _     ____  
#  |  _ \ | |  | | | |     / ___|    / \   |  _ \ 
#  | |_) || |  | | | |     \ ___ \  / _ \  | |_) |
#  |  __/ | |__| | | |____  ___) / / ___ \ |  _ < 
#  |_|    |_|__|_| |_|____||____/ /_/   \_\|_| \_\
#                
#  ____   ____   ____   ____   ____   ____    ____  

"""
Pulsar Library
=================
Pulsar: A Python library for building and managing distributed systems.
This library provides a framework for creating, running, and managing distributed
systems, with a focus on ease of use and flexibility.

  >>> from pulsar import setup, run, teardown
  >>> setup()
  Getting logs from Pulsar stage initialized.
  >>> run()
  Running the Pulsar stage.
  >>> teardown()
  Tearing down the Pulsar stage.
  >>> from pulsar import load_stage_modules
  >>> load_stage_modules()
  [<module 'pulsar.stages.get_logs' from 'pulsar/stages/get_logs.py'>]



"""
import pulsar
from .stages import get_logs
from .stages import send_messages
from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
    __copyright_year__,
    __cake__,
)
from .utils import loader
