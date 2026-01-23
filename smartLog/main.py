# all variables up till now:
# parse_log_line
# parsed logs: tuple list (timestamp, level, service, message)
# count_frequencies
# service_count, level_count
# detect_error_spikes
# tuple list named spikes -> (timestamp, len(error_timestamps))


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


if __name__ == "__main__":
    main()