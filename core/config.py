from core import main_dir
import yaml

with open(main_dir + "/config.yml", "r") as _config:
    config_data = yaml.load(_config, Loader=yaml.SafeLoader)


class Config:
    def __init__(self):
        self.discord_client_id = config_data["discord_client_id"]
        self.discord_client_secret = config_data["discord_client_secret"]
        self.discord_redirect_uri = config_data["discord_redirect_uri"]
        self.web_admins = config_data["web_admins"]

config = Config()