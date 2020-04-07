from scripts.reader import LineReader

class ParseConfig:
    def __init__(self, filename):
        self.filename = filename

    def __config_to_kv(self, line):
        splits = line.split(" ")
        key = splits[0]
        value = " ".join(splits[1:])

        return (key, value)

    def __line_is_host(self, line):
        return line.startswith("Host") and not line.startswith("HostName")

    def parse_sub_config(self, liner):
        subconfig = {}
        key, value = self.__config_to_kv(liner.cur().strip())
        subconfig[key] = value

        while not liner.eof() and not self.__line_is_host(liner.peek().strip()):
            key, value = self.__config_to_kv(liner.next().strip())
            subconfig[key] = value

        return subconfig

    def parse_ssh_config(self):
        config = []
        liner = LineReader(self.filename)

        while not liner.eof():
            line = liner.cur().strip()
            if self.__line_is_host(line):
                subconfig = self.parse_sub_config(liner)
                config.append(subconfig)
                if not liner.eof(): liner.next()
        return config

    def add_config(self):
        return ""
