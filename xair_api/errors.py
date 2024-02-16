class XAirRemoteError(Exception):
    """Base error class for XAIR Remote."""


class XAirRemoteConnectionTimeoutError(XAirRemoteError):
    """Exception raised when a connection attempt times out"""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        super().__init__(
            f"Timeout attempting to connect to mixer at {self.ip}:{self.port}"
        )
