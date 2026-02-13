
from typing import List
from os.path import join
import time
from libs.ue_log import UE_Log


# infinite read files, sleep n seconds where file and
def read_files_runtime(path: str, file_names: List[str]):
    # open files by name and path
    files = {}
    for file_name in file_names:
        files[file_name] = open(join(path, file_name), "r")

    # infinite read this files
    while True:
        for file_name, file in files.items():
            while True:
                line = file.readline()
                if not line:
                    break
                yield file_name, line

        time.sleep(2)


# read file to the end, yield UE_Log's
def read_file(file_name, file):
    accumulated_log_line: UE_Log = UE_Log.make_empty()

    try:
        while True:
            line = file.readline()
            if not line:
                # yield accumulated log string
                if accumulated_log_line.is_valid():
                    yield accumulated_log_line
                    accumulated_log_line: UE_Log = UE_Log.make_empty()
                break
    
            log_line: UE_Log = UE_Log.create_from_line(file_name, line)
    
            # accumulate log if it continue previous string
            if not log_line.is_valid():
                if accumulated_log_line.is_valid():
                    # print(f"..... accumulate")
                    accumulated_log_line.log_text += "\n" + "\t" + "\t" + line[:-1]    # remove last char "/n"
                else:
                    # print(f"..... new line")
                    accumulated_log_line = log_line
            
            # return accumulated log line if start next line
            else:
                if accumulated_log_line.is_valid():
                    # print(f"..... push")
                    yield accumulated_log_line
                # print(f"..... create new")
                accumulated_log_line = log_line
    
    except Exception as error:
        pass
    
    pass
