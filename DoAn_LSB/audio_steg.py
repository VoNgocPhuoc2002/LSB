# audio_steg.py
import wave

def embed_message_in_audio(cover_audio_path, secret_message, stego_audio_path):
    try:
        audio = wave.open(cover_audio_path, 'rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        secret_message += "#####"  # Dấu hiệu kết thúc
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)

        if len(binary_message) > len(frame_bytes):
            return "Lỗi: Thông điệp quá dài để giấu trong file âm thanh."

        for i in range(len(binary_message)):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_message[i])

        stego_audio = wave.open(stego_audio_path, 'wb')
        stego_audio.setparams(audio.getparams())
        stego_audio.writeframes(bytes(frame_bytes))
        
        audio.close()
        stego_audio.close()
        return "Nhúng tin vào âm thanh thành công!"
    except Exception as e:
        return f"Lỗi khi nhúng tin vào âm thanh: {e}"

def extract_message_from_audio(stego_audio_path):
    try:
        audio = wave.open(stego_audio_path, 'rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        extracted_bits = ""
        for byte in frame_bytes:
            extracted_bits += str(byte & 1)
        
        delimiter = ''.join(format(ord(char), '08b') for char in "#####")
        delimiter_index = extracted_bits.find(delimiter)

        if delimiter_index != -1:
            secret_binary = extracted_bits[:delimiter_index]
            message = ""
            for i in range(0, len(secret_binary), 8):
                byte = secret_binary[i:i+8]
                if len(byte) == 8:
                    message += chr(int(byte, 2))
            return message
        else:
            return "Không tìm thấy thông điệp ẩn trong file âm thanh."
    except Exception as e:
        return f"Lỗi khi trích xuất tin từ âm thanh: {e}"