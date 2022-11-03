import time
import paramiko  # SSH使用必要的模块
import socket    # 端口检测必要的模块
import serial    # UART使用必要模块
import os        # 调用系统模块
import config_

# ssh配置
HOST_IP = config_.HOST_IP
HOST_PORT = config_.HOST_PORT
HOST_USERNAME = config_.HOST_USERNAME
HOST_PASSWORD = config_.HOST_PASSWORD
# 端口检测配置
HOST_SOCK_IP = config_.HOST_IP
HOST_SOCK_PORT = config_.HOST_PORT
# bmc配置
BMC_IP = config_.BMC_IP
BMC_USERNAME = config_.BMC_USERNAME
BMC_PASSWORD = config_.BMC_PASSWORD
# ipmitool配置
IPMITOOL_PATH = config_.IPMITOOL_PATH
# uart配置
UART_PORT=config_.UART_PORT
UART_BAUDRATE=config_.UART_BAUDRATE
UART_TIMEOUT=config_.UART_TIMEOUT

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


# 端口检测功能函数
def host_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((HOST_SOCK_IP, HOST_SOCK_PORT))  # 判断22端口是否开启（方便判断是否进入OS以及是否ssh连接）
    if 0 == result:
        print("Port 22 is open!")
    else:
        print("Port 22 is not open，return code：%s" % result)
    return result  # 状态码0表端口开启，否则未开启

# bmc上下电服务器功能函数（有待考量是否上下电和直接reboot的区别？？？）
def power_on():
    os.system(IPMITOOL_PATH+" -I lan" + " -U " + BMC_USERNAME + " -P " + BMC_PASSWORD + " -H " + BMC_IP + " power on")
def power_off():
    os.system(IPMITOOL_PATH+" -I lan" + " -U " + BMC_USERNAME + " -P " + BMC_PASSWORD + " -H " + BMC_IP + " power off")
# bmc重启服务器检测功能函数
def reboot():
    while True:
        time.sleep(10)
        flag_value = host_ssh_.host_sock()
        if flag_value == 0:
            print("reboot success! port 22 is open! ")
            break
        else:
            print("The device is restarting...")

# uart串口交互功能函数
def serial_open(port, bps, timeouts):
    serial_obj =serial.Serial(port, bps, timeout=timeouts, rtscts=True, dsrdtr=True)  # 打开串口，并得到串口对象
    return serial_obj

def serial_cmd(cmd):
    serial_obj = serial_open(UART_PORT, UART_BAUDRATE, UART_TIMEOUT)
    # print(serial_obj.is_open)
    serial_obj.write(cmd.encode("utf-8"))  # 写数据
    time.sleep(0.4)
    r_data = serial_obj.readlines()
    rdata = []
    for i in r_data:
        i = i.decode("utf-8", "ignore")
        rdata.append(i[:-1])
    return rdata
