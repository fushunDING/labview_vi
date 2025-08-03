import pyvisa

def set_it6332a(visa_address, voltage, current, channel=1):
    rm = pyvisa.ResourceManager()
    power = rm.open_resource(visa_address)

    power.write(f'INST:NSEL {channel}')
    power.write(f'VOLT {voltage}')
    power.write(f'CURR {current}')
    power.write('OUTP ON')

    v_out = power.query('MEAS:VOLT?').strip()
    i_out = power.query('MEAS:CURR?').strip()

    power.close()
    rm.close()

    return f"Channel {channel}: Voltage set to {v_out} V, Current set to {i_out} A"

if __name__ == '__main__':
    visa_addr = 'USB0::0xFFFF::0x6300::802071092796770281::INSTR'  # 用你识别到的地址
    result = set_it6332a(visa_addr, 12, 1.5)  # 设置12V，1.5A
    print(result)


