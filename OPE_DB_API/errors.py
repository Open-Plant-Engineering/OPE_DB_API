class SessionNotActiveError(Exception):
    """
    Raised when an operation is attempted on a closed or inactive session.
    """

    def __init__(self, session_id: int):
        self.session_id = session_id
        super().__init__(f"Session {session_id} is not active")