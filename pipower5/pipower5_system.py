from .utils import log_error

from sf_rpi_status import \
    get_cpu_temperature, \
    get_gpu_temperature, \
    get_cpu_percent, \
    get_cpu_freq, \
    get_cpu_count, \
    get_memory_info, \
    get_disks, \
    get_disks_info, \
    get_boot_time, \
    get_ips, \
    get_macs, \
    get_network_connection_type, \
    get_network_speed

import time
import asyncio
import threading
from typing import Callable

class TaskScheduler:
    """极简异步任务调度系统，通过回调暴露关键节点"""
    
    def __init__(self):
        self.scheduler = {}  # 存储所有任务
        self._stop_event = asyncio.Event()
        self._callbacks = {
            "task_start": [],
            "task_complete": [],
            "task_error": [],
            "task_cancel": [],
        }
    
    def add_callback(self, event_type: str, callback: Callable) -> None:
        """
        注册事件回调
        
        Args:
            event_type: 事件类型，可选值: task_start, task_complete, task_error, task_cancel
            callback: 回调函数，接受任务ID和相关数据作为参数
        """
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)
    
    def _trigger_callback(self, event_type: str, task_id: str, **kwargs) -> None:
        """触发事件回调"""
        for callback in self._callbacks[event_type]:
            callback(task_id, **kwargs)
    
    async def run_once(self, func: Callable, delay: float = 0, *args, **kwargs) -> str:
        """注册一次性任务"""
        task_id = f"once-{int(time.time()*1000)}-{len(self.scheduler)}"
        
        async def _wrapper():
            await asyncio.sleep(delay)
            if not self._stop_event.is_set():
                self._trigger_callback("task_start", task_id, task_type="once")
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    self._trigger_callback("task_complete", task_id, result=result)
                except Exception as e:
                    self._trigger_callback("task_error", task_id, error=e)
                finally:
                    self.scheduler.pop(task_id, None)
        
        self.scheduler[task_id] = asyncio.create_task(_wrapper())
        return task_id
    
    async def run_periodically(self, func: Callable, interval: float, initial_delay: float = 0, *args, **kwargs) -> str:
        """注册周期性任务"""
        task_id = f"periodic-{int(time.time()*1000)}-{len(self.scheduler)}"
        
        async def _wrapper():
            if initial_delay > 0:
                await asyncio.sleep(initial_delay)
                
            while not self._stop_event.is_set():
                start_time = time.time()
                self._trigger_callback("task_start", task_id, task_type="periodic")
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    self._trigger_callback("task_complete", task_id, result=result, duration=time.time()-start_time)
                except Exception as e:
                    self._trigger_callback("task_error", task_id, error=e, duration=time.time()-start_time)
                
                # 计算执行耗时并调整下一次执行时间
                elapsed = time.time() - start_time
                wait_time = max(0, interval - elapsed)
                await asyncio.sleep(wait_time)
        
        self.scheduler[task_id] = asyncio.create_task(_wrapper())
        return task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """取消指定任务"""
        task = self.scheduler.pop(task_id, None)
        if task:
            task.cancel()
            self._trigger_callback("task_cancel", task_id)
            return True
        return False
    
    def cancel_all_tasks(self) -> None:
        """取消所有任务"""
        for task_id in list(self.scheduler.keys()):
            self.cancel_task(task_id)

    async def stop(self) -> None:
        """停止调度器并清理资源"""
        self._stop_event.set()
        self.cancel_all_tasks()
        if self.scheduler:
            await asyncio.gather(*self.scheduler.values(), return_exceptions=True)

