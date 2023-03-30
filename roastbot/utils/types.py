from typing import Union

def ConvertBool(var: Union[int, str]) -> bool:
    """converts a string or integer into a boolean.

    Args:
        var (Union[int, str]): The integer or string

    Returns:
        bool: Defaults to false however if 1, true, yes or ok is found it'll return true
    """
    bool_list_true = ["1", "true", "yes", "ok"]
    if str(var).strip().lower() in bool_list_true:
        return True
    return False

def wrap(msg: str) -> str:
    """Wraps a message in the # character

    Args:
        msg (str): The message to wrap

    Returns:
        str: Returns the wrapped message.
    """
    msg = f'# {msg} #'
    wrp = "#".replace("#", '#'*len(msg), 1)
    return f'{wrp}\n{msg}\n{wrp}\n'

class Singleton(type):
    """Singleton Metaclass

    This class will keep track of a given class and make sure there's only one instance at a time.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class obj(object):
    """Callable object class

    This class can help generate the object structure.
    """
    def __init__(self, _name: str):
        self._name = _name

    def set(self, _name: str, _value: any) -> None:
        setattr(self, _name, _value)
    
    def get(self, _name: str) -> any:
        return getattr(self, _name)

    def __getattr__(self, _name: str) -> None:
        """ Fallback to prevent AttributeError
        Args:
            _name (str): The attribute name

        Returns:
            None: Will always return none.
        """
        return None