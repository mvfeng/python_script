# 一个串口发送立刻直接输出给另一个串口 (串口自动转发)
import time
import serial  # 导入模块


# BOOL = True  # 读取标志位
# 关闭串口
def DColsePort(Cser):
    # global BOOL
    # BOOL = False
    Cser.close()


# 写数据
def DWritePort(Wser, Wdata):
    Wser.write(Wdata.encode('utf-8'))  # 写数据


# 读数据
def DReadPort(Rser):
    Rdata = Rser.read(Rser.in_waiting).decode("utf-8")
    # print("读出："+Rdata)
    return Rdata


# 串口
def DOpenPort(port, bps, timeout):
    ret = False
    try:
        # 打开串口，并得到串口对象
        Oser = serial.Serial(port, bps, timeout=timeout)
        # 判断是否打开成功
        if (Oser.is_open):
            ret = True
    except Exception as e:
        print("---异常---：", e)
    return Oser


# # 读写独立线程
# def DOpenthread(wrFunction, wrParameter):
#     threading.Thread(target=wrFunction, args=(wrParameter,)).start()
if __name__ == "__main__":
    Rser = DOpenPort("COM10", 115200, None)
    Wser = DOpenPort("COM13", 115200, None)
    # for i in range(0, 100000):
    while True:
        Data = DReadPort(Rser)
        # for i in range(10):
        DWritePort(Wser, Data)
        # time.sleep(0.01)
