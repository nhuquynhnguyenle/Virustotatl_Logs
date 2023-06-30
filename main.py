import time
from log_management import log_management
import json

file_path = 'access.log'
management = log_management(file_path)

#
def getSampleTime ():
    file_path = 'configure.json'
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    sample_time = json_data["sampleTime"]
    return sample_time

#
def readFile():
    while True:
        try:
            with open(file_path, 'r') as file:
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if line:
                        print(line, end='')
                        management.separateData(line)
                    time.sleep(getSampleTime())
        except KeyboardInterrupt:
            print("\nstop")
            break

#
def main():
    readFile()
    management.printInfo(management.proxy_logs)

#
if __name__ == '__main__':
    main()