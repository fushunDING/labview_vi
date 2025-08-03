import json
import os
import random
import time
from datetime import datetime

# === 可配置参数 ===
UID_LIST = [f"DUT_{i:03d}" for i in range(1, 7)]  # 模拟 6 个通道
GOOD_YIELD = 0.98  # 模拟良率 98%
MAX_RETRY = 3

# === 获取脚本路径，确保文件总能正确写出 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_PATH = os.path.join(SCRIPT_DIR, "test_results.json")

# === 模拟单个 DUT 的测试 ===
def test_dut(uid):
    test_log = {
        "uid": uid,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": "PASS",
        "items": []
    }

    test_items = [
        {"name": "Voltage Check", "type": "number"},
        {"name": "Communication", "type": "string"},
        {"name": "Indicator Red", "type": "passfail"},
        {"name": "Indicator Green", "type": "passfail"},
        {"name": "Worklight Test", "type": "passfail"},
    ]

    for item in test_items:
        for attempt in range(1, MAX_RETRY + 1):
            start = time.time()
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            result = simulate_result(item["type"])
            duration = round(time.time() - start, 3)

            test_log["items"].append({
                "timestamp": timestamp,
                "test_item": item["name"],
                "result": result,
                "attempt": attempt,
                "duration": duration
            })

            if result != "FAIL":
                break
        else:
            test_log["result"] = "FAIL"  # 三次都失败就整体失败

        if test_log["result"] == "FAIL":
            break  # 不继续往下测了

    test_log["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return test_log

# === 模拟测试项返回结果 ===
def simulate_result(test_type):
    if test_type == "number":
        return round(random.uniform(3.0, 3.6), 3)
    elif test_type == "string":
        return "OK" if random.random() < GOOD_YIELD else "ERROR"
    else:  # passfail 类型
        return "PASS" if random.random() < GOOD_YIELD else "FAIL"

# === 主流程 ===
def main():
    all_results = []

    for uid in UID_LIST:
        result = test_dut(uid)
        all_results.append(result)

    # 输出为 JSON 文件，确保路径正确
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("✅ 模拟测试完成，结果已保存至 test_results.json")

if __name__ == "__main__":
    main()
