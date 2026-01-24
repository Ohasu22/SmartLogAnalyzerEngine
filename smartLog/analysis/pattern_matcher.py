# okay now I have three things (timestamp, service, level) what can I do with it??
# maybe count the error patterns
# edit: lets just print the pattern instead of counting it(my logic's not working for counting)

from collections import deque, defaultdict

# class patternFinder:
#     def __init__(self, pattern):
#         # whats my pattern line WARN ERROR WARN ERROR
#         self.pattern = pattern
#         self.window = deque(maxlen = len(pattern))
#         self.matches = 0
#
#
#     def process(self,level):
#         self.window.append(level)
#
#         if len(self.window) == len(self.pattern):
#             if tuple(self.window) == self.pattern:
#                 self.matches += 1
#                 return True
#         return False


#kinda very simple code tbh, I dont feel confident its gonna look good in front of google
# right now I am just giving out on what timestamp the logs are showing a pattern, I still have service and level unused
# how about I add on the service and level as well

#playing way too much apex to not add this easteregg
class patternFinder:
    def __init__(self, pattern, max_time_gap = None):

        self.pattern = pattern
        self.window = deque(maxlen = len(pattern))
        self.timestamps = deque(maxlen= len(pattern))
        self.max_time_gap = max_time_gap
        self.pattern_count = defaultdict(int)


    def analysis(self,service, level, timestamp):
        self.window.append((service, level))
        self.timestamps.append(timestamp)

        if len(self.window) < len(self.pattern):
            return False

        if tuple(self.window) != self.pattern:
            return False

        #edit: adding this from gpt so dont know if it will work or not
        #edit2: yup it works
        if self.max_time_gap:
            if(self.timestamps[-1] - self.timestamps[0]).total_seconds() > self.max_time_gap:
                return False

        self.pattern_count[self.pattern] += 1
        return True