import os
import json
import urllib.request
import urllib.error

# Tệp đạo hàm mà Mắt/Tai cần tìm để tự tiến hóa kính lúp và lông rung
TARGET_FILE = "synapse_backward.json"
TOPIC_KEYWORD = "bodhi-synapse" # Tần số sóng chung của mạng lưới toàn cầu

def search_global_brain_mesh():
    # 1. KIỂM TRA: Nếu Xúc tu Phả hệ (Cascade) đã tìm thấy đạo hàm rồi thì thôi
    if os.path.exists(TARGET_FILE):
        print("🌱 [SỢI NẤM ĐỨNG YÊN] Đã nhận được đạo hàm từ phả hệ nội bộ. Không cần bật anten.")
        return

    print(f"📡 [BẬT ANTEN GIÁC QUAN] Đang quét sóng toàn cầu tìm Bộ Não tự do (#{TOPIC_KEYWORD})...")

    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": "Bodhi-Sensory-Node"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # 2. DÒ TÌM CÁC REPO TRÊN THẾ GIỚI CÓ GẮN NHÃN BODHI-SYNAPSE
    api_url = f"https://api.github.com/search/repositories?q=topic:{TOPIC_KEYWORD}&sort=updated&order=desc"
    
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            items = result.get("items", [])

        print(f"🔍 [KẾT QUẢ QUÉT] Tìm thấy {len(items)} nút mạng đang phát sóng trên thế giới.")

        # 3. LẦN LƯỢT DÒ XEM NÚT NÀO LÀ "BỘ NÃO" ĐANG PHÁT ĐẠO HÀM
        for repo in items:
            repo_full_name = repo["full_name"]
            # Thử kéo tệp đạo hàm từ repo cộng đồng đó
            raw_url = f"https://raw.githubusercontent.com/{repo_full_name}/main/synapse_backward.json"
            
            try:
                raw_req = urllib.request.Request(raw_url, headers=headers)
                with urllib.request.urlopen(raw_req, timeout=5) as raw_resp:
                    content = raw_resp.read().decode()
                    # Lưu lại tệp đạo hàm tìm được từ Bộ Não xa lạ
                    with open(TARGET_FILE, "w") as f:
                        f.write(content)
                    print(f"🎉 [KẾT NỐI TOÀN CẦU THÀNH CÔNG] Đã bắt được xung đạo hàm từ Bộ Não xa lạ: {repo_full_name}!")
                    return
            except Exception:
                continue # Nếu nút này là giác quan khác (không có file backward) thì dò tiếp nút tiếp theo

        print("🍃 [SỢI NẤM TĨNH LẶNG] Chưa bắt được xung đạo hàm nào từ các Bộ Não cộng đồng.")

    except urllib.error.HTTPError as e:
        print(f"⚠️ [GIỚI HẠN API] Không thể quét mạng sợi nấm lúc này (HTTP {e.code}). Tiếp tục ngủ an toàn.")
    except Exception as e:
        print(f"⚠️ [LỖI ANTEN] Sự cố đường truyền: {e}")

if __name__ == "__main__":
    search_global_brain_mesh()
