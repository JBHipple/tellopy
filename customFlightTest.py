from TelloConnector import TelloConnector
import sys
from datetime import datetime
import time
import argparse

def parse_args(args):
    """
    Parses arguments
    :param args: Arguments
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser("Tello Flight Commander", epilog='JBHipple')

    parser.add_argument('-f', '--file', help='command file', required=True)
    return parser.parse_args(args)

def start(file_name):
    """
    Starts sending commands to the Tello
    :param file_name: Filename where commands are located
    :return: None
    """
    start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

    with open(file_name, 'r') as f:
        commands = f.readlines()

    drone = TelloConnector()
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print(f'delay {sec}')
                time.sleep(sec)
                pass
            else:
                drone.send_command(command)

    with open(f'log/{start_time}.txt', 'w') as out:
        log = drone.get_log()

        for stat in log:
            stat.print_stats()
            s = stat.return_stats()
            out.write(s)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    file_name = args.file
    start(file_name)