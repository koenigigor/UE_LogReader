import json
import os.path
from libs.ue_log import VerbosityLevel


class Config:
    # Config for LanteyaLogCollector
    
    def __init__(self, config_path: str):
        if not os.path.exists(config_path):
            print(f"config {config_path} not found")
            return

        print(f"OK load config {config_path}")
        config_file = open(config_path)
        config_json = json.load(config_file)

        self.log_path = config_json["LogPath"]
        self.verbosity: VerbosityLevel = VerbosityLevel[config_json["VerbosityLevel"]]

        self.listen_categories: list[str] = []
        if bool(config_json["UseListenCategories"]):
            self.listen_categories: list[str] = config_json["ListenCategories"]

        self.ignore_categories: list[str] = []
        if bool(config_json["UseIgnoreCategories"]):
            self.ignore_categories: list[str] = config_json["IgnoreCategories"]

        self.send_errors_in_discord: bool = bool(config_json["SendErrorsInDiscord"])
        self.discord_webhook = config_json["DiscordWebhook"]
        self.hostname = config_json["Hostname"]

        self.b_output_file: bool = bool(config_json["OutputInFile"])
        self.b_read_backup: bool = bool(config_json["ReadBackup"])
        
        self.poll_interval_sec = int(config_json.get("PollIntervalSec", 10))
