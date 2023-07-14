import logging
import os

from dynaconf import Dynaconf

logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
if os.getenv("ESTELA_CONTEXT") == "remote":
    def_settings = f"{current_directory}/settings_remote.py"
else:
    def_settings = f"{current_directory}/default_settings.py"
settings_files_list = [def_settings, f"{current_directory}/.secrets.py",
                       f"{os.getcwd()}/settings.py", f"{os.getcwd()}/.secrets.py"
                       f"{os.getcwd()}/custom_settings.py"]
settings = Dynaconf(
    envvar_prefix=False,
    settings_files= settings_files_list,
)

print("Settings file list: %s" % settings_files_list)
sett_as_dict = settings.as_dict()
print("Settings obtained: %s" % sett_as_dict)
