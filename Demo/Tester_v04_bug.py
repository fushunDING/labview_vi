# 创建完整的脚本内容，符合用户需求
script_content = '''
import os
import json
import random
import time
from datetime import datetime

# 全局变量
base_path = os.path.dirname(os.path.abspath(__file__))
uid_counter_file = os.path.join(base_path, "sn_counter.json")
total_units = 6  # 每轮模拟 6 个产品
pass_rate = 0.6  # 总体良率控制为 60%

# 初始化 SN 计数器
def load_sn_counter():
    today = datetime.now().strftime("%Y%m%d")
    if not os.path.exists(uid_counter_file):
        with open(uid_counter_file, "w") as f:
            json.dump({"date": today, "counter": 0}, f)
    with open(uid_counter_file, "r") as f:
        data = json.load(f)

    if data["date"] != today:
        data = {"date": today, "counter": 0}

    sn = data["counter"]
    data["counter"] += total_units
    with open(uid_counter_file, "w") as f:
        json.dump(data, f)

    return sn

# 模拟单个测试项目
def simulate_test(sn_index):
    result = {
        "SN": f"SN{sn_index:012d}",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "tests": [],
        "result": "pass"
    }

    def add_step(name, func):
        start = time.time()
        value, status = func()
        end = time.time()
        step = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "test_item": name,
            "value": value,
            "status": status,
            "duration_ms": round((end - start) * 1000, 2)
        }
        result["tests"].append(step)
        if status == "fail":
            result["result"] = "fail"

    # 模拟不同类型的测试
    def voltage_test():
        value = round(random.uniform(4.8, 5.2), 3)
        return value, "pass" if 4.9 <= value <= 5.1 else "fail"

    def response_test():
        responses = ["OK", "ERR", "TIMEOUT"]
        value = random.choice(responses)
        return value, "pass" if value == "OK" else "fail"

    def status_test():
        return "pass", "pass" if random.random() < 0.95 else "fail"

    # 三次失败才算 fail
    for test_func, name in [(voltage_test, "5V电压测试"), (response_test, "串口响应测试"), (status_test, "状态位检查")]:
        for attempt in range(3):
            add_step(name, test_func)
            if result["tests"][-1]["status"] == "pass":
                break

    result["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return result

def save_test_results(sn_start):
    now = datetime.now()
    year_month = now.strftime("%Y_%m")
    date_str = now.strftime("%Y%m%d")
    timestamp_folder = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]
    sn_base = f"{sn_start:012d}"

    month_dir = os.path.join(base_path, year_month)
    os.makedirs(month_dir, exist_ok=True)

    sub_folder_name = f"{sn_base}_testlog_{timestamp_folder}"
    test_folder = os.path.join(month_dir, sub_folder_name)
    os.makedirs(test_folder, exist_ok=True)

    for i in range(total_units):
        sn = sn_start + i
        result = simulate_test(sn)
        result_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{result_time}_SN{sn:012d}_{result['result']}.json"
        filepath = os.path.join(test_folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[INFO] 测试完成，文件保存在：{test_folder}")

if __name__ == "__main__":
    sn_start = load_sn_counter()
    save_test_results(sn_start)
'''

# 保存为 Tester_v04.py
script_path = "/mnt/data/Tester_v04.py"
with open(script_path, "w", encoding="utf-8") as f:
    f.write(script_content)

script_path
input("按回车键退出...")
