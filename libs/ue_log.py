import enum


class VerbosityLevel(enum.IntEnum):
    Empty = 0
    VeryVerbose = 1
    Verbose = 2
    Log = 3
    Display = 4
    Warning = 5
    Error = 6
    Fatal = 7

    def __str__(self):
        return str(self.name)


class UE_Log:
    @classmethod
    def create_from_line(cls, file_name: str, line: str) -> "UE_Log":
        # sample line: [2024.07.14-17.01.13:873][487]LogD3D12RHI: Display: ...

        line = line[:-1]    # remove last char "/n"

        # find verbosity
        split: list = line.split(":")
        try:
            verbosity_level = VerbosityLevel[split[2][1:]]  # str to enum, verbosity block, without first space
        except:
            verbosity_level = VerbosityLevel.Log

        # line has time or not
        if line.startswith("[202"):
            log_time = split[0][1:]
            log_category = split[1].split("]")[-1]
            if verbosity_level != VerbosityLevel.Log:
                log_text = "".join(split[3:])[1:]       # ...
            else:
                log_text = "".join(split[2:])[1:]       # ...
            return UE_Log(file_name, log_time, verbosity_level, log_category, log_text)
        else:
            log_time = ""
            log_category = split[0]
            log_text = "".join(split[1:])[1:]
            return UE_Log(file_name, log_time, verbosity_level, log_category, log_text)

    @classmethod
    def make_empty(cls):
        return UE_Log('', '', VerbosityLevel.Empty, "", "")
    
    def is_valid(self):
        return self.time != "" or self.log_category.startswith("Log")
        # return self.log_category != ""
        # return not (self.log_text == "" or len(self.log_text) == 0)

    # todo how make private?
    def __init__(self, file_name: str, time: str, verbosity_level: VerbosityLevel, log_category: str, log_text: str):
        self.file_name = file_name
        self.time = time
        self.log_category = log_category
        self.verbosity_level = verbosity_level
        self.log_text = log_text

    def __str__(self):
        return (f"{self.file_name} [{self.time}] {self.log_category}: "
                f"{self.verbosity_level if self.verbosity_level != VerbosityLevel.Empty else ""}: {self.log_text}")

    def is_satisfy_verbosity(self, target_verbosity: VerbosityLevel) -> bool:
        return self.verbosity_level >= target_verbosity

    def is_close(self) -> bool:
        return "Log file closed" in self.log_category  # todo correct parsing

