from OPE_DB_API.app import create_app
from OPE_DB_API.config import set_config_file, get_config

set_config_file("/workspaces/OPE_DB_API/defaults/config.toml")
cfg = get_config(force_reload=True)

app = create_app()
