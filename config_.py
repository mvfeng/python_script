# 全部的配置文件

# BMC配置
BMC_IP = "172.17.00.000"
BMC_PORT = 22
BMC_USERNAME = "Admin"
BMC_PASSWORD = "Admin"

# ipmitool路径配置
IPMITOOL_PATH = "/usr/bin/ipmitool"  # linux服务器
# IPMITOOL_PATH = "ipmitool"  # windows服务器(安装ipmitool的路径)



# SSH配置
HOST_IP = "172.17.00.000"
HOST_PORT = 22
HOST_USERNAME = "root"
HOST_PASSWORD = "1234"

# UART配置
# UART_PORT = "/dev/ttyACM0"
UART_PORT = "COM13"
UART_BAUDRATE = 115200
UART_TIMEOUT = 2

# 其他配置(暂未使用到)
BAR2_BASE = 0x00000000
SW_MEM_READ = "mr"
SW_MEM_WRITE = "mw"

HOST_MEM_READ = "./main r"
HOST_MEM_WRITE = "./main w"

REG_TEST_PASS = 10
