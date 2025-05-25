from locust import LoadTestShape
from typing import Optional, Tuple
from load_shaper.LoadProfileFactory import LoadProfileFactory
from config import LOAD_SHAPER_CONFIG


class BaseLoadShape(LoadTestShape):
    """
    Base class for all LoadTestShape implementations that provides common initialization logic.
    Implements a complex load pattern using multiple phases:
    - Initial spike
    - Ramp up
    - Steady state
    - Stress test
    """

    def __init__(self) -> None:
        """Initialize the load shape with predefined phases."""
        super().__init__()
        config = LOAD_SHAPER_CONFIG
        self.phases = LoadProfileFactory() \
            .spike(config["INITIAL_SPIKE_USERS"]) \
            .ramp_up(config["RAMP_UP_USERS"], config["RAMP_UP_DURATION"]) \
            .steady_users(config["STEADY_USERS"], config["STEADY_DURATION"]) \
            .stress_ramp(config["STRESS_START_USERS"], config["STRESS_END_USERS"], config["STRESS_DURATION"]) \
            .build()

    def tick(self) -> Optional[Tuple[int, float]]:
        """
        Calculate the number of users and spawn rate for the current time.

        Returns:
            Optional[Tuple[int, float]]: A tuple of (user_count, spawn_rate) or None if no phase is active
        """
        run_time = self.get_run_time()

        for phase in self.phases:
            user_count = phase.user_count_at(run_time)
            if user_count is not None:
                return (user_count, phase.spawn_rate)

        return None 