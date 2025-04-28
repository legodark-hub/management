from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="DEV")
if ENVIRONMENT == "PROD":
    from .production import *
else:
    from .development import *
