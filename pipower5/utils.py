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


def get_device_tree_path():
    """
    获取设备树路径。
    
    Returns:
        str: 设备树路径，如果不存在则返回None。
    """
    from os import path
    device_tree_path = '/proc/device-tree'
    if not path.exists(device_tree_path):
        device_tree_path = '/device-tree'
        if not path.exists(device_tree_path):
            return None
    return device_tree_path

def read_device_tree_file(file_path):
    from os import path
    if not path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        result = f.read()[:-1]
        result = int(result, 16)
        return result

def get_part_number():
    """
    获取HAT设备的版本号。
    
    如果未发现HAT设备或发生错误，则返回错误码。
    
    Returns:
        str: HAT设备的PN号。
    """
    from os import listdir
    device_tree_path = get_device_tree_path()
    part_number = ""
    if device_tree_path is None:
        return
    hat_path = None
    for file in listdir(device_tree_path):
        if file.startswith('hat'):
            hat_path = f"{device_tree_path}/{file}"
            break
    if hat_path is None:
        return
    product_id_file = f"{hat_path}/product_id"
    product_ver_file = f"{hat_path}/product_ver"

    try:
        product_id = read_device_tree_file(product_id_file)
        product_ver = read_device_tree_file(product_ver_file)
        if product_id is None or product_ver is None:
            return
        part_number = f"{product_id:04d}V{product_ver:02d}"
    except Exception as e:
        # print(f"Error: {e}")
        pass
    
    return part_number

def get_varient_id_and_version():
    import os
    # Set Variant
    # Check environment variable PIRONMAN5_PART_NUMBER
    part_number = os.getenv('PIRONMAN5_PART_NUMBER', None)
    if part_number == None:
        # Get variant from hat info
        part_number = get_part_number()
    if part_number == None:
        part_number = "0306V10"
    # Set variant
    varient_id = part_number.split('V')[0]
    version_id = part_number.split('V')[1]
    return varient_id, version_id

class LazyCaller:
    def __init__(self, func, *args, interval=1, oneshot=False, **kwargs):
        '''
        Lazy caller.

        Args:
            func (function): Function to call.
            interval (int, optional): Interval in seconds. Defaults to 1.
            oneshot (bool, optional): Call only once. Defaults to False.
            *args: Preset args to pass to the function.
            **kwargs: Preset kwargs to pass to the function.
        '''
        self.func = func
        self.last_call = None
        self.interval = interval
        self.preset_args = args
        self.preset_kwargs = kwargs
        self.oneshot = oneshot
        self.called = False

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        '''
        Call the function if the interval is reached.

        Returns:
            Any: The return value of the function.
        '''
        if self.oneshot:
            if self.called:
                return None
        elif self.last_call is None or time.time() - self.last_call > self.interval:
            self.last_call = time.time()
            self.called = True
            return self.func(*self.preset_args, *args, **self.preset_kwargs, **kwargs)

    def reset(self):
        '''
        Reset the state for the next call.
        '''
        self.last_call = None
        self.called = False
