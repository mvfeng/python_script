# Data:20220530
# Descript:最新版适用所有用到ssh/uart的自动化任务
# Version:1.5
# 配置文件入口
import logging
LOG_LEVEL = logging.INFO
LOG_DIR = "./"
LOG_FORMAT = '%(asctime)s %(message)s'

# BMC配置 !!!提前确认下自己BMC密码是正确的 # ipmitool user list 1
BMC_IP = "172.17.1.2"
BMC_PORT = 22
BMC_USERNAME = "admin"
BMC_PASSWORD = "admin"

# ipmitool路径配置
# IPMITOOL_PATH = "/usr/bin/ipmitool"  # linux服务器
IPMITOOL_PATH = "ipmitool"         # windows服务器(安装ipmitool的路径) #此处我演示的是加入全局变量后的

# SSH配置
HOST_IP = "172.17.1.1"
HOST_PORT = 22
HOST_USERNAME = "root"
HOST_PASSWORD = "root123"

# UART配置
# UART_PORT = "/dev/ttyACM0"   # linux服务器
UART_PORT = "COM3"            # windows服务器
UART_BAUDRATE = 115200
UART_TIMEOUT = 0.01
#  0.1 0.2 1 2 可调整

# 其他配置(暂未使用到)
BAR2_BASE = 0x55550000
SW_MEM_READ = "mr"
SW_MEM_WRITE = "mw"

HOST_MEM_READ = "./main r"
HOST_MEM_WRITE = "./main w"

REG_TEST_PASS = 10