# Data:20220530
# Descript:最新版适用所有用到ssh/uart的自动化任务
# Version:1.5
# import logging
# import time
import time

from funct_ import *
import threading

import re
'''
双线程，任何一个线程结束，整个程序都会结束掉(线程1：uart循环执行：HOST跑业务期间uart进行收集信息然后判断温度；线程2：Host循环：上电、HOST跑业务、下电)，日志是两个；
R5和Host掉速/掉lan自行判断，或着后面有时间再加判断。
'''

uart_01 = ['dev temp\n']
ssh_01 = "fio fio.conf"

def SSH_01():
    Host_result = ssh_cmd(uart_)
    return Host_result
def UART_01():
    serial_cmd(uart_01)
    print('====进入uart ====')
    log_b.info('====打印温度====')

def thread1():
    """
    线程1 SSH程序跑FIO
    """
    while True:
        # 可以自行加for循环
        log_a.info("正在执行fio测试")
        power_monitor()
        time.sleep(1)
        log_a.info(SSH_01())
        time.sleep(10)
        log_a.info("Host端长时间fio已经跑完！！！")
        print("测试全部执行完毕-执行BMC关机操作！")
        break

def thread2():
    """
    线程2 UART程序NVME卡温度检测
    """
    while True:
        flag_v = host_sock()
        time.sleep(8)
        if flag_v == 0:
            print("ssh连接成功或在使用！此时持续进行uart信息收集")
            log_b.info("ssh连接成功或在使用！此时持续进行uart信息收集")
            UART_01()


def main():
    """
    主线程
    """

    t1 = threading.Thread(target=thread1, name="fun_thread1", daemon=True)  # 创建thread1线程
    t2 = threading.Thread(target=thread2, name="fun_thread2", daemon=True)  # 创建thread2线程
    t1.start()  # 启动thread1线程
    t2.start()  # 启动thread2线程

    #一共有3个线程，一个隐藏主线程，2个创建的子线程
    while True:
        if threading.active_count() < 3:
            break
        else:
            time.sleep(5)
    print("自动测试执行完毕！")

if __name__ == "__main__":
    log_a = log_1("eg1")
    log_b = log_2("eg2")
    main()

'''
    上面只是举个例子的代码，未进行实际测试，本人用过还可以，本人入门菜鸡勿喷。
'''




