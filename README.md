# Lanteya Log Collector
Read dedicated server log and report warnings in discord.
<br>
Automatically open new log files if new game server starts.

![ExampleReport](https://raw.githubusercontent.com/koenigigor/UE_LogReader/refs/heads/master/example/ExampleReport.png)


---

## Usage
1. Download latest release or clone repository.
2. Setup **config.json**
   <br>&nbsp;&nbsp;2.1. Set LogPath with game log folder
   <br>&nbsp;&nbsp;2.2. Set DiscordWebhook for reports
   <br>&nbsp;&nbsp;2.3. Set Listen or Ignore Categories
3. Run tool

> You can override **config.json** by _config=_ argument (LanteyaLogCollector.exe -config=OtherConfig.json)


---

## Future plans
1. Replace config.json with config.ini
