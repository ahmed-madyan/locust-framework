"""
LoadShapeTest module for testing load shapes in the Locust Framework.
This module provides example implementations of user classes and load shapes
for testing the load shaping functionality.
"""

from locust import LoadTestShape, HttpUser, task, between
from typing import Optional, Tuple
from LoadProfileFactory import LoadProfileFactory


class MyUser(HttpUser):
    """
    A test user that simulates API calls to a dummy endpoint.
    
    This class demonstrates how to:
    1. Configure a user class for load testing
    2. Make HTTP requests to an API
    3. Handle responses and logging
    
    The user makes requests to reqres.in, a free API for testing.
    """
    host = "https://reqres.in/"  # Dummy endpoint for testing
    wait_time = between(1, 2)  # Wait between 1-2 seconds between tasks

    def on_start(self):
        """
        Initialize the user before starting tasks.
        This method is called once when each simulated user starts.
        """
        print("User started")

    # @task
    # def getUsersList(self) -> None:
    #     print("Executing getUsersList task")
    #     """Make a GET request to the dummy API endpoint."""
    #     response = self.client.get("/api/users", params={"page": "2"}, name="Get Users List")
    #     print(f"Response status code: {response.status_code}")
    #     print(f"Response content: {response.content}")

    @task
    def getUsersList(self) -> None:
        """
        Make a GET request to the dummy API endpoint.
        
        This task:
        1. Makes a GET request to /api/users
        2. Includes query parameters and headers
        3. Logs the response status and content
        """
        print("Executing getUsersList task")
        response = self.client.get("/api/users", params={"page": "2"}, headers={"x-api-key": "reqres-free-v1"},
                                   name="Get Users List")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")


class CustomLoadShape(LoadTestShape):
    """
    A custom load shape that implements a complex load pattern using multiple phases.
    
    This class demonstrates how to:
    1. Create a custom load shape for Locust
    2. Define different load phases (spike, ramp-up, steady, stress)
    3. Calculate user counts and spawn rates over time
    
    The load pattern consists of:
    - Initial spike: Quick increase to initial user count
    - Ramp up: Gradual increase to target user count
    - Steady state: Maintain constant user count
    - Stress test: Gradual increase to stress test user count
    """

    # LOAD TEST CONFIGURATION CONSTANTS
    INITIAL_SPIKE_USERS = 10    # Number of users for initial spike
    RAMP_UP_USERS = 20         # Target users for ramp-up phase
    RAMP_UP_DURATION = 10      # Duration of ramp-up in seconds
    STEADY_USERS = 5           # Number of users for steady state
    STEADY_DURATION = 5        # Duration of steady state in seconds
    STRESS_START_USERS = 5     # Starting users for stress test
    STRESS_END_USERS = 15      # Target users for stress test
    STRESS_DURATION = 10       # Duration of stress test in seconds

    def __init__(self) -> None:
        """
        Initialize the load shape with predefined phases.
        
        This method:
        1. Calls the parent class constructor
        2. Creates a load profile using LoadProfileFactory
        3. Configures all phases with their respective parameters
        """
        super().__init__()
        self.phases = LoadProfileFactory() \
            .spike(self.INITIAL_SPIKE_USERS) \
            .ramp_up(self.RAMP_UP_USERS, self.RAMP_UP_DURATION) \
            .steady_users(self.STEADY_USERS, self.STEADY_DURATION) \
            .stress_ramp(self.STRESS_START_USERS, self.STRESS_END_USERS, self.STRESS_DURATION) \
            .build()

    def tick(self) -> Optional[Tuple[int, float]]:
        """
        Calculate the number of users and spawn rate for the current time.
        
        This method:
        1. Gets the current run time
        2. Checks each phase to find the active one
        3. Returns the user count and spawn rate for the active phase
        
        Returns:
            Optional[Tuple[int, float]]: A tuple of (user_count, spawn_rate) or None if no phase is active
        """
        run_time = self.get_run_time()

        for phase in self.phases:
            user_count = phase.user_count_at(run_time)
            if user_count is not None:
                return (user_count, phase.spawn_rate)

        return None
