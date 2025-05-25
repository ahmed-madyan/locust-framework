"""
Phase module for defining load test phases in the Locust Framework.
This module provides a class for representing a single phase in a load test,
where a phase defines how the number of users changes over time.
"""

from logger import logger

class Phase:
    """
    Represents a single phase in a load test.
    
    A phase defines how the number of users changes over a specific time period.
    It supports linear interpolation between start and end user counts.
    
    Attributes:
        start_time (float): When this phase starts (in seconds)
        duration (float): How long this phase lasts (in seconds)
        user_start (int): Number of users at the start of the phase
        user_end (int): Number of users at the end of the phase
        spawn_rate (float): Rate at which users are spawned (users per second)
    """
    
    def __init__(self, start_time, duration, user_start, user_end, spawn_rate):
        """
        Initialize a new load test phase.
        
        Args:
            start_time (float): When this phase starts (in seconds)
            duration (float): How long this phase lasts (in seconds)
            user_start (int): Number of users at the start of the phase
            user_end (int): Number of users at the end of the phase
            spawn_rate (float): Rate at which users are spawned (users per second)
        """
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
        """
        Calculate the number of users at a given time.
        
        This method:
        1. Checks if the time is within the phase bounds
        2. Handles instant phase transitions (duration = 0)
        3. Uses linear interpolation to calculate user count for times within the phase
        
        Args:
            t (float): The time to calculate the user count for (in seconds)
            
        Returns:
            int: The number of users at time t, or None if t is outside the phase bounds
        """
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
            
        # Linear interpolation between start and end user counts
        progress = (t - self.start_time) / self.duration
        user_count = int(self.user_start + (self.user_end - self.user_start) * progress)
        logger.debug("User count calculated", 
                    time=t,
                    progress=progress,
                    user_count=user_count)
        return user_count
