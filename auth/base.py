import environ
import os
from pathlib import Path

env = environ.Env(
    # set casting, default value
    # DEBUG=(bool, False)
)

# Set the project base directory
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
