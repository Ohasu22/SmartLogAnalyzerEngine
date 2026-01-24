# all variables up till now:
# parse_log_line
# parsed logs: tuple list (timestamp, level, service, message)
# count_frequencies
# service_count, level_count
# detect_error_spikes
# tuple list named spikes -> (timestamp, len(error_timestamps))

# dont need parser, created the generator to create logs
from parser.log_parser import parse_log_line
from analysis.frequency import count_frequencies
from analysis.spike_detector import detect_error_spikes
#edit(25/01/26): adding pattern matcher for testing
from analysis.pattern_matcher import patternFinder

def load_logs(file_path):
    parsed_logs = []

    with open(file_path, "r") as file:
        for line in file:
            parsed = parse_log_line(line)
            # just a check if parsed has given proper output or not
            if parsed:
                parsed_logs.append(parsed)

    return parsed_logs

def main():
    # edit: mental note to automate this location chooser
    log_file = "sample_logs/sample.log"

    parsed_logs = load_logs(log_file)

    service_count, level_count = count_frequencies(parsed_logs)

    #testing phase

    print("\n --------------Frequency Analysis-------------- ")

    print("\n Logs in Service: ")
    for service, count in service_count.items():
        print(f"{service}: {count}")

    print("\n Logs in Level: ")
    for level, count in level_count.items():
        print(f"{level}: {count}")


    # def detect_error_spikes(parsed_logs, threshold, window_seconds):
    spikes = detect_error_spikes(
        parsed_logs, threshold = 5, window_seconds= 10
    )

    print("\n --------------Spike Detection-------------- ")
    if not spikes:
        print("No spikes detected YAY!")
    else:
        for timestamps, errorCount in spikes:
            print(f"Spike at {timestamps} -> {count} errors")

#-----------------------------------------------XOXO--------------------------------------
#edit(23/01/25): scrolled up and down so many times even I got confused where to look so adding this line and XOXO
#starting the generator main file
# all variable up till now:
#generator: generate_log_stream
#statistical: RollingStats

from utils.generator import generate_log_stream
from anomaly.statistical import RollingStats
from datetime import datetime, timedelta
from collections import defaultdict

def stream_main(num_logs = 1000, window_seconds = 10, rolling_window = 5, threshold = 2):
    service_count = defaultdict(int)
    level_count = defaultdict(int)

    stats = RollingStats(window_size = rolling_window, threshold = threshold)

    error_count = 0
    window_start = None
    WINDOW_SECONDS = window_seconds

    #edit: initialising my pattern finder
    pattern = (
        ("AuthService", "WARN"),
        ("AuthService", "ERROR"),
        ("Shaktiiii", "ERROR"),
    )
    pattern_matcher = patternFinder(
        pattern = pattern,
        max_time_gap= 5
    )

    for line in generate_log_stream(num_logs):
        parsed = parse_log_line(line)
        if not parsed:
            continue

        ts, level, service, message = parsed
        #edit: I AM AN IDOITTTTTTTT!!!!!
        #timestamp = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        timestamp = ts

        matched = pattern_matcher.analysis(service, level, timestamp)

        if matched:
            print(
                f"[PATTERN DETECTED BEEP BOOP] "
                f"{pattern} | "
                f"from {pattern_matcher.timestamps[0].strftime('%H:%M:%S')} "
                f"to {pattern_matcher.timestamps[-1].strftime('%H:%M:%S')}"
            )

        service_count[service] += 1
        level_count[level] += 1

        if window_start is None:
            window_start = timestamp

        if timestamp - window_start <= timedelta(seconds = WINDOW_SECONDS):
            if level == "ERROR":
                error_count += 1
        else:
            stats.update(error_count)

            #changing my printing window to look like google's
            # I am thinking of showing everything like error(already doing), std, mean, anomaly
            # error mean std amomaly(uwu)
            #edit(24/01/25): I guess on second thought I'll add this error= | mean= | std= | isAnomaly=  this one looks much better

            #dont need this now
            # if stats.is_anomaly(error_count):
            #     print(f"Anomaly detected boss!: {error_count} errors in the last window")
            # edit(24/05/26): mental note, find the difference between strf and strp time
            print(
                f"Window [{window_start.strftime('%H:%M:%S')} - {timestamp.strftime('%H:%M:%S')} | "
                f"errors = {error_count} | "
                f"mean = {stats.mean():.2f} | "
                f"std = {stats.std():.2f} | "
                f"isAnomaly = {stats.is_anomaly(error_count)}"
            )

            # for some reason I cant declare error_count as a local variable so here is my solution
            error_count = 0
            window_start = timestamp

    # edit(24/01/25): copy pasting the frequency outputs here from main
    print("\n --------------Frequency Analysis-------------- ")

    print("\n Logs in Service: ")
    for service, count in service_count.items():
        print(f"{service}: {count}")

    print("\n Logs in Level: ")
    for level, count in level_count.items():
        print(f"{level}: {count}")



if __name__ == "__main__":
    #main()
    stream_main(num_logs=10000, window_seconds=10, rolling_window=5, threshold=2)
    # for line in generate_log_stream(12):
    #     parsed = parse_log_line(line)
    #     print(parsed)