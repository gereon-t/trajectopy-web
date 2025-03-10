class ResultNotFoundException(Exception):
    def __init__(self, result_id: str):
        super().__init__(f"Result with id {result_id} not found")


class SessionNotFoundException(Exception):
    def __init__(self, session_id: str):
        super().__init__(f"Session with id {session_id} not found")


class TrajectoryNotFoundException(Exception):
    def __init__(self, trajectory_id: str):
        super().__init__(f"Trajectory with id {trajectory_id} not found")


class SessionAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Session already exists")
