import json
import random

# ==========================================================
# MẮT DIỀU HÂU: TỰ ĐIỀU CHỈNH KÍNH LÚP KHI NHẬN ĐẠO HÀM TỪ NÃO
# ==========================================================
class AdaptiveRetina:
    def __init__(self):
        # 2 bộ lọc kính lúp 2x2 khởi tạo ngẫu nhiên
        random.seed(10)
        self.k1 = [[random.uniform(-0.5, 0.5) for _ in range(2)] for _ in range(2)]
        self.k2 = [[random.uniform(-0.5, 0.5) for _ in range(2)] for _ in range(2)]

    # CHIỀU XUÔI: Quét ảnh -> Xuất tín hiệu
    def forward(self, img):
        self.last_img = img # Lưu lại vết ảnh để phục vụ đạo hàm
        
        # Quét kính lúp trên góc ảnh 2x2
        f1 = sum(img[r][c] * self.k1[r][c] for r in range(2) for c in range(2))
        f2 = sum(img[r][c] * self.k2[r][c] for r in range(2) for c in range(2))
        
        self.features = [max(0.0, f1), max(0.0, f2)] # Hàm ReLU
        
        # Gói tín hiệu bắn sang Não
        with open("synapse_forward.json", "w") as f:
            json.dump({"features": self.features}, f, indent=4)
        print(f"👁️ [MẮT] Đã quét ảnh -> Bắn tín hiệu sang Não: {self.features}")
        return self.features

    # CHIỀU NGƯỢC (ĐỘT PHÁ): Nhận đạo hàm từ Não để tự vặn lại kính lúp!
    def backward(self, lr=0.1):
        print("📥 [MẮT] Đang đón nhận xung đạo hàm từ Não...")
        with open("synapse_backward.json", "r") as f:
            data = json.load(f)
            grads = data["gradients_for_eye"] # [grad_f1, grad_f2]

        print(f"⚡ [MẮT] Nhận đạo hàm từ Não: {grads}")

        # Vặn lại bộ lọc Kính lúp K1 theo đạo hàm từ Não gửi về
        if self.features[0] > 0: # Đạo hàm của ReLU
            for r in range(2):
                for c in range(2):
                    self.k1[r][c] += lr * grads[0] * self.last_img[r][c]

        # Vặn lại bộ lọc Kính lúp K2
        if self.features[1] > 0:
            for r in range(2):
                for c in range(2):
                    self.k2[r][c] += lr * grads[1] * self.last_img[r][c]

        print("🔧 [MẮT] ĐÃ TỰ ĐIỀU CHỈNH XONG CÁC GÓC KÍNH LÚP CNN!")
        print(f"   Kính lúp K1 mới: {self.k1}")

if __name__ == "__main__":
    retina = AdaptiveRetina()
    
    # Bức ảnh thực tế đưa vào mắt (Vạch sáng)
    anh_mau = [
        [1.0, 1.0],
        [0.0, 0.0]
    ]
    
    # 1. Chiều đi: Mắt nhìn ảnh -> xuất tín hiệu forward
    retina.forward(anh_mau)
    
    # (Tại đây, Bộ Não sẽ chạy và bắn ngược lại synapse_backward.json)
    # Giả lập xung đạo hàm do Não gửi về để kiểm tra Mắt:
    with open("synapse_backward.json", "w") as f:
        json.dump({"gradients_for_eye": [0.45, -0.12]}, f)

    # 2. Chiều về: Mắt đọc đạo hàm của Não và tự tiến hóa!
    retina.backward(lr=0.1)
