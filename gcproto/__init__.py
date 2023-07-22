import os
import sys

# Workaround for https://github.com/protocolbuffers/protobuf/issues/1491
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
