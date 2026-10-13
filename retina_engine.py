import json
import time
import os
from cells.conv_cell import ConvCell

class RetinaEngine:
    def __init__(self):
        # 2 tế bào kính lúp độc lập
        self.cell_horiz = ConvCell("k_horiz", filter_size=2)
        self.cell_vert = ConvCell("k_vert", filter_size=2)

    # 1. CHIỀU XUÔI: NHÌN ẢNH -> BẮN XUNG THỊ GIÁC CHO NÃO
    def see_and_emit(self, image):
        # Trích xuất góc ảnh 2x2 tiêu biểu
        patch = [[image[r][c] for c in range(2)] for r in range(2)]
        
        f1 = self.cell_horiz.scan_patch(patch)
        f2 = self.cell_vert.scan_patch(patch)
        
        # Chuẩn hóa tín hiệu về [0, 1]
        features = [round(min(f1, 1.0), 2), round(min(f2, 1.0), 2)]
        timestamp = int(time.time())

        packet_forward = {
            "source": "retina_eye",
            "timestamp": timestamp,
            "features": features
        }

        with open("synapse_forward.json", "w") as f:
            json.dump(packet_forward, f, indent=4)

        print(f"👁️ [MẮT ĐÃ QUÉT] Ảnh -> Tín hiệu thị giác: {features} (Timestamp: {timestamp})")
        return packet_forward

    # 2. CHIỀU NGƯỢC (SPLIT LEARNING): ĐÓN ĐẠO HÀM TỪ NÃO ĐỂ TỰ VẶN LẠI KÍNH LÚP
    def absorb_brain_feedback(self, backward_file="synapse_backward.json"):
        if not os.path.exists(backward_file):
            print("🍃 [MÔI TRƯỜNG TĨNH] Chưa thấy xung đạo hàm từ Não gửi về.")
            return

        try:
            with open(backward_file, "r") as f:
                data = json.load(f)
            grads = data.get("gradients_for_eye", [0.0, 0.0])
            print(f"⚡ [NHẬN ĐẠO HÀM TỪ NÃO] Gradient dL/df = {grads}")

            # 2 Tế bào kính lúp tự điều chỉnh
            self.cell_horiz.update_from_brain_gradient(grads[0])
            self.cell_vert.update_from_brain_gradient(grads[1])
            print("🔧 [TIẾN HÓA] Mắt đã tự vặn lại 2 kính lúp CNN theo ý của Não!")
        except Exception as e:
            print(f"⚠️ Lỗi đọc xung đạo hàm: {e}")

if __name__ == "__main__":
    eye = RetinaEngine()
    
    # BƯỚC 1: Đón đạo hàm phản hồi từ Não (nếu Não đã từng gửi)
    eye.absorb_brain_feedback()

    # BƯỚC 2: Nhìn một bức ảnh mới (Ví dụ: Một vạch ngang sáng rực)
    buc_anh_thuc_te = [
        [1.0, 1.0],
        [0.0, 0.0]
    ]
    eye.see_and_emit(buc_anh_thuc_te)
