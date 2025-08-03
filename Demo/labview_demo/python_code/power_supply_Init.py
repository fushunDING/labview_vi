import pyvisa

def initialize_all_channels(visa_address, channels):
    rm = pyvisa.ResourceManager()
    power = rm.open_resource(visa_address)

    for ch in channels:
        power.write(f'INST:NSEL {ch}')
        power.write('VOLT 0')
        power.write('CURR 0')
        power.write('OUTP OFF')
        print(f"Channel {ch} initialized: Voltage=0V, Current=0A, Output OFF")

    power.close()
    rm.close()

if __name__ == '__main__':
    visa_addr = 'USB0::0xFFFF::0x6300::802071092796770281::INSTR'  # 你的设备地址
    channels = [1, 2, 3, 4]  # 根据你电源通道数量修改
    initialize_all_channels(visa_addr, channels)


