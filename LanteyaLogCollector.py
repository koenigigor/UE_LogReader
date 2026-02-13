import getopt
import os
import sys
import time
from os import listdir
from os.path import isfile, join

from libs.file_reader import read_file
from libs.reader_config import Config
from libs.ue_log import VerbosityLevel, UE_Log
from libs.my_discord import DiscordMessenger


def get_config_path():
    # Allow to override the path via --config argument
    config_path = "config.json"
    options, args = getopt.getopt(sys.argv[1:], "", ['config='])
    for option in options:
        if option[0] == "--config":     # key
            config_path = option[1]     # value

    return config_path

def open_new_files(log_path, opened_files, closed_files_protection_map, b_read_backup, messanger: DiscordMessenger):
    # 1. Get files in folder
    log_file_names = [f for f in listdir(log_path) if isfile(join(log_path, f))
                      and (b_read_backup or not f.__contains__("backup"))
                      and not f.__contains__("UnrealVersionSelector")]

    open_files_count = 0
    for file_name in log_file_names:
        # 2. check if already open
        if file_name in opened_files:
            continue
        
        # 3. check if was already read
        if file_name in closed_files_protection_map:
            closed_last_modified_time = closed_files_protection_map[file_name]
            new_last_modified_time = os.path.getmtime(join(log_path, file_name))
            if closed_last_modified_time == new_last_modified_time:
                continue

        opened_files[file_name] = open(join(log_path, file_name), "r", encoding="utf-8")
        #print(f'Open new file {file_name}')
        
        open_files_count += 1
        if open_files_count <= 3:
            messanger.send(f'Open new file {file_name}')
    if open_files_count > 3:
        messanger.send(f'Open {open_files_count - 3} more files')

def process_log_line(log_line: UE_Log, config: Config, output_file, messanger: DiscordMessenger) -> None:
    if not log_line.is_satisfy_verbosity(config.verbosity):
        return
    if (len(config.listen_categories) != 0) and (log_line.log_category not in config.listen_categories):
        return
    if (len(config.ignore_categories) != 0) and (log_line.log_category in config.ignore_categories):
        return

    #if "Hubie" not in log_line.log_text:
    #    return

    print(log_line)
    if output_file:
        output_file.write(log_line.__str__() + "\n")

    # Send discord if error
    #if config.send_errors_in_discord and log_line.is_satisfy_verbosity(VerbosityLevel.Error):
    if config.send_errors_in_discord and log_line.is_satisfy_verbosity(VerbosityLevel.Warning):
        messanger.send(log_line.__str__())


def main():
    print("Lanteya log collector v0.3")

    # Load config
    config_path = get_config_path()
    config = Config(config_path)

    # Validate log folder
    print(f"Log path: {config.log_path}")
    if not os.path.exists(config.log_path):
        print("... path not found")
        return

    # Create output file
    output_file = 0
    if config.b_output_file:
        if os.path.exists("Output.txt"):
            os.remove("Output.txt")
        output_file = open("Output.txt", mode="w", encoding="utf-8")

    # init discord messanger
    messanger = DiscordMessenger(config.hostname, "LogCollector", config.discord_webhook)
    messanger.b_active = config.send_errors_in_discord

    tick_time = 0.1

    check_new_files_time = 0.0
    opened_files_map = {}               # name - file
    closed_files_protection_map = {}    # name - last modified time

    open_new_files(config.log_path, opened_files_map, closed_files_protection_map, config.b_read_backup, messanger)
    
    while True:
        # 1. Periodically open new files
        check_new_files_time += tick_time
        if check_new_files_time >= config.poll_interval_sec:
            open_new_files(config.log_path, opened_files_map, closed_files_protection_map, config.b_read_backup, messanger)
            check_new_files_time -= config.poll_interval_sec

        # 2. Read opened files
        files_to_close: list[str] = []
        for file_name, file in opened_files_map.items():
            for log_line in read_file(file_name, file):
                process_log_line(log_line, config, output_file, messanger)
                
                if log_line.is_close():
                    files_to_close.append(file_name)
            pass

        # 3. Cache last modify time and close file
        closed_files_count = 0
        for file_to_close in files_to_close:
            
            closed_files_protection_map[file_to_close] = os.path.getmtime(join(config.log_path, file_to_close))

            file = opened_files_map[file_to_close]
            file.close()
            del opened_files_map[file_to_close]
            #print(f"Close file: {file_to_close}")

            closed_files_count += 1
            if closed_files_count <= 3:
                messanger.send(f"Close file: {file_to_close}")
        if closed_files_count > 3:
            messanger.send(f'Close {closed_files_count - 3} more files')

        time.sleep(tick_time)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
    input("End program")
