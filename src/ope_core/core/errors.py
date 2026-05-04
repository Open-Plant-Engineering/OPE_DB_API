class OpeCoreError(Exception):
    """
    Base class for all domain-level errors in ope_core.
    """
    pass


class SessionError(OpeCoreError):
    """
    Base class for session-related errors.
    """
    pass


class SessionNotActiveError(SessionError):
    """
    Raised when an operation is attempted on a closed or inactive session.
    """

    def __init__(self, session_id: int):
        self.session_id = session_id
        super().__init__(f"Session {session_id} is not active")


class SessionNotFoundError(SessionError):
    """
    Raised when a session_id does not exist.
    """

    def __init__(self, session_id: int):
        self.session_id = session_id
        super().__init__(f"Session {session_id} not found")