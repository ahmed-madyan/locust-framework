from locust import LoadTestShape
from typing import Optional, Tuple, List
from load_shaper.LoadProfileFactory import LoadProfileFactory
from load_shaper.Phase import Phase
from config import LoadShaperConfig
import threading
from queue import Queue
import time


class BaseLoadShape(LoadTestShape):
    """
    Base class for all LoadTestShape implementations that provides common initialization logic.
    Implements a complex load pattern using multiple phases with multi-threading support:
    - Initial spike
    - Ramp up
    - Steady state
    - Stress test
    """

    def __init__(self) -> None:
        """Initialize the load shape with predefined phases and thread management."""
        super().__init__()
        self.phases = LoadProfileFactory() \
            .spike(LoadShaperConfig.INITIAL_SPIKE_USERS) \
            .ramp_up(LoadShaperConfig.RAMP_UP_USERS, LoadShaperConfig.RAMP_UP_DURATION) \
            .steady_users(LoadShaperConfig.STEADY_USERS, LoadShaperConfig.STEADY_DURATION) \
            .stress_ramp(LoadShaperConfig.STRESS_START_USERS, LoadShaperConfig.STRESS_END_USERS, LoadShaperConfig.STRESS_DURATION) \
            .build()
        
        # Thread management
        self._lock = threading.Lock()
        self._active_threads = []
        self._thread_queue = Queue()
        self._stop_event = threading.Event()
        self._phase_lock = threading.Lock()
        self._current_phase_index = 0
        self._phase_start_time = time.time()

    def _execute_phase(self, phase: Phase, thread_id: int):
        """
        Execute a single phase in a separate thread.
        
        Args:
            phase: The phase to execute
            thread_id: Unique identifier for the thread
        """
        try:
            while not self._stop_event.is_set():
                with self._phase_lock:
                    current_time = time.time() - self._phase_start_time
                    if current_time > phase.duration:
                        break
                    
                    user_count = phase.user_count_at(current_time)
                    if user_count is not None:
                        self._thread_queue.put((user_count, phase.spawn_rate))
                
                time.sleep(0.1)  # Prevent CPU overuse
        except Exception as e:
            print(f"Error in thread {thread_id}: {str(e)}")
        finally:
            with self._lock:
                if thread_id in self._active_threads:
                    self._active_threads.remove(thread_id)

    def start_phases(self):
        """Start all phases in separate threads."""
        self._stop_event.clear()
        self._phase_start_time = time.time()
        
        for i, phase in enumerate(self.phases):
            thread = threading.Thread(
                target=self._execute_phase,
                args=(phase, i),
                name=f"PhaseThread-{i}"
            )
            thread.daemon = True
            thread.start()
            with self._lock:
                self._active_threads.append(i)

    def stop_phases(self):
        """Stop all running phase threads."""
        self._stop_event.set()
        for thread_id in self._active_threads[:]:
            thread = threading.Thread(
                target=lambda: self._active_threads.remove(thread_id) if thread_id in self._active_threads else None
            )
            thread.start()
            thread.join(timeout=1.0)

    def tick(self) -> Optional[Tuple[int, float]]:
        """
        Calculate the number of users and spawn rate for the current time.
        This method is thread-safe and supports multiple concurrent phases.

        Returns:
            Optional[Tuple[int, float]]: A tuple of (user_count, spawn_rate) or None if no phase is active
        """
        try:
            # Non-blocking check for new values
            if not self._thread_queue.empty():
                return self._thread_queue.get_nowait()
        except Exception:
            pass
        
        return None

    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop_phases()
