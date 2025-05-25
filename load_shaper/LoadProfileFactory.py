from load_shaper.Phase import Phase
from logger import logger


class LoadProfileFactory:
    def __init__(self):
        self.phases = []
        self.current_time = 0
        logger.debug("LoadProfileFactory initialized")

    def spike(self, users):
        """Create a spike phase with immediate user count change."""
        self.phases.append(Phase(self.current_time, 0.1, users, users, users))
        self.current_time += 0.1
        logger.info("Spike phase added", 
                   users=users,
                   start_time=self.current_time - 0.1,
                   duration=0.1)
        return self

    def ramp_up(self, to_users, duration):
        """Create a ramp-up phase with gradual user count increase."""
        from_users = self.phases[-1].user_end if self.phases else 0
        self.phases.append(Phase(self.current_time, duration, from_users, to_users, (to_users - from_users) / duration))
        self.current_time += duration
        logger.info("Ramp-up phase added", 
                   from_users=from_users,
                   to_users=to_users,
                   duration=duration,
                   start_time=self.current_time - duration)
        return self

    def steady_users(self, users, duration):
        """Create a steady phase with constant user count."""
        self.phases.append(Phase(self.current_time, duration, users, users, 1))
        self.current_time += duration
        logger.info("Steady phase added", 
                   users=users,
                   duration=duration,
                   start_time=self.current_time - duration)
        return self

    def stress_ramp(self, from_users, to_users, duration):
        """Create a stress test phase with gradual user count increase."""
        self.phases.append(Phase(self.current_time, duration, from_users, to_users, (to_users - from_users) / duration))
        self.current_time += duration
        logger.info("Stress ramp phase added", 
                   from_users=from_users,
                   to_users=to_users,
                   duration=duration,
                   start_time=self.current_time - duration)
        return self

    def build(self):
        """Build and return the complete load profile."""
        logger.info("Load profile built", 
                   total_phases=len(self.phases),
                   total_duration=self.current_time)
        return self.phases
