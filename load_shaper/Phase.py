from logger import logger

class Phase:
    def __init__(self, start_time, duration, user_start, user_end, spawn_rate):
        self.start_time = start_time
        self.duration = duration
        self.user_start = user_start
        self.user_end = user_end
        self.spawn_rate = spawn_rate
        logger.debug("Phase initialized", 
                    start_time=start_time,
                    duration=duration,
                    user_start=user_start,
                    user_end=user_end,
                    spawn_rate=spawn_rate)

    def user_count_at(self, t):
        """Calculate the number of users at a given time."""
        if t < self.start_time or t > self.start_time + self.duration:
            logger.debug("Time outside phase bounds", 
                        time=t,
                        phase_start=self.start_time,
                        phase_end=self.start_time + self.duration)
            return None
            
        if self.duration == 0:
            logger.debug("Instant phase transition", 
                        user_count=self.user_end)
            return self.user_end
            
        # Linear interpolation
        progress = (t - self.start_time) / self.duration
        user_count = int(self.user_start + (self.user_end - self.user_start) * progress)
        logger.debug("User count calculated", 
                    time=t,
                    progress=progress,
                    user_count=user_count)
        return user_count
