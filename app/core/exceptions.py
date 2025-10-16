class FocusGuardException(Exception):
    """Base exception for FocusGuard application"""
    pass

class DatabaseException(FocusGuardException):
    """Database related exceptions"""
    pass

class BusinessException(FocusGuardException):
    """Business logic exceptions"""
    pass

class ValidationException(FocusGuardException):
    """Data validation exceptions"""
    pass

class NotFoundException(FocusGuardException):
    """Resource not found exceptions"""
    pass

class AuthenticationException(FocusGuardException):
    """Authentication related exceptions"""
    pass