from core import main_dir
import yaml

with open(main_dir + "/config.yml", "r") as _config:
    config_data = yaml.load(_config, Loader=yaml.SafeLoader)


class Config:
    def __init__(self):
        self.discord_client_id = config_data["DISCORD_CLIENT_ID"]
        self.discord_client_secret = config_data["DISCORD_CLIENT_SECRET"]
        self.discord_redirect_uri = config_data["DISCORD_REDIRECT_URI"]

config = Config()