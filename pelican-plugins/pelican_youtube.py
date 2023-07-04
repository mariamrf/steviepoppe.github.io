import sys
import os

PLUGINS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(PLUGINS_DIR, 'pelican_youtube', 'pelican_youtube'))

from youtube import register