"""
LoadProfileFactory module for creating load test profiles in the Locust Framework.
This module provides a factory class for building complex load test profiles by
combining different types of load phases (spike, ramp-up, steady, stress).
"""

from load_shaper.Phase import Phase
from logger import logger


class LoadProfileFactory:
    """
    Factory class for creating load test profiles.
    
    This class provides a fluent interface for building load test profiles by
    combining different types of load phases. It maintains the current time
    and automatically chains phases together.
    
    Example usage:
        profile = LoadProfileFactory() \
            .spike(10) \                    # Initial spike of 10 users
            .ramp_up(50, 30) \             # Ramp up to 50 users over 30 seconds
            .steady_users(50, 60) \        # Maintain 50 users for 60 seconds
            .stress_ramp(50, 100, 30) \    # Stress test from 50 to 100 users
            .build()
    """
    
    def __init__(self):
        """
        Initialize a new LoadProfileFactory.
        Creates an empty list of phases and sets the current time to 0.
        """
        self.phases = []
        self.current_time = 0
        logger.debug("LoadProfileFactory initialized")

    def spike(self, users):
        """
        Create a spike phase with immediate user count change.
        
        A spike phase is used to quickly increase the number of users to a
        specific value. It has a very short duration (0.1 seconds) to simulate
        an immediate change.
        
        Args:
            users (int): The number of users to spike to
            
        Returns:
            LoadProfileFactory: The factory instance for method chaining
        """
        self.phases.append(Phase(self.current_time, 0.1, users, users, users))
        self.current_time += 0.1
        logger.info("Spike phase added", 
                   users=users,
                   start_time=self.current_time - 0.1,
                   duration=0.1)
        return self

    def ramp_up(self, to_users, duration):
        """
        Create a ramp-up phase with gradual user count increase.
        
        A ramp-up phase gradually increases the number of users from the
        previous phase's end count to a target number over a specified duration.
        
        Args:
            to_users (int): The target number of users to ramp up to
            duration (float): How long the ramp-up should take (in seconds)
            
        Returns:
            LoadProfileFactory: The factory instance for method chaining
        """
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
        """
        Create a steady phase with constant user count.
        
        A steady phase maintains a constant number of users for a specified duration.
        This is useful for testing system stability under constant load.
        
        Args:
            users (int): The number of users to maintain
            duration (float): How long to maintain the user count (in seconds)
            
        Returns:
            LoadProfileFactory: The factory instance for method chaining
        """
        self.phases.append(Phase(self.current_time, duration, users, users, 1))
        self.current_time += duration
        logger.info("Steady phase added", 
                   users=users,
                   duration=duration,
                   start_time=self.current_time - duration)
        return self

    def stress_ramp(self, from_users, to_users, duration):
        """
        Create a stress test phase with gradual user count increase.
        
        A stress ramp phase is similar to a ramp-up phase but is specifically
        designed for stress testing. It gradually increases the user count
        from a starting value to a higher target value over a specified duration.
        
        Args:
            from_users (int): The starting number of users
            to_users (int): The target number of users to ramp up to
            duration (float): How long the stress ramp should take (in seconds)
            
        Returns:
            LoadProfileFactory: The factory instance for method chaining
        """
        self.phases.append(Phase(self.current_time, duration, from_users, to_users, (to_users - from_users) / duration))
        self.current_time += duration
        logger.info("Stress ramp phase added", 
                   from_users=from_users,
                   to_users=to_users,
                   duration=duration,
                   start_time=self.current_time - duration)
        return self

    def build(self):
        """
        Build and return the complete load profile.
        
        This method finalizes the load profile by returning the list of phases
        that have been configured. It logs the total number of phases and
        the total duration of the load test.
        
        Returns:
            List[Phase]: The complete list of load test phases
        """
        logger.info("Load profile built", 
                   total_phases=len(self.phases),
                   total_duration=self.current_time)
        return self.phases
