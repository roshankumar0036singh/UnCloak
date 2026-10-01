from uncloak.exceptions import (
    UncloakError,
    NoCandidatesError,
    UnreliableEndpointError,
    ContractError,
    AuthError,
    GraphQLNotSupportedError,
)

def test_exception_inheritance():
    assert issubclass(NoCandidatesError, UncloakError)
    assert issubclass(UnreliableEndpointError, UncloakError)
    assert issubclass(ContractError, UncloakError)
    assert issubclass(AuthError, UncloakError)
    assert issubclass(GraphQLNotSupportedError, UncloakError)

def test_exception_instantiation():
    err = AuthError("Missing token")
    assert str(err) == "Missing token"
    assert isinstance(err, Exception)
