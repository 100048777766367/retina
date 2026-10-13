import json

# ==================================================
# 1. NƠ-RON MẮT DIỀU HÂU (CONVOLUTIONAL NEURON THUẦN PYTHON)
# ==================================================
class ConvNeuron:
    def __init__(self, filter_weights, bias=0.0):
        # Bộ lọc (Kính lúp): ma trận nhỏ ví dụ 2x2 hoặc 3x3
        self.filter = filter_weights
        self.bias = bias
        self.f_size = len(filter_weights)

    # Thao tác quét kính lúp trên bức ảnh (Phép tích chập - Convolution)
    def scan(self, image):
        img_h = len(image)
        img_w = len(image[0])
        feature_map = []

        # Trượt kính lúp từng bước một (stride = 1)
        for r in range(img_h - self.f_size + 1):
            row_out = []
            for c in range(img_w - self.f_size + 1):
                # Nhân từng điểm ảnh với kính lúp và cộng dồn
                tong = 0.0
                for fr in range(self.f_size):
                    for fc in range(self.f_size):
                        tong += image[r + fr][c + fc] * self.filter[fr][fc]
                tong += self.bias
                # Hàm kích hoạt ReLU (Phép tính thứ 5: Giữ lại điểm sáng nét)
                row_out.append(max(0.0, tong))
            feature_map.append(row_out)
        return feature_map

# Hàm thu gọn (Max Pooling): Lấy giá trị mạnh nhất trong bản đồ quét
def max_pooling(feature_map):
    gia_tri_lon_nhat = 0.0
    for row in feature_map:
        for val in row:
            if val > gia_tri_lon_nhat:
                gia_tri_lon_nhat = val
    return gia_tri_lon_nhat

# ==================================================
# 2. CHẠY THỬ MẮT NHÌN MỘT BỨC ẢNH MA TRẬN (3x3 điểm ảnh)
# ==================================================
if __name__ == "__main__":
    # Giả sử đây là một bức ảnh 3x3 điểm ảnh (0 là tối, 1 là sáng)
    # Bức ảnh này có một "Vạch Ngang" phát sáng ở hàng giữa:
    buc_anh = [
        [0, 0, 0],
        [1, 1, 1],  # Vạch ngang sáng
        [0, 0, 0]
    ]

    # Kính lúp số 1: Chuyên phát hiện VẠCH NGANG
    mat_vach_ngang = ConvNeuron(filter_weights=[
        [ 1,  1],
        [-1, -1]
    ])

    # Kính lúp số 2: Chuyên phát hiện VẠCH ĐỨNG
    mat_vach_dung = ConvNeuron(filter_weights=[
        [ 1, -1],
        [ 1, -1]
    ])

    # Mắt bắt đầu quét bức ảnh
    map_ngang = mat_vach_ngang.scan(buc_anh)
    map_dung = mat_vach_dung.scan(buc_anh)

    # Nén lại thành 2 tín hiệu thần kinh duy nhất
    tin_hieu_1 = max_pooling(map_ngang)
    tin_hieu_2 = max_pooling(map_dung)

    # Chuẩn hóa về thang đo khoảng [0, 1]
    tin_hieu_thi_giac = [round(min(tin_hieu_1, 1.0), 2), round(min(tin_hieu_2, 1.0), 2)]

    print(f"👁️ Mắt Diều Hâu đã quét xong bức ảnh!")
    print(f"📡 Tín hiệu thị giác trích xuất được: {tin_hieu_thi_giac}")

    # Xuất tín hiệu ra tệp JSON để gửi cho Bộ Não
    with open("visual_signal.json", "w") as f:
        json.dump({"signal": tin_hieu_thi_giac}, f, indent=4)
    print("💾 Đã lưu tín hiệu vào visual_signal.json")
