# I want to parse the logs first
# I'll do it for google's log line later
# Google's log line looks like {
#   "insertId": "1234567890abcdef",
#   "jsonPayload": {
#     "message": "User logged in",
#     "userId": "123",
#     "event": "login"
#   },
#   "resource": {
#     "type": "gce_instance",
#     "labels": {
#       "instance_id": "987654321",
#       "zone": "us-central1-a"
#     }
#   },
#   "timestamp": "2024-08-02T15:01:23.045Z",
#   "severity": "INFO",
#   "logName": "projects/my-project/logs/app-log"
# } I found this on Google search so I dont know if its correct or not
# I dont want to deal with JSON now so I'll make a different log
# date time ERROR error description USERID, this is what I came up with to start
# 2026-01-21 10:45:32 ERROR AuthService BAAADD! userId=1
#timestamp log_level service message -- have to keep this in mind

from datetime import datetime

def parse_log_line(line):

    parts = line.strip().split(" ", 4)
    #I want this at most 5 parts so I'll just add a constraint as 4

    if len(parts) < 5:
        return None
    # Not going to look anything which is not in my standard log sequence
    timestamp_str = parts[0] + " " + parts[1]
    log_level = parts[2]
    service = parts[3]
    # edit : right now I have not thought of doing anything with the userID so I'll include it with message
    message = " ".join(parts[4:])

    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    return (timestamp, log_level, service, message)

#testing if everything works okay
# if __name__ == "__main__":
#     sample = "2026-01-18 10:45:32 ERROR Shakti MAAASHAKTIIIIII userId=sunilshetty123"
#     parsed = parse_log_line(sample)
#     print(parsed)
