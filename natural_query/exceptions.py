class NaturalQueryError(Exception):
    """Base class for all errors in Natural Query."""
    pass


class QueryBuilderError(NaturalQueryError):
    """Raised for errors in the QueryBuilder."""
    pass
