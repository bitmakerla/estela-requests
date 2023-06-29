import os
from dynaconf import Dynaconf
import logging

logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
settings_files_list = [f"{current_directory}/default_settings.py", f"{current_directory}/.secrets.py",
                       f"{os.getcwd()}/settings.py", f"{os.getcwd()}/.secrets.py"
                       f"{os.getcwd()}/custom_settings.py"]
settings = Dynaconf(
    envvar_prefix=False,
    settings_files= settings_files_list,
)

print("Settings file list: %s" % settings_files_list)
sett_as_dict = settings.as_dict()
print("Settings obtained: %s" % sett_as_dict)