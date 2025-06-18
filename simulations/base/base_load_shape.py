from locust import LoadTestShape, events
from typing import Optional, Tuple
from load_shaper.LoadProfileFactory import LoadProfileFactory
from config import LoadShaperConfig


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
        self.phases = LoadProfileFactory() \
            .spike(LoadShaperConfig.INITIAL_SPIKE_USERS) \
            .build()
            # .ramp_up(LoadShaperConfig.RAMP_UP_USERS, LoadShaperConfig.RAMP_UP_DURATION) \
            # .steady_users(LoadShaperConfig.STEADY_USERS, LoadShaperConfig.STEADY_DURATION) \
            # .stress_ramp(LoadShaperConfig.STRESS_START_USERS, LoadShaperConfig.STRESS_END_USERS, LoadShaperConfig.STRESS_DURATION) \
            # .build()

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


# Register the shape class with Locust
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    environment.shape_class = BaseLoadShape
