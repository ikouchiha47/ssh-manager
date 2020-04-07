import os
import ntpath
import sys
import argparse
import git
from scripts.tasks import Tasks
from scripts.writer import FileWriter
from scripts.parser import ParseConfig

class CustomArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


filename = os.path.expanduser("~/.ssh/config")
parser = ParseConfig(filename)
#print(parser.parse_ssh_config())

cliopts = {
    "add": [
        { "opt": "host", "type": str, "help": "provide the host ip", "required": True },
        { "opt": "alias", "type": str, "help": "provide the host, for aliasing, defaults to host", "required": False },
        { "opt": "user", "type": str, "help": "provide ssh user", "required": False, "default": "amitava.ghosh" },
        { "opt": "key", "type": str, "help": "provide the private key file. defaults to ~/.ssh/id_rsa", "required": False, "default": "~/.ssh/id_rsa" },
        { "opt": "write", "type": str, "help": "writes result to specified file", "required": False, "default": argparse.SUPPRESS },
        { "opt": "jumpbox", "type": str, "help": "jumpbox config", "required": False }
    ],
    "delete": [
        { "opt": "host", "type": str, "help": "provide the hostname", "required": False },
        { "opt": "alias", "type": str, "help": "provide the host, for aliasing, defaults to hostname", "required": False },
        { "opt": "user", "type": str, "help": "provide ssh username", "required": False },
        { "opt": "key", "type": str, "help": "provide the private key file. defaults to ~/.ssh/id_rsa", "required": False },
        { "opt": "write", "type": str, "help": "writes result to specified file", "required": False }
    ],
    "find": [
        { "opt": "host", "type": str, "help": "provide the hostname", "required": False },
        { "opt": "alias", "type": str, "help": "provide the host, for aliasing, defaults to hostname", "required": False },
        { "opt": "user", "type": str, "help": "provide ssh username", "required": False },
        { "opt": "key", "type": str, "help": "provide the private key file. defaults to ~/.ssh/id_rsa", "required": False }
        #{ "opt": "write", "type": str, "help": "writes result to specified file", "required": False }
    ]
   # ,
   # "modify": [
   #     { "opt": "hostname", "type": str, "help": "provide the hostname", "required": False },
   #     { "opt": "host", "type": str, "help": "provide the host, for aliasing, defaults to hostname", "required": False },
   #     { "opt": "user", "type": str, "help": "provide ssh username", "required": True },
   #     { "opt": "key", "type": str, "help": "provide the private key file. defaults to ~/.ssh/id_rsa", "required": False },
   #     { "opt": "new_hostname", "type": str, "help": "provide the hostname", "required": False },
   #     { "opt": "new_host", "type": str, "help": "provide the host, for aliasing, defaults to hostname", "required": False },
   #     { "opt": "new_user", "type": str, "help": "provide ssh username", "required": True },
   #     { "opt": "new_key", "type": str, "help": "provide the private key file. defaults to ~/.ssh/id_rsa", "required": False },

   # ],
}

def add_opts_to_parser(key, parser):
    for opt in cliopts[key]:
        if "default" in opt:
            parser.add_argument("--%s" % (opt["opt"]), type=opt["type"], help=opt["help"], required=opt["required"], default=opt["default"])
        else:
            parser.add_argument("--%s" % (opt["opt"]), type=opt["type"], help=opt["help"], required=opt["required"])


def is_task_defined(obj, command):
    return hasattr(obj, command)

def execute_task(obj, command):
    return getattr(task, args.task)()

def write_and_commit(filepath, result):
    fw = FileWriter(filepath)
    if fw.write(result).commit():
        print("Changes written to %s and commited to git locally for tracking" % (filepath))
    else:
        print("failed to commit file, please check `git status` in %s" % (filepath))


arg_parser = CustomArgParser(description='manages ssh config file')
#arg_parser.add_argument("--write", type=str, help="writes result to specified file. defaults to ./ssh_config.", required=False, default="ssh_config")

subparsers = arg_parser.add_subparsers(dest="task")

## add subparser

add_sub_parser = subparsers.add_parser("add", description='''
    Adds ssh config with given config values.
    Example: sshman.py add --hostname=g-app-b-01 --user=some.user [--write="~/.ssh/config"]
''')
add_opts_to_parser("add", add_sub_parser)

## remove subparser

remove_sub_parser = subparsers.add_parser("delete", description='''
    Deletes ssh config with given config values.
    Can delete multiple matching entries
    Example: sshman.py delete --hostname=g-app-b-01 [--write="~/.ssh/config"]
''')
add_opts_to_parser("delete", remove_sub_parser)

## find subparser

find_sub_parser = subparsers.add_parser("find", description='''
    Finds ssh config with given config values.
    Example: sshman.py find --hostname=g-app-b-01
''')
add_opts_to_parser("find", find_sub_parser)

## modify subparser

#modify_sub_parser = subparsers.add_parser("modify")
#add_opts_to_parser("modify", modify_sub_parser)

args = arg_parser.parse_args()
task = Tasks(args, parser.parse_ssh_config())
if is_task_defined(task, args.task):
    result = execute_task(task, args.task)
    if is_task_defined(args, 'write'):
        write_and_commit(args.write, result)
    else:
        print(result)
