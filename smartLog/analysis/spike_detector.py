# Note: strike means the whole line is striked through (strike isnt working on github but on pycharm it is, had to change some TODO settings)
# Now I have two things from frequency.py -> timestamp and errorcode
# how about I make a system which detects a sudden spike in the error, that way I know something is wrong
# So like There are A type of ERROR logs within B seconds
# so threshold should be something I have to decide later IMP
# edit 1: threshold = 5
# strike I am thinking of using a sliding window for counting the timestamps (time complexity is O(2n))
# Instead lets go for Queue / deque with Two pointers (this one is much better)
# edit 2:   Core idea:
# walk through the log only once
# keep only the recent timestamp ERROR
# remove old timestamp from pointer and check count
# time complixity O(n), space O(m) edit 3: mental note to further optimise the space

from collections import deque
# all variables up till now:
# parsed logs: tuple list (timestamp, level, service, message)
# service_count, level_count
def detect_error_spikes(parsed_logs, threshold, window_seconds):

    error_timestamps = deque()
    spikes = []

    for log in parsed_logs:
        timestamp, level, _, _ = log

        #only want the errors so skipping the non error ones
        if level != "ERROR":
            continue

        error_timestamps.append(timestamp)

        # checking the last and first values in the error logs if they are bigger than window_seconds
        # remove timestamps outside the window
        while (error_timestamps[-1] - error_timestamps[0]).seconds > window_seconds:
            error_timestamps.popleft()

        if len(error_timestamps) > threshold:
            #edit : making tuple of timestamp and error timestamp count for extra security
            spikes.append((timestamp, len(error_timestamps)))
    # list of tuples
    return spikes