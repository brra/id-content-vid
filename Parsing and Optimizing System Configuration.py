import re

def parse_log(file_path):
    with open(file_path, 'r') as file:
        log_contents = file.readlines()

    for line in log_contents:
        print(line.strip())

# Extract system configuration
parse_log('/mnt/data/report-asus-pn51.log')
parse_log('/mnt/data/performance-asus-pn51.log')
parse_log('/mnt/data/system.journal')
