from locust import LoadTestShape, HttpUser, task, between
from typing import Optional, Tuple
from LoadProfileFactory import LoadProfileFactory


class MyUser(HttpUser):
    """
    A test user that simulates API calls to a dummy endpoint.
    """
    host = "https://reqres.in/"  # Dummy endpoint for testing
    wait_time = between(1, 2)  # Wait between 1-2 seconds between tasks

    def on_start(self):
        """Initialize the user before starting tasks."""
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
        print("Executing getUsersList task")
        """Make a GET request to the dummy API endpoint."""
        response = self.client.get("/api/users", params={"page": "2"}, headers={"x-api-key": "reqres-free-v1"},
                                   name="Get Users List")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")


class CustomLoadShape(LoadTestShape):
    """
    A custom load shape that implements a complex load pattern using multiple phases:
    - Initial spike
    - Ramp up
    - Steady state
    - Stress test
    """

    # LOAD TEST CONFIGURATION CONSTANTS
    INITIAL_SPIKE_USERS = 10
    RAMP_UP_USERS = 20
    RAMP_UP_DURATION = 10
    STEADY_USERS = 5
    STEADY_DURATION = 5
    STRESS_START_USERS = 5
    STRESS_END_USERS = 15
    STRESS_DURATION = 10

    def __init__(self) -> None:
        """Initialize the load shape with predefined phases."""
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
        
        Returns:
            Optional[Tuple[int, float]]: A tuple of (user_count, spawn_rate) or None if no phase is active
        """
        run_time = self.get_run_time()

        for phase in self.phases:
            user_count = phase.user_count_at(run_time)
            if user_count is not None:
                return (user_count, phase.spawn_rate)

        return None
