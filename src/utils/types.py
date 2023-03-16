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
