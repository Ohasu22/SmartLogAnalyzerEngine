# I'll count how many times the error or anything for that matter is happening
# I am thinking maybe dictonary is the best option for this because using a list to update will kill if I scale this like Google
# Who would wanna see a list of 5 Million entries each day just to search it mannually again & again
# let me get the frequency of these logs first and then I'll think of what to do with these numbers

from collections import defaultdict

def count_frequencies(parsed_logs):

    service_count = defaultdict(int)
    level_count = defaultdict(int)

    for log in parsed_logs:
        #adding an edge case just in case if it ever goes haywire
        if log is None:
            continue

        # my log is (timestamp, log_level, service_name, message)
        _, level, service, _ = log

        service_count[service] += 1
        level_count[level] += 1


    return service_count, level_count

# testing
# if __name__ == "__main__":
#     logs = [
#         ("t", "ERROR", "AuthService", "Invalid token"),
#         ("t", "WARNING", "AuthService", "Retry"),
#         ("t", "ERROR", "PaymentService", "Timeout")
#     ]
#
#     service_count, level_count = count_frequencies(logs)
#     print(service_count)
#     print(level_count)
