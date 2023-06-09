import os
from dynaconf import Dynaconf
current_directory = os.path.dirname(os.path.abspath(__file__))
settings = Dynaconf(
    envvar_prefix=False,
    settings_files=[f"{current_directory}/settings.py", f"{current_directory}/.secrets.py", f"{os.getcwd()}/settings.py"],
)
