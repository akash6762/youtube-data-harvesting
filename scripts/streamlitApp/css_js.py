import sys
import os

# Append the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from scripts.youtubeApi.getChannelId import getChannelIdByName

print(getChannelIdByName("madan gowri"))
