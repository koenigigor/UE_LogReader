from discordwebhook import Discord


class DiscordMessenger:
    def __init__(self, hostname: str, bot_name: str, webhook: str):
        self.hostname = hostname
        self.discord = Discord(url=webhook)
        self.bot_name = bot_name
        self.b_active = True

    def send(self, message: str):
        if self.b_active:
            self.discord.post(content=message,
                              username=f"{self.bot_name} ({self.hostname})",
                              avatar_url="https://p7.hiclipart.com/preview/840/826/516/pig-cartoon-illustration-vector-painted-big-wild-boar-thumbnail.jpg")


if __name__ == '__main__':
    discord_webhook: str = "https://discord.com/api/webhooks/1141321050911682570/aXL4r4EbEhoq-jp4u2WzrE5EhhkneEC-FKmeMIzuXXMGD2veOyUUkWHN51T-DJTrAbob"
    messenger = DiscordMessenger("test_host", "test", discord_webhook)
    messenger.send("Test message")

