# I dont want to use ai to generate me log each time to feed to the main file
# so how about I just generate the logs with a random generator
# mybe using random would be the best option
# should I generate the logs as files or stream? files is good for but I dont think google will bat an eye on that tbh
# asked google what to do and I guess doing stream is the best option

import random
from datetime import datetime, timedelta

SERVICES = ["AuthService", "PaymentService", "Shaktiiii", "UserService"]
LEVELS = ["INFO", "WARN", "ERROR"]

# edit: not doing the file thing
#def generate_logs(filename, num_logs = 1000000, start_time = None):

def generate_log_stream(num_logs):
    # works on benchmarking!! so not using this default timestamp to start
    # if start_time is None:
    #     start_time = datetime(2026, 1, 18, 10, 45, 30)


    current_time = datetime.now()

    for _ in range(num_logs):
        level = random.choices(LEVELS, weights = [0.7,0.2,0.1])[0]
        service = random.choice(SERVICES)
        message = f"shaktiMAAAAA userId=user{random.randint(1,1000)}"

        yield f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} {level} {service} {message}"

        current_time += timedelta(seconds = random.randint(0,1))

# testing
if __name__ == "__main__":
    for idx, line in enumerate(generate_log_stream(5)):
        print(line)