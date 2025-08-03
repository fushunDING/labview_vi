def set_it6332a(visa_address, voltage, current, channel=1):
    return f"模拟设置通道 {channel}：{voltage}V / {current}A"

if __name__ == "__main__":
    visa_addr = "USB0::0xFFFF::0x6300::802071092796770281::INSTR"
    voltage = 12.0
    current = 1.5
    print(set_it6332a(visa_addr, voltage, current))  # 第四个参数不写，默认是 1




