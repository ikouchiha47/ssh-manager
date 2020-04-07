import re

class Tasks:
    def __init__(self, args, configs):
        self.args = args
        self.configs = configs

    # change shit shit, its ugly
    def __make_config(self, hostname, host, user, key, jumpbox):
        config = {}
        if hostname:
            config['HostName'] = hostname
        if host:
            config['Host'] = host
        if user:
            config['User'] = user
        if key:
            config['IdentityFile'] = key
        if jumpbox:
            config['ProxyJump'] = jumpbox

        return config

    def __get_values(self):
        hostname = self.args.host
        user     = self.args.user
        key      = self.args.key
        host     = hostname
        jumpbox  = None

        if "jumpbox" in self.args: jumpbox  = self.args.jumpbox
        if self.args.alias: host = self.args.alias

        return (hostname, host, user, key, jumpbox)

    def __print_config(self, conf):
        if not conf['Host']:
            return ""

        s = ["%s %s" % ("Host", conf["Host"])]
        for ckey, cval in conf.items():
            if ckey == "Host": continue
            s.append("\t%s %s" % (ckey, cval))

        return "\n".join(s)

    def __find(self, conf):
        idxs = []
        for idx, config in enumerate(self.configs):
            success_compares = 0
            for ckey, cval in conf.items():
                if cval is None: continue
                rx = re.compile(cval)
                if ckey in config and rx.search(config[ckey]):
                    success_compares += 1

            if success_compares == len(conf):
                idxs.append(idx)

        return idxs

    def __show_existing_configs(self, host):
        # check if config with same hostname exists
        idxs = self.__find({'Host': host })

        if len(idxs) > 0:
            print("Some config with existing Host already exists")
            for idx in idxs:
                print(self.__print_config(self.configs[idx]))
            return True
        return False

    def print_configs(self):
        config_str = [self.__print_config(conf) for conf in self.configs]
        return "\n\n".join(config_str)

    def find(self):
        #print("find")

        (hostname, host, user, key, jumpbox) = self.__get_values()

        c = self.__make_config(hostname, host, user, key, jumpbox)
        idxs = self.__find(c)
        configs = []

        for idx in idxs:
            configs.append(self.configs[idx])

        self.configs = configs

        return self.print_configs()

    def add(self):
        #print("add")

        (hostname, host, user, key, jumpbox) = self.__get_values()
        __continue = False

        if self.__show_existing_configs(host):
            sys.stdout.write("Do you want to continue? (y/n)")
            choice = input().lower()
            if choice == 'y':
                __continue = True

            if not __continue:
                return self.print_configs()

        c = self.__make_config(hostname, host, user, key, jumpbox)
        self.configs.append(c)

        return self.print_configs()
    def delete(self):
        #print("delete")

        (hostname, host, user, key, jumpbox) = self.__get_values()
        if not (hostname or host):
            print("please provide either host or hostname")
            sys.exit(1)

        c = self.__make_config(hostname, host, user, key)
        idxs = self.__find(c)

        if len(idxs) < 0:
            print("Couldn't find any ssh config for those values")
            sys.exit(1)

        configs = self.configs
        for index in sorted(idxs, reverse=True):
            del configs[index]

        self.configs = configs

        return self.print_configs()
    def modify(self):
        #print("modify")

        (hostname, host, user, key) = self.__get_values()
        c = self.__make_config(hostname, host, user, key)
        idx = self.find(c)

        if idx < 0:
            return self.print_configs()

        (hostname, host, user, key) = self.__get_values()
        if not (hostname and host):
            print("please provide either host or hostname")
            sys.exit(1)
