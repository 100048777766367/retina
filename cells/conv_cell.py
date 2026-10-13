import random
import json
import os

class ConvCell:
    def __init__(self, cell_id, filter_size=2, storage_dir="synapses"):
        self.id = cell_id
        self.f_size = filter_size
        self.storage_path = os.path.join(storage_dir, f"{self.id}.json")
        self.os_dir = storage_dir
        
        self.kernel = []
        self.last_patch = []
        self.last_activation = 0.0
        
        # Tự nạp túi nhớ hoặc tự khởi sinh
        self.load_self()

    def load_self(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                if len(data.get("k", [])) == self.f_size:
                    self.kernel = data["k"]
                    return
            except Exception:
                pass

        # TỰ KHỞI SINH (SELF-BOOTSTRAP): Tạo kính lúp ngẫu nhiên
        self.kernel = [[random.uniform(-0.5, 0.5) for _ in range(self.f_size)] for _ in range(self.f_size)]
        self.save_self()

    def scan_patch(self, patch):
        self.last_patch = patch
        # Tích chập cục bộ: sum(patch * kernel)
        tong = sum(patch[r][c] * self.kernel[r][c] for r in range(self.f_size) for c in range(self.f_size))
        # Phép tính thứ 5: ReLU giữ lại điểm sáng
        self.last_activation = max(0.0, tong)
        return self.last_activation

    def update_from_brain_gradient(self, grad, lr=0.1):
        # Đạo hàm của ReLU: Nếu kích hoạt > 0 thì cho đạo hàm đi qua
        if self.last_activation > 0:
            for r in range(self.f_size):
                for c in range(self.f_size):
                    self.kernel[r][c] += lr * grad * self.last_patch[r][c]
            self.save_self()

    def save_self(self):
        os.makedirs(self.os_dir, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"k": self.kernel}, f, indent=4)
