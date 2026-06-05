import time

def merge_dict(dict1, dict2):
    new_dict = dict1.copy()
    for key in dict2:
        if isinstance(dict2[key], dict):
            if key not in dict1:
                dict1[key] = {}
            new_dict[key] = merge_dict(dict1[key], dict2[key])
        elif isinstance(dict2[key], list):
            if key not in dict1:
                new_dict[key] = []
            new_dict[key].extend(dict2[key])
        else:
            new_dict[key] = dict2[key]
    return new_dict

def log_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.log.exception(e)
    return wrapper

def has_common_items(list1, list2):
    return bool(set(list1) & set(list2))

def is_included(li, target):
    '''
    Check if the target or one of the targets is included in the list.
    '''
    if isinstance(target, str):
        return target in li
    if isinstance(target, list):
        return has_common_items(li, target)
    return False


def get_varient_id_and_version():
    """Return board variant and version. Defaults to V50."""
    return "2602", "50"
