import time

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
            self.called = True
            return self.func(*self.preset_args, *args, **self.preset_kwargs, **kwargs)
        elif self.last_call is None or time.time() - self.last_call > self.interval:
            self.last_call = time.time()
            self.called = True
            return self.func(*self.preset_args, *args, **self.preset_kwargs, **kwargs)
        else:
            return None

    def reset(self):
        '''
        Reset the state for the next call.
        '''
        self.last_call = None
        self.called = False
