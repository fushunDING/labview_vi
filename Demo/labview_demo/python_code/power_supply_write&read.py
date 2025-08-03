import pyvisa
import time 

def set_it6332a(visa_address, voltage, current, channel=1):
    try:
        rm = pyvisa.ResourceManager()
        power = rm.open_resource(visa_address)

        power.write('*RST')
        power.write(f'INST:NSEL {channel}')
        power.write(f'VOLT {voltage}')
        power.write(f'CURR {current}')
        power.write('OUTP ON')
        time.sleep(1)

        v_out = float(power.query('MEAS:VOLT?').strip())
        i_out = float(power.query('MEAS:CURR?').strip())

        power.close()
        rm.close()

        # 返回一个元组，让 LabVIEW 显示为簇
        return (str(visa_address), int(channel), v_out, i_out)

    except Exception as e:
        # 返回错误时也返回固定格式的元组
        return (f"Python error: {str(e)}", -1, -1.0, -1.0)