class PiPower5System():
    def __init__(self, peripherals=None, log=None):
        self.peripherals = peripherals
        self.log = log
        self.__before_shutdown__ = None
        self.__on_data_changed__ = None
        self.scheduler = TaskScheduler()

        self.task = None
        self.running = False
        self.loop = None
        self.loop_thread = None

        self._is_ready = True

    @log_error
    def set_before_shutdown(self, callback):
        self.__before_shutdown__ = callback

    @log_error
    def set_on_data_changed(self, callback):
        self.__on_data_changed__ = callback

    @log_error
    def shutdown(self, reason):
        if reason != 'None' or reason != None or reason != 0:
            self.log.info(f"Shutdown reason: {reason}")
            if self.__before_shutdown__:
                self.__before_shutdown__(reason)
            time.sleep(2)

            try:
                from sf_rpi_status import shutdown
                shutdown()
            except Exception as e:
                self.log.error(f"Failed to shutdown: {e}")
                from os import system
                system("sudo shutdown -h now")

    @log_error
    def task_once(self):
        data = {}
        if 'cpu' in self.peripherals:
            data['cpu_count'] = int(get_cpu_count())
        if 'mac_address' in self.peripherals:
            macs = get_macs()
            for name in macs:
                data[f'mac_{name}'] = macs[name]
        if self.__on_data_changed__:
            self.__on_data_changed__(data)

    @log_error
    def task_1s(self):
        data = {}
        data['boot_time'] = float(get_boot_time())

        if 'cpu_temperature' in self.peripherals:
            data['cpu_temperature'] = float(get_cpu_temperature()) if get_cpu_temperature() is not None else None
        if 'gpu_temperature' in self.peripherals:
            data['gpu_temperature'] = float(get_gpu_temperature()) if get_gpu_temperature() is not None else None
        if 'cpu' in self.peripherals:
            cpu_percent = get_cpu_percent()
            data['cpu_percent'] = float(cpu_percent)
            cpu_percents = get_cpu_percent(percpu=True)
            for i, percent in enumerate(cpu_percents):
                data[f'cpu_{i}_percent'] = float(percent)
            cpu_freq = get_cpu_freq()
            data['cpu_freq'] = float(cpu_freq.current)
            data['cpu_freq_min'] = float(cpu_freq.min)
            data['cpu_freq_max'] = float(cpu_freq.max)
        if 'memory' in self.peripherals:
            memory = get_memory_info()
            data['memory_total'] = int(memory.total)
            data['memory_available'] = int(memory.available)
            data['memory_percent'] = float(memory.percent)
            data['memory_used'] = int(memory.used)

        if 'network' in self.peripherals:
            network_speed = get_network_speed()
            data['network_upload_speed'] = int(network_speed.upload)
            data['network_download_speed'] = int(network_speed.download)
    
        if self.__on_data_changed__:
            self.__on_data_changed__(data)

    @log_error
    def task_3s(self):
        data = {}
        if 'ip_address' in self.peripherals:
            ips = get_ips()
            data['ips'] = ips
            for name in ips:
                data[f'ip_{name}'] = ips[name]

        if 'network' in self.peripherals:
            network_connection_type = get_network_connection_type()
            data['network_type'] = "&".join(network_connection_type)

        if self.__on_data_changed__:
            self.__on_data_changed__(data)

    @log_error
    def task_5s(self):
        data = {}
        if 'storage' in self.peripherals:
            data['disk_list'] = get_disks()
            disks = get_disks_info(temperature=True)
            data['disks'] = disks
            for disk_name in disks:
                disk = disks[disk_name]
                data[f'disk_{disk_name}_mounted'] = int(disk.mounted)
                data[f'disk_{disk_name}_total'] = int(disk.total)
                data[f'disk_{disk_name}_used'] = int(disk.used)
                data[f'disk_{disk_name}_free'] = int(disk.free)
                data[f'disk_{disk_name}_percent'] = float(disk.percent)
        
        if self.__on_data_changed__:
            self.__on_data_changed__(data)

    @log_error
    async def main(self):
        self.log.debug("SystemAddon main loop started")
        await self.scheduler.run_once(self.task_once, 1)
        await self.scheduler.run_periodically(self.task_1s, 1)
        await self.scheduler.run_periodically(self.task_3s, 3)
        await self.scheduler.run_periodically(self.task_5s, 5)
        while self.running:
            await asyncio.sleep(1)

    @log_error
    def start(self):
        if self.running:
            self.log.warning("Already running")
            return
        
        self.running = True
        # 创建新的事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # 在新线程中运行事件循环
        self.loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.loop_thread.start()
        # 在事件循环中创建并运行任务
        self.loop.call_soon_threadsafe(self._start_loop_task)
        self.log.info("PiPower5 service started")

    def _run_loop(self):
        """在线程中运行事件循环"""
        try:
            self.loop.run_forever()
        except Exception as e:
            self.log.error(f"Event loop error: {e}")
        finally:
            self.loop.close()
            self.log.debug("Event loop closed")

    def _start_loop_task(self):
        """在事件循环中创建并启动任务"""
        self.task = self.loop.create_task(self.main())

    @log_error
    def stop(self):
        if not self.running or self.task is None:
            self.log.warning("Service not running")
            return
            
        self.running = False
        
        # 如果任务已完成，直接返回
        if self.task.done():
            return
            
        # 取消任务
        self.loop.call_soon_threadsafe(self.task.cancel)
        
        # 停止事件循环
        self.loop.call_soon_threadsafe(self.loop.stop)
        
        # 等待线程结束
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join(timeout=2.0)
                
        self.log.info("PiPower5 service stopped")

