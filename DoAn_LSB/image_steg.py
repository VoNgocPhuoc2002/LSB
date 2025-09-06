# image_steg.py
from PIL import Image
import numpy as np

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_string):
    message = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        message += chr(int(byte, 2))
    return message

def embed_message_in_image(cover_image_path, secret_message, stego_image_path):
    try:
        img = Image.open(cover_image_path, 'r')
        width, height = img.size
        img_array = np.array(list(img.getdata()))
        
        if img.mode != 'RGB':
            return "Lỗi: Chỉ hỗ trợ ảnh định dạng RGB."
        n = 3
        total_pixels = img_array.size // n

        secret_message += "#####"  # Dấu hiệu kết thúc
        binary_message = message_to_binary(secret_message)
        
        if len(binary_message) > total_pixels * 3:
            return "Lỗi: Thông điệp quá dài để giấu trong ảnh."

        pixel_index = 0
        for i in range(total_pixels):
            for j in range(0, 3):
                if pixel_index < len(binary_message):
                    img_array[i][j] = int(bin(img_array[i][j])[2:].zfill(8)[:-1] + binary_message[pixel_index], 2)
                    pixel_index += 1
        
        img_array = img_array.reshape((height, width, n))
        stego_image = Image.fromarray(img_array.astype('uint8'), img.mode)
        stego_image.save(stego_image_path)
        return "Nhúng tin vào ảnh thành công!"
    except Exception as e:
        return f"Lỗi khi nhúng tin vào ảnh: {e}"

def extract_message_from_image(stego_image_path):
    try:
        img = Image.open(stego_image_path, 'r')
        img_array = np.array(list(img.getdata()))
        
        if img.mode != 'RGB':
            return "Lỗi: Chỉ hỗ trợ ảnh định dạng RGB."
        n = 3
        total_pixels = img_array.size // n

        binary_data = ""
        for i in range(total_pixels):
            for j in range(0, 3):
                binary_data += bin(img_array[i][j])[2:].zfill(8)[-1]

        delimiter = message_to_binary("#####")
        delimiter_index = binary_data.find(delimiter)
        
        if delimiter_index != -1:
            secret_binary = binary_data[:delimiter_index]
            return binary_to_message(secret_binary)
        else:
            return "Không tìm thấy thông điệp ẩn trong ảnh."
    except Exception as e:
        return f"Lỗi khi trích xuất tin từ ảnh: {e}"