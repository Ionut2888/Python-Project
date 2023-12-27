import re
from collections import defaultdict


def parse_log(line):
    # Check for 'ran successfully' log entry
    success_match = re.search(
        r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - ([A-Za-z]+) (has ran successfully(?: in (\d+)ms)?)', line)

    # Check for 'failed' log entry
    failure_match = re.search(
        r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - ([A-Za-z]+) (has failed after (\d+)ms\. Retrying\.\.\.)', line)

    # Check for basic log entry
    basic_match = re.search(r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - ([A-Za-z]+) (.+)', line)

    if success_match:
        time, log_type, app_name, action, duration = success_match.groups()
        return time, log_type, app_name, action, int(duration) if duration else None
    elif failure_match:
        time, log_type, app_name, action, duration = failure_match.groups()
        return time, log_type, app_name, action, int(duration) if duration else None
    elif basic_match:
        time, log_type, app_name, action = basic_match.groups()
        return time, log_type, app_name, action, None
    else:
        return None, None, None, None, None


def count_logs(filename):
    log_entries = []

    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            time, log_type, app_name, action, duration = parse_log(line)
            if time:
                log_entries.append((log_type, app_name, time, action, duration))
            else:
                print(f"Warning: Skipped line {line_number} as it does not match the expected format.")

    return log_entries


def main():
    filename = 'output.txt'
    log_entries = count_logs(filename)

    print("Log Entries:")
    if not log_entries:
        print("No log entries found.")
    else:
        # Sort log entries by log type, app name, time, and duration
        sorted_logs = sorted(log_entries, key=lambda entry: (
        entry[0], entry[1], entry[2], entry[4] if entry[4] is not None else float('inf')))

        for log_type, app_name, time, action, duration in sorted_logs:
            if duration is not None:
                print(f"{log_type} {app_name} {time} {duration}ms")
            else:
                print(f"{log_type} {app_name} {time}")


if __name__ == "__main__":
    main()
