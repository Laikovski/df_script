import argparse
import json
import re
from subprocess import Popen, PIPE


class BaseParser:
    '''main class for work with data and get info'''

    def __init__(self, output):
        self.output = output

    def parse(self):
        ''' get and split data '''
        keys = re.findall(r'\w+[\s%\-a-z]*', self.output[0])
        keys = [x.strip() for x in keys]
        parsed_data = []
        for line in self.output[1:]:
            values = line.split()
            parsed_data.append(dict(zip(keys, values)))

        return parsed_data


class BaseExecutor:
    '''main class executor for json'''

    def __init__(self):
        self.command = "df"

    def execute(self, parameter=None):
        command_with_arg = [self.command, parameter] if parameter else [self.command]
        with Popen(command_with_arg, stdout=PIPE) as proc:
            result = proc.stdout.read()
            return result.decode().splitlines()

    def run(self):
        output = self.execute()
        parser = BaseParser(output)
        return parser.parse()

    def main(self):
        result = self.run()
        result_schema = {
            "status": "success",
            "error": None,
            "result": result
        }
        return result_schema


class HumanRepresentationExecutor(BaseExecutor):
    '''inherited class to work with humanrepresentation'''

    def run(self):
        output = self.execute("-h")
        parser = BaseParser(output)
        return parser.parse()


class InodeRepresentationExecutor(BaseExecutor):
    '''inherited class to work with inoderepresention'''

    def run(self):
        output = self.execute("-i")
        parser = BaseParser(output)
        return parser.parse()


def get_args():
    '''get arguments from request use argparse'''
    parser = argparse.ArgumentParser(description="Execute unix 'df' command.")
    parser.add_argument('--human', action='store_true', help='Enter argument for human representation')
    parser.add_argument('--inode', action='store_true', help='Enter argument for inode representation')

    return vars(parser.parse_args())


def main(args):
    if args["human"]:
        executor = HumanRepresentationExecutor()
    elif args["inode"]:
        executor = InodeRepresentationExecutor()
    else:
        executor = BaseExecutor()
    result = executor.main()
    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    arguments = get_args()
    main(arguments)
