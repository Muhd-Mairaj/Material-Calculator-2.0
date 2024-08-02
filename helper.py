import warnings
import functools

def deprecated(cls):
    """This decorator can be used to mark classes as deprecated.
    It will result in a warning being emitted when the class is instantiated."""
    
    @functools.wraps(cls)
    def new_cls(*args, **kwargs):
        warnings.warn(f"{cls.__name__} is deprecated.", 
                      category=DeprecationWarning, 
                      stacklevel=2)
        return cls(*args, **kwargs)
    
    return new_cls
