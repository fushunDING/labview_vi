import random
import time
from datetime import datetime
import json
import sys

# -----------------------------
# 配置项（可修改以适配更多测试）
# -----------------------------
UID_LIST = [f"UID_{i:04d}" for i in range(1, 7)]  # 模拟6个产品
PASS_RATE = 0.98  # 总良率98%
MAX_RETRIES = 3


# -----------------------------
# 模拟测试项定义
# -----------------------------
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def simulate_numeric_test(name, min_val, max_val, low_limit, high_limit):
    for attempt in range(1, MAX_RETRIES + 1):
        start = time.time()
        value = round(random.uniform(min_val, max_val), 2)
        result = "PASS" if low_limit <= value <= high_limit else "FAIL"
        duration = round(time.time() - start, 3)
        yield {
            "timestamp": get_timestamp(),
            "name": name,
            "value": value,
            "result": result,
            "attempts": attempt,
            "duration_s": duration,
        }
        if result == "PASS":
            break


def simulate_string_test(name, expected_responses):
    for attempt in range(1, MAX_RETRIES + 1):
        start = time.time()
        value = random.choice(expected_responses + ["ERROR", "TIMEOUT"])
        result = "PASS" if value in expected_responses else "FAIL"
        duration = round(time.time() - start, 3)
        yield {
            "timestamp": get_timestamp(),
            "name": name,
            "value": value,
            "result": result,
            "attempts": attempt,
            "duration_s": duration,
        }
        if result == "PASS":
            break


def simulate_passfail_test(name):
    for attempt in range(1, MAX_RETRIES + 1):
        start = time.time()
        result = "PASS" if random.random() < PASS_RATE else "FAIL"
        duration = round(time.time() - start, 3)
        yield {
            "timestamp": get_timestamp(),
            "name": name,
            "value": result,
            "result": result,
            "attempts": attempt,
            "duration_s": duration,
        }
        if result == "PASS":
            break


# -----------------------------
# 单个产品的测试流程
# -----------------------------
def test_single_uid(uid):
    print(f"[{get_timestamp()}] 🔧 开始测试：{uid}")
    log = {
        "uid": uid,
        "start_time": get_timestamp(),
        "tests": [],
        "final_result": "PASS",
    }

    try:
        # 初始化（模拟时间）
        time.sleep(random.uniform(0.05, 0.15))

        # 测试项列表
        tests = [
            simulate_numeric_test("VCC Voltage", 4.5, 5.5, 4.7, 5.3),
            simulate_passfail_test("LED Red Light"),
            simulate_passfail_test("LED Green Light"),
            simulate_string_test("MCU Handshake", ["OK", "READY"]),
            simulate_numeric_test("WorkLight Current", 90, 110, 95, 105),
            simulate_passfail_test("Switch A Press"),
            simulate_passfail_test("Switch B Press"),
        ]

        for test_func in tests:
            for result in test_func:
                log["tests"].append(result)
                if result["result"] == "FAIL" and result["attempts"] >= MAX_RETRIES:
                    log["final_result"] = "FAIL"
                    raise Exception(f"测试项 {result['name']} 重试失败")

        log["end_time"] = get_timestamp()
        print(f"[{get_timestamp()}] ✅ 完成测试：{uid} ✅ 结果：{log['final_result']}")

    except Exception as e:
        log["end_time"] = get_timestamp()
        print(f"[{get_timestamp()}] ❌ 测试失败：{uid}，原因：{str(e)}")

    return log


# -----------------------------
# 主流程
# -----------------------------
def main():
    all_logs = []
    for uid in UID_LIST:
        log = test_single_uid(uid)
        all_logs.append(log)

    # 输出 JSON 格式的测试结果
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(all_logs, f, indent=4, ensure_ascii=False)

    print(f"\n[{get_timestamp()}] 📝 所有测试完成，结果保存在 test_results.json")


if __name__ == "__main__":
    main()
