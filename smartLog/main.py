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


#starting the generator main file
# all variable up till now:
#generator: generate_log_stream
#statistical: RollingStats

from utils.generator import generate_log_stream
from anomaly.statistical import RollingStats
from datetime import datetime, timedelta
from collections import defaultdict

def stream_main():
    service_count = defaultdict(int)
    level_count = defaultdict(int)

    stats = RollingStats(window_size = 5, threshold = 2)

    error_count = 0
    window_start = None
    WINDOW_SECONDS = 10

    for line in generate_log_stream(10000):
        parsed = parse_log_line(line)
        if not parsed:
            continue

        ts, level, service, message = parsed
        #edit: I AM AN IDOITTTTTTTT!!!!!
        #timestamp = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        timestamp = ts

        service_count[service] += 1
        level_count[level] += 1

        if window_start is None:
            window_start = timestamp

        if timestamp - window_start <= timedelta(seconds = WINDOW_SECONDS):
            if level == "ERROR":
                error_count += 1
        else:
            stats.update(error_count)

            if stats.is_anomaly(error_count):
                print(f"Anomaly detected boss!: {error_count} errors in the last window")

            # for some reason I cant declare error_count as a local variable so here is my solution
            error_count = 0
            window_start = timestamp



if __name__ == "__main__":
    #main()
    stream_main()
    # for line in generate_log_stream(12):
    #     parsed = parse_log_line(line)
    #     print(parsed)