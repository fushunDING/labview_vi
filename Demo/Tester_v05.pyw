import os
import json
import random
import time
from datetime import datetime

base_path = os.path.dirname(os.path.abspath(__file__))
uid_counter_file = os.path.join(base_path, "sn_counter.json")
total_units = 6
product_pass_rate = 0.6

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

def simulate_test(sn_index):
    result = {
        "SN": f"SN{sn_index:012d}",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "tests": [],
        "result": "pass"
    }
    product_pass = random.random() < product_pass_rate
    if not product_pass:
        result["result"] = "fail"

    test_items = ["5V电压测试", "串口响应测试", "状态位检查"]

    def voltage_test():
        value = round(random.uniform(4.9, 5.1), 3)
        return value, "pass"

    def response_test():
        return "OK", "pass"

    def status_test():
        return "pass", "pass"

    test_funcs = [voltage_test, response_test, status_test]
    fail_index = random.randint(0, len(test_items) - 1) if not product_pass else -1

    for i, (name, func) in enumerate(zip(test_items, test_funcs)):
        start = time.time()
        time.sleep(random.uniform(1, 2))
        value, status = func()
        if i == fail_index:
            status = "fail"
            if name == "5V电压测试":
                value = round(random.choice([4.7, 5.3]), 3)
            elif name == "串口响应测试":
                value = random.choice(["ERR", "TIMEOUT"])
        end = time.time()
        step = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "test_item": name,
            "value": value,
            "status": status,
            "duration_ms": round((end - start) * 1000, 2)
        }
        result["tests"].append(step)

    result["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return result

def save_test_results(sn_start):
    now = datetime.now()
    year_month = now.strftime("%Y_%m")
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
