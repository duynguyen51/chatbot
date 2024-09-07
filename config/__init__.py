
from .settings import get_settings
import os


config = get_settings(os.path.abspath('config/config.yaml'))
