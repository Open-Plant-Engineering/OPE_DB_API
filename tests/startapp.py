from sqlalchemy import Sequence
from OPE_DB_API.app import create_app
from OPE_DB_API.config import set_config_file
from OPE_DB_API.db import Base, get_engine
from OPE_DB_API.db.init_db import init_database

# 1. Set config path FIRST
set_config_file(r"C:\SKRepo\OPE_DB_API\defaults\config.toml")

# 2. Explicitly create tables (DEV ONLY)
engine = get_engine("XYZ", True)  # use your project code

init_database(engine)

# 3. Create the FastAPI app
app = create_app()