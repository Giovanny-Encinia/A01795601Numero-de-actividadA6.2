import sys
import os

parent = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(parent, "..", "src"))

print(parent_dir)
sys.path.append(parent_dir)
