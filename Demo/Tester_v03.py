import os
import time
import json
import random
from datetime import datetime

UID_COUNTER_FILE = os.path.join(os.path.dirname(__file__), "uid_counter.json")

# ---------- 生成 UID ----------
def generate_uid():
    now = datetime.now()
    today_str = now.strftime("%Y%m%d")
    counter = {"last_date": today_str, "last_index": -1}

    if os.path.exists(UID_COUNTER_FILE):
        with open(UID_COUNTER_FILE, "r") as f:
            try:
                counter = json.load(f)
            except:
                pass

    if counter["last_date"] != today_str:
        counter["last_date"] = today_str
        counter["last_index"] = 0
    else:
        counter["last_index"] += 1

    uid = f"{today_str}_{counter['last_index']:04d}"

    with open(UID_COUNTER_FILE, "w") as f:
        json.dump(counter, f)

    return uid

# ---------- 创建测试批次路径 ----------
def create_log_path():
    now = datetime.now()
    month_folder = now.strftime("%Y_%m")
    day_folder = f"0001_testlog_{now.strftime('%Y%m%d')}"
    batch_folder = now.strftime("%Y%m%d_%H%M%S")

    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, month_folder, day_folder, batch_folder)
    os.makedirs(full_path, exist_ok=True)
    return full_path, batch_folder

# ---------- 保存每个 JSON 文件 ----------
def save_log(data, uid, result, batch_folder):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{uid}_TestLog_{batch_folder}_{result}.json"
    full_path, _ = create_log_path()
    file_path = os.path.join(full_path, filename)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ 保存日志：{file_path}")
    return file_path

# ---------- 单项测试步骤 ----------
def perform_test_step(step_name, func):
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = func()
    duration = round(time.time() - start_time, 3)
    return {
        "step": step_name,
        "timestamp": timestamp,
        "result": result,
        "duration_sec": duration
    }

# ---------- 模拟测试内容 ----------
def simulate_voltage(): return round(random.uniform(2.8, 3.3), 3)
def simulate_comm(): return random.choice(["OK", "READY", "WAIT", "BUSY"])
def simulate_pass(): return "PASS" if random.random() < 0.98 else "FAIL"

def simulate_pass_with_retry():
    for i in range(3):
        result = simulate_pass()
        if result == "PASS":
            return result
        time.sleep(0.2)
    return "FAIL"

# ---------- 单个 DUT 测试流程 ----------
def run_test_for_uid(uid):
    print(f"\n🚀 测试开始：{uid}")
    test_result = {
        "uid": uid,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": [],
        "final_result": "PASS"
    }

    test_result["steps"].append(perform_test_step("初始化", lambda: "OK"))

    steps = [
        ("电压检测", simulate_voltage),
        ("通信测试", simulate_comm),
        ("功能确认", simulate_pass_with_retry)
    ]

    for step_name, func in steps:
        step_result = perform_test_step(step_name, func)
        test_result["steps"].append(step_result)
        if step_result["result"] == "FAIL":
            test_result["final_result"] = "FAIL"
            test_result["steps"].append(perform_test_step("异常收尾", lambda: "Reset"))
            break

    if test_result["final_result"] == "PASS":
        test_result["steps"].append(perform_test_step("正常收尾", lambda: "Done"))

    test_result["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return test_result

# ---------- 主函数 ----------
def main():
    num_devices = 6
    _, batch_folder = create_log_path()

    for _ in range(num_devices):
        uid = generate_uid()
        data = run_test_for_uid(uid)
        result = data["final_result"]
        save_log(data, uid, result, batch_folder)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
