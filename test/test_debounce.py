import time

class Debounce:
    """
    A debounce mechanism to handle value changes with stability checks.
    
    Ensures that a value is only updated after it has remained stable for a 
    specified timeout period. Supports both function-based value reading and 
    direct value passing.
    """
    def __init__(self, func=None, timeout=0.5):
        """
        Initialize the debounce mechanism.
        
        :param func: Optional function to read the current value
        :param timeout: Stability timeout in seconds (default: 0.5)
        """
        self.func = func          # Function to read values (optional)
        self.timeout = timeout    # Stability timeout in seconds
        self.last_check_time = 0  # Timestamp of the last value change check
        self.stable_value = None  # Confirmed stable value (returned by default)
        self.pending_value = None # Temporary new value waiting for stability check
        self.is_monitoring = False # Flag indicating if monitoring a pending value

    def __call__(self, value=None):
        """
        Get the current value with debounce processing.
        
        :param value: New value to process (required if no func is provided)
        :return: The stable value after debounce processing
        """
        # Get current value (prioritize function output if available)
        current_value = self.func() if self.func is not None else value

        # Initialize on first call
        if self.stable_value is None:
            self.stable_value = current_value
            return self.stable_value

        # Return stable value if no change detected
        if current_value == self.stable_value:
            self.is_monitoring = False
            self.pending_value = None
            return self.stable_value

        # Start monitoring if new value differs from pending value
        if current_value != self.pending_value:
            self.pending_value = current_value
            self.last_check_time = time.time()
            self.is_monitoring = True
            return self.stable_value  # Return old value while monitoring

        # Check if timeout has been reached
        elapsed = time.time() - self.last_check_time
        if elapsed >= self.timeout:
            # Update stable value if new value remains stable
            self.stable_value = self.pending_value
            self.pending_value = None
            self.is_monitoring = False
            return self.stable_value

        # Return old value if timeout not reached
        return self.stable_value

    def __str__(self):
        """String representation of the debounce state."""
        func_name = self.func.__name__ if self.func else "None"
        return (f"Debounce(func={func_name}, timeout={self.timeout}, "
                f"stable_value={self.stable_value}, pending_value={self.pending_value})")

# 测试1：通过函数获取值的场景
def test_func():
    return 10  # 可模拟动态变化的传感器值

debounce1 = Debounce(func=test_func, timeout=1)
print(debounce1())  # 首次调用，返回10

# 测试2：直接传入值的场景
debounce2 = Debounce(timeout=2)
print(f"Get: {debounce2(True)}, expect: True")   # 首次调用，返回True
time.sleep(1)
print(f"Get: {debounce2(False)}, expect: True")   # 一秒后，读到False，返回True
time.sleep(1)
print(f"Get: {debounce2(False)}, expect: True")   # 再过一秒，返回True
time.sleep(1)
print(f"Get: {debounce2(False)}, expect: False")   # 再过一秒，返回False
time.sleep(1)
print(f"Get: {debounce2(False)}, expect: False")   # 再过一秒，返回False

