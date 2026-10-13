import json
import os

RAW_SIGNAL = "synapse_backward.json"
VERIFIED_SIGNAL = "verified_backward.json"

def verify_and_purify():
    if not os.path.exists(RAW_SIGNAL):
        return False

    try:
        with open(RAW_SIGNAL, "r") as f:
            data = json.load(f)

        grads = data.get("gradients_for_eye", [])
        if not isinstance(grads, list) or len(grads) < 2:
            print(f"⛔ [HỆ MIỄN DỊCH CHẶN] Xung đạo hàm sai cấu trúc: {data}")
            return False

        # Kháng độc tố: Giới hạn đạo hàm trong khoảng an toàn [-5.0, 5.0] chống nổ gradient
        clean_grads = [max(-5.0, min(5.0, float(g))) for g in grads[:2]]
        
        purified_packet = {
            "reply_to_timestamp": data.get("reply_to_timestamp", 0),
            "gradients_for_eye": clean_grads
        }

        with open(VERIFIED_SIGNAL, "w") as f:
            json.dump(purified_packet, f, indent=4)

        print(f"🛡️ [LỌC ĐẠO HÀM THÀNH CÔNG] Đạo hàm tinh khiết: {clean_grads}")
        return True
    except Exception as e:
        print(f"⚠️ [ĐỘC TỐ] Tệp đạo hàm bị hỏng: {e}")
        return False

if __name__ == "__main__":
    verify_and_purify()
