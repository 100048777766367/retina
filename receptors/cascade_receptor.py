import os
import subprocess

OWNER = os.environ.get("REPO_OWNER", "")
PARENT = os.environ.get("REPO_PARENT", "")
UPSTREAM_SEED = "100048777766367"

TARGET_FILE = "synapse_backward.json"

def try_fetch(target_owner):
    if not target_owner:
        return False
    url = f"https://raw.githubusercontent.com/{target_owner}/neuron/main/synapse_backward.json"
    print(f"📡 [XÚC TU MẮT] Đang dò tìm xung đạo hàm tại: {target_owner}/neuron...")
    res = subprocess.run(["curl", "-s", "-f", url, "-o", TARGET_FILE], capture_output=True)
    if res.returncode == 0 and os.path.exists(TARGET_FILE):
        print(f"🎯 [HÚT THÀNH CÔNG] Đã nhận được xung đạo hàm từ Bộ Não của {target_owner}!")
        return True
    return False

def main():
    if OWNER and try_fetch(OWNER): return
    if PARENT and try_fetch(PARENT): return
    if try_fetch(UPSTREAM_SEED): return
    print("🍃 [MÔI TRƯỜNG TĨNH] Chưa thấy xung đạo hàm từ bất kỳ nhánh phả hệ nào.")

if __name__ == "__main__":
    main()
