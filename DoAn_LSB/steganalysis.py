# steganalysis.py
from PIL import Image
import numpy as np
import wave
from scipy.stats import chisquare

def analyze_image_lsb(image_path):
    """
    Phân tích ảnh sử dụng phương pháp Pairs of Values (PoV) Chi-Square Attack.
    Đây là phương pháp steganalysis thống kê kinh điển và hiệu quả cho LSB.
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            return "Phân tích chỉ hỗ trợ ảnh RGB."
            
        img_array = np.array(img)
        # Lấy một kênh màu để phân tích, ví dụ kênh Đỏ (Red)
        channel = img_array[:, :, 0].flatten()

        # Xây dựng danh sách tần suất quan sát và kỳ vọng cho các cặp giá trị
        observed = []
        expected = []
        for i in range(0, 256, 2):
            # Tần suất của giá trị 2i
            obs1 = np.count_nonzero(channel == i)
            # Tần suất của giá trị 2i+1
            obs2 = np.count_nonzero(channel == i + 1)
            
            # Chỉ xét các cặp có dữ liệu
            if obs1 + obs2 > 0:
                # Tần suất kỳ vọng cho mỗi giá trị trong cặp là trung bình cộng
                exp = (obs1 + obs2) / 2.0
                if exp > 0:
                    observed.extend([obs1, obs2])
                    expected.extend([exp, exp])
        
        if not observed:
            return "Không đủ dữ liệu để phân tích."
            
        chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
        
        # Ngưỡng quyết định (thông thường là 0.05 hoặc 0.01)
        threshold = 0.05
        
        # Logic đúng: P-value CAO (> threshold) cho thấy tần suất các cặp gần bằng nhau,
        # đây là dấu hiệu của việc nhúng tin LSB.
        if p_value > threshold:
            return (f"Phát hiện khả năng có tin ẩn LSB (Tấn công PoV Chi-Square).\n"
                    f"(P-value = {p_value:.4f} > {threshold}).\n"
                    f"Phân bố tần suất của các cặp pixel liền kề quá cân bằng, đây là dấu hiệu bất thường.")
        else:
            return (f"Không phát hiện dấu hiệu LSB rõ ràng.\n"
                    f"(P-value = {p_value:.4f} <= {threshold}).\n"
                    f"Phân bố tần suất của các cặp pixel có vẻ tự nhiên.")
    except Exception as e:
        return f"Lỗi phân tích ảnh: {e}"

def analyze_audio_lsb(audio_path, chunk_size=4096):
    """
    Phân tích âm thanh LSB bằng cách chia thành các khối (chunks) để tăng độ nhạy.
    Nếu bất kỳ khối nào có dấu hiệu, toàn bộ file bị coi là đáng ngờ.
    """
    try:
        audio = wave.open(audio_path, 'rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        audio.close()

        if len(frame_bytes) == 0:
            return "File âm thanh rỗng."

        num_chunks = len(frame_bytes) // chunk_size
        if num_chunks == 0:
            chunk_size = len(frame_bytes) # Nếu file quá nhỏ, phân tích toàn bộ file
            num_chunks = 1

        # Lặp qua từng khối để phân tích
        for i in range(num_chunks):
            chunk = frame_bytes[i*chunk_size : (i+1)*chunk_size]
            
            lsb_bits = [byte & 1 for byte in chunk]
            count_zeros = lsb_bits.count(0)
            count_ones = lsb_bits.count(1)

            if count_zeros + count_ones == 0:
                continue

            observed = [count_zeros, count_ones]
            expected = [(count_zeros + count_ones) / 2, (count_zeros + count_ones) / 2]
            
            # Bỏ qua khối nếu không có đủ dữ liệu để tránh lỗi chia cho 0
            if expected[0] == 0:
                continue

            chi2_stat, p_value = chisquare(observed, expected)
            
            threshold = 0.1 # Có thể tăng ngưỡng một chút để nhạy hơn
            
            # Nếu tìm thấy một khối đáng ngờ, dừng lại và kết luận ngay
            if p_value > threshold:
                return (f"Phát hiện khả năng có tin ẩn LSB (Phân tích theo khối).\n"
                        f"Khối số {i+1}/{num_chunks} có dấu hiệu bất thường.\n"
                        f"(P-value = {p_value:.4f} > {threshold}).\n"
                        f"Phân bố bit LSB quá cân bằng.")
        
        # Nếu không có khối nào đáng ngờ sau khi kiểm tra hết
        return (f"Không phát hiện dấu hiệu LSB rõ ràng sau khi quét {num_chunks} khối.\n"
                f"Phân bố bit LSB trong các khối có vẻ tự nhiên.")

    except Exception as e:
        return f"Lỗi phân tích âm thanh: {e}"