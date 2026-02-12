#my config coz i hate changing num_logs for testing

NUM_LOGS = 1000       # number of logs to generate
WINDOW_SECONDS = 10 # time window size for stats
ROLLING_WINDOW = 5  # rolling window size for rolling mean detection
THRESHOLD = 2       # threshold for anomalies
PATTERN_TO_DETECT = [('AuthService', 'WARN'), ('AuthService', 'ERROR'),('Shaktiiii','ERROR')]
MAX_TIME_GAP = 5    # seconds gap for logs for ignorance