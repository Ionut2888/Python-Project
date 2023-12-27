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
#req1
def count_and_print_logs(log_entries):
    log_counts = defaultdict(int)

    for log_type, app_name, _, _, _ in log_entries:
        if log_type in ['ERROR', 'DEBUG', 'INFO']:
            log_counts[(log_type, app_name)] += 1

    print("Log Counts:")
    for log_type in ['ERROR', 'DEBUG', 'INFO']:
        for (log, app_name), count in log_counts.items():
            if log == log_type:
                if log == 'INFO':
                    count //= 2  # Divide INFO count by 2
                print(f"{log} {app_name}: {count} logs")
#req2
def average_successful_run_time(log_entries):
    info_logs = [(log_type, app_name, duration) for log_type, app_name, _, action, duration in log_entries
                 if log_type == 'INFO' and app_name not in ['SYSTEM', ''] and duration is not None]

    if not info_logs:
        print("No relevant INFO logs found.")
        return

    durations = [duration for _, _, duration in info_logs]
    average_time = sum(durations) / len(durations)

    print(f"\nAverage Successful Run Time: {average_time:.2f} ms")


#req3
def count_failures(log_entries):
    failure_counts = defaultdict(int)

    for log_type, app_name, _, _, _ in log_entries:
        if log_type == 'ERROR':
            failure_counts[app_name] += 1

    print("\nFailure Counts:")
    for app_name, count in failure_counts.items():
        print(f"{app_name}: {count} failures")

#req4
def most_failed_app(log_entries):
    failure_counts = defaultdict(int)

    for log_type, app_name, _, _, _ in log_entries:
        if log_type == 'ERROR':
            failure_counts[app_name] += 1

    if not failure_counts:
        print("\nNo ERROR logs found.")
        return

    most_failed_app = max(failure_counts, key=failure_counts.get)
    most_failed_count = failure_counts[most_failed_app]

    print(f"\nApp with the most failed runs:")
    print(f"{most_failed_app}: {most_failed_count} failures")

#req5
def most_successful_app(log_entries):
    success_counts = defaultdict(int)

    for log_type, app_name, _, _, _ in log_entries:
        if log_type == 'INFO':
            success_counts[app_name] += 1

    if not success_counts:
        print("\nNo successful INFO logs found.")
        return

    most_successful_app = max(success_counts, key=success_counts.get)
    most_successful_count = success_counts[most_successful_app]

    print(f"\nApp with the most successful runs:")
    print(f"{most_successful_app}: {most_successful_count//2} successful runs")

def most_failed_third_of_day(log_entries):
    thirds_counts = {'00:00:00-07:59:59': 0, '08:00:00-15:59:59': 0, '16:00:00-23:59:59': 0}

    for _, _, time, _, _ in log_entries:
        hour = int(time.split(':')[0])
        if 0 <= hour < 8:
            thirds_counts['00:00:00-07:59:59'] += 1
        elif 8 <= hour < 16:
            thirds_counts['08:00:00-15:59:59'] += 1
        else:
            thirds_counts['16:00:00-23:59:59'] += 1

    most_failed_third = max(thirds_counts, key=thirds_counts.get)
    most_failed_third_count = thirds_counts[most_failed_third]

    print(f"\nThird of the day with the most failed runs:")
    print(f"{most_failed_third}: {most_failed_third_count} failures")

#req6
def longest_shortest_successful_run_times(log_entries):
    successful_runs = [(time, app_name, duration) for log_type, app_name, time, _, duration in log_entries
                       if log_type == 'INFO' and duration is not None]

    if not successful_runs:
        print("\nNo successful runs found.")
        return

    # Find the longest and shortest successful run times
    longest_run = max(successful_runs, key=lambda x: x[2])
    shortest_run = min(successful_runs, key=lambda x: x[2])

    print(f"\nLongest Run: {longest_run[1]} {longest_run[0]} {longest_run[2]}ms")
    print(f"Shortest Run: {shortest_run[1]} {shortest_run[0]} {shortest_run[2]}ms")

#req7
def most_active_hour_by_app_and_log_type(log_entries):
    # Dictionary to store counts for each hour, app, and log type combination
    activity_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for log_type, app_name, time, _, _ in log_entries:
        hour = int(time.split(':')[0])
        activity_counts[hour][app_name][log_type] += 1

    print("\nMost Active Hour by App and Log Type (Sorted by App Type):")
    for app_name in sorted(set(entry[1] for entry in log_entries)):
        for hour, log_counts in activity_counts.items():
            if app_name in log_counts:
                for log_type, count in log_counts[app_name].items():
                    if count == max(log_counts[app_name].values()):
                        print(f"Hour {hour:02d}: App={app_name}, Log Type={log_type}, Count={count}")

def main():
    filename = 'output.txt'
    log_entries = count_logs(filename)
    #requirmets
    count_and_print_logs(log_entries)
    average_successful_run_time(log_entries)
    count_failures(log_entries)
    most_failed_app(log_entries)
    most_successful_app(log_entries)
    most_failed_third_of_day(log_entries)
    longest_shortest_successful_run_times(log_entries)
    most_active_hour_by_app_and_log_type(log_entries)

    print("Log Entries:")
    if not log_entries:
        print("No log entries found.")
    else:
        # Sort log entries by log type, app name, time, and duration
        sorted_logs = sorted(log_entries, key=lambda entry: (
            entry[0], entry[1], entry[2], entry[4] if entry[4] is not None else float('inf')))

        for log_type, app_name, time, action, duration in sorted_logs:
            if duration is not None:
                print(f"{log_type} {app_name} {time} {duration}ms {action}" )
            else:
                print(f"{log_type} {app_name} {time} {action}")


if __name__ == "__main__":
    main()
