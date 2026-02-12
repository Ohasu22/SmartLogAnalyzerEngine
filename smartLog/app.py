# from fastapi import FastAPI, Query
# from main import stream_main
# from config import NUM_LOGS, WINDOW_SECONDS, ROLLING_WINDOW, THRESHOLD
#
# app = FastAPI(title="Distributed Log Analyzer Engine")
#
# @app.get("/")
# def root():
#     return {"status": "Log Analyzer Engine is running"}
#
# @app.get("/run")
# def run_engine(
#         num_logs: int = Query(NUM_LOGS, description="Number of logs to process"),
#         window_seconds: int = Query(WINDOW_SECONDS, description="Window size in seconds"),
#         rolling_window: int = Query(ROLLING_WINDOW, description=" Rolling window size"),
#         threshold: int = Query(THRESHOLD, description="Threshold for anomaly detection")
# ):
#
#     import io
#     import sys
#     buffer = io.StringIO()
#     sys.stdout = buffer
#
#     stream_main(num_logs=num_logs, window_seconds=window_seconds, rolling_window= rolling_window, threshold= threshold)
#
#     sys.stdout = sys.__stdout__
#     output = buffer.getvalue().splitlines()
#
#     return {"output": output}

from fastapi import FastAPI
from collections import defaultdict
from datetime import timedelta
from utils.generator import generate_log_stream
from anomaly.statistical import RollingStats
from analysis.pattern_matcher import patternFinder
from config import NUM_LOGS, WINDOW_SECONDS, ROLLING_WINDOW, THRESHOLD, PATTERN_TO_DETECT, MAX_TIME_GAP
from parser.log_parser import parse_log_line

app = FastAPI(title="Distributed Log Analyzer Engine")

@app.get("/")
def root():
    return {"status": "Log Analyzer Engine is running"}

@app.get("/run")
def run_logs(num_logs: int = NUM_LOGS):
    service_count = defaultdict(int)
    level_count = defaultdict(int)
    stats = RollingStats(window_size=ROLLING_WINDOW, threshold=THRESHOLD)
    pattern_matcher = patternFinder(pattern=PATTERN_TO_DETECT, max_time_gap=MAX_TIME_GAP)

    error_count = 0
    total_logs = 0
    window_start = None
    window_stats = []

    for line in generate_log_stream(num_logs):
        parsed = parse_log_line(line)
        if not parsed:
            continue

        ts, level, service, message = parsed
        timestamp = ts
        total_logs += 1

        matched = pattern_matcher.analysis(service, level, timestamp)

        service_count[service] += 1
        level_count[level] += 1

        if window_start is None:
            window_start = timestamp

        if timestamp - window_start <= timedelta(seconds=WINDOW_SECONDS):
            if level == "ERROR":
                error_count += 1
        else:
            stats.update(error_count)
            # window_stats.append({
            #     "window_start": window_start.strftime("%H:%M:%S"),
            #     "window_end": timestamp.strftime("%H:%M:%S"),
            #     "errors": error_count,
            #     "mean": round(stats.mean(), 2),
            #     "std": round(stats.std(), 2),
            #     "is_anomaly": stats.is_anomaly(error_count)
            # })
            error_count = 0
            window_start = timestamp

    return {
        "total_logs": total_logs,
        "total_error_windows": len(stats.values),
        "service_counts": dict(service_count),
        "level_counts": dict(level_count),
        # "window_stats": window_stats,
        "detected_patterns": dict(pattern_matcher.pattern_count)
    }