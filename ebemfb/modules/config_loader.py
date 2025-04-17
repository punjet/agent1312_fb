from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.toml", ".env"],
    environments=True,
)