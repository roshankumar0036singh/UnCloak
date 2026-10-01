class UncloakError(Exception):
    """Base exception for all uncloak errors."""


class NoCandidatesError(UncloakError):
    """Raised when no valid endpoints are found in the HAR."""


class UnreliableEndpointError(UncloakError):
    """Raised when the endpoint uses signed parameters or is otherwise unreliable."""


class ContractError(UncloakError):
    """Raised when an invalid contract is loaded."""


class AuthError(UncloakError):
    """Raised when authentication fails."""


class GraphQLNotSupportedError(UncloakError):
    """Raised when GraphQL endpoints are detected."""
