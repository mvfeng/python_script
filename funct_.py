# Data:20220530
# Descript:最新版适用所有用到ssh/uart的自动化任务
# Version:1.5
import paramiko  # SSH使用必要的模块
import socket    # 端口检测必要的模块
import serial    # UART使用必要模块
import os        # 调用windows系统模块
import time
from config_ import *
# import msvcrt
import logging
# from sendmail import Mail

# def log_init(name_):
#     log_filename = LOG_DIR + name_ + ".log"
#     logger = logging.getLogger()
#     logging.basicConfig(filename=log_filename, format=LOG_FORMAT, level=LOG_LEVEL)
#     return logger

def log_1(name_):
    # 定义文件
    file1 = logging.FileHandler(filename=str(name_)+'.log', mode='a', encoding='utf-8')
    fmt = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    file1.setFormatter(fmt)

    # 定义日志
    logger1 = logging.Logger(name='log_1', level=logging.INFO)
    logger1.addHandler(file1)
    return logger1

def log_2(name_):
    # 定义文件
    file2 = logging.FileHandler(filename=str(name_)+'.log', mode='a', encoding='utf-8')
    fmt = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    file2.setFormatter(fmt)

    # 定义日志
    logger2 = logging.Logger(name='log_2', level=logging.INFO)
    logger2.addHandler(file2)
    return logger2


def anykey_go():
    print("自动模式/提前连好xxx")
    # while True:
    #     key=input("如果您已经完成按 'D' 或 'd' 继续下一步...\n")
    #     if key == "D":
    #         break
    #     elif key == "d":
    #         break

# uart串口交互功能函数
def serial_open(port, bps, timeouts):
    serial_obj =serial.Serial(port, bps, timeout=timeouts)  # 打开串口，并得到串口对象
    return serial_obj
def serial_cmd(cmd):
    serial_obj = serial_open(UART_PORT, UART_BAUDRATE, UART_TIMEOUT)
    # print(serial_obj.is_open)
    for line in cmd:
        serial_obj.write(line.encode("utf-8"))  # 写数据
        time.sleep(0.01) # 必须添加
    r_data = serial_obj.readlines()
    rdata = []
    for i in r_data:
        i = i.decode("utf-8", "ignore")
        rdata.append(i[:-2])
    if serial_obj.is_open:
        serial_obj.close()
    return rdata

# ssh交互功能函数
def ssh_connect(host_ip,host_port,host_name,host_password,cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_ip, port=host_port, username=host_name, password=host_password, timeout=None, allow_agent=False,look_for_keys=False)
    stdin, stdout, stderr = client.exec_command(str(cmd)+" 1>&2")
    result_info = ""
    for line in stderr.readlines():
        result_info += line
    client.close()
    return result_info

def ssh_cmd(cmd):
    ssh_result=ssh_connect(HOST_IP,HOST_PORT,HOST_USERNAME,HOST_PASSWORD,cmd)
#   print("ssh connect success!")
    return ssh_result

def ssh_cmd2(cmd):
    ssh_result=ssh_connect(HOST_IP2,HOST_PORT2,HOST_USERNAME2,HOST_PASSWORD2,cmd)
#   print("ssh connect success!")
    return ssh_result

# 端口检测功能函数
def host_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((HOST_IP, HOST_PORT))  # 判断22端口是否开启（方便判断是否进入OS以及是否ssh连接）
    if 0 == result:
        # print("Port 22 is open!")
        pass
    else:
        # print("Port 22 is not open，return code：%s" % result)
        pass
    return result  # 状态码0表端口开启，否则未开启

# bmc上下电服务器功能函数（有待考量是否上下电和直接reboot的区别？？？）
def power_on():
    os.system(IPMITOOL_PATH+" -I lanplus" + " -U " + BMC_USERNAME + " -P " + BMC_PASSWORD + " -H " + BMC_IP + " power on")
def power_off():
    os.system(IPMITOOL_PATH+" -I lanplus" + " -U " + BMC_USERNAME + " -P " + BMC_PASSWORD + " -H " + BMC_IP + " power off")
# bmc重启服务器检测功能函数
def power_monitor():
    while True:
        time.sleep(10)
        flag_value = host_sock()
        if flag_value == 0:
            print("reboot success! port 22 is open! ")
            break
        else:
            print("The device is restarting...")



# 邮件通知功能
def mail_note():
    # 定义邮件参数内容
    msg = '测试已经over,请注意查看'   # 邮件正文f
    title = '《测试报告》'    # 邮件标题
    receivers = ['admin@qq.com']   # 邮件接收者
    attachment = [r"C:\Users\readme.md"]    # 附件仅支持zip/pdf/xlsx/docx后缀文件

    # 通过邮件发送最新的报告
    Mail().sendmail(receivers, title, msg, attachment)
