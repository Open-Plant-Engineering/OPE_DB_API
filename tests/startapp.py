from OPE_DB_API.app import create_app
from OPE_DB_API.config import set_config_file
from OPE_DB_API.db import Base, get_engine

# 1. Set config path FIRST
set_config_file("E:\\SKGitRepo\\OPE\\OPE_DB_API\\defaults\\config.toml")

# 2. Explicitly create tables (DEV ONLY)
engine = get_engine("XYZ")  # use your project code
Base.metadata.create_all(bind=engine)

# 3. Create the FastAPI app
app = create_app()