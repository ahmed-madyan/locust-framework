import os

INITIAL_SPIKE_USERS = int(os.environ.get("INITIAL_SPIKE_USERS", 1))
RAMP_UP_USERS = int(os.environ.get("RAMP_UP_USERS", 20))
RAMP_UP_DURATION = int(os.environ.get("RAMP_UP_DURATION", 10))
STEADY_USERS = int(os.environ.get("STEADY_USERS", 5))
STEADY_DURATION = int(os.environ.get("STEADY_DURATION", 5))
STRESS_START_USERS = int(os.environ.get("STRESS_START_USERS", 5))
STRESS_END_USERS = int(os.environ.get("STRESS_END_USERS", 15))
STRESS_DURATION = int(os.environ.get("STRESS_DURATION", 10))

# LOAD TEST CONFIGURATION
# LOAD_SHAPER_CONFIG = {
#     "INITIAL_SPIKE_USERS": 1,
#     "RAMP_UP_USERS": 20,
#     "RAMP_UP_DURATION": 10,
#     "STEADY_USERS": 5,
#     "STEADY_DURATION": 5,
#     "STRESS_START_USERS": 5,
#     "STRESS_END_USERS": 15,
#     "STRESS_DURATION": 10
# }
#
# # LOAD TEST PROFILES
# LOAD_PROFILES = {
#     "BASIC": {
#         "INITIAL_SPIKE_USERS": 1,
#         "RAMP_UP_USERS": 20,
#         "RAMP_UP_DURATION": 10
#     },
#     "STRESS": {
#         "INITIAL_SPIKE_USERS": 5,
#         "RAMP_UP_USERS": 50,
#         "RAMP_UP_DURATION": 20,
#         "STEADY_USERS": 30,
#         "STEADY_DURATION": 30
#     },
#     "ENDURANCE": {
#         "INITIAL_SPIKE_USERS": 1,
#         "RAMP_UP_USERS": 10,
#         "RAMP_UP_DURATION": 30,
#         "STEADY_USERS": 10,
#         "STEADY_DURATION": 3600  # 1 HOUR
#     }
# }
#