import cv2
import numpy as np

def to_binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return ''.join([format(i, '08b') for i in data])
    elif isinstance(data, int) or isinstance(data, np.integer):
        return format(data, '08b')
    else:
        raise TypeError(f"Input type not supported: {type(data)}")

def encode_image(image_path, data, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or format not supported")

    message_len = len(data)
    binary_len = format(message_len, '032b')  # First 32 bits store length
    binary_message = binary_len + to_binary(data)

    data_index = 0
    total_bits = len(binary_message)

    for values in image:
        for pixel in values:
            for n in range(3):  # RGB channels
                if data_index < total_bits:
                    pixel[n] = int(to_binary(pixel[n])[:-1] + binary_message[data_index], 2)
                    data_index += 1
                else:
                    break

    if data_index < total_bits:
        raise ValueError("Message too large to hide in this image.")

    cv2.imwrite(output_path, image)
    print(f"Message encoded and saved as {output_path}")

def decode_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or format not supported")

    binary_data = ""
    stop_after = None

    for values in image:
        for pixel in values:
            for n in range(3):  # R, G, B
                binary_data += to_binary(pixel[n])[-1]

                if stop_after is None and len(binary_data) == 32:
                    # First 32 bits = message length in bytes
                    message_len = int(binary_data, 2)
                    stop_after = 32 + (message_len * 8)

                if stop_after and len(binary_data) >= stop_after:
                    break
            if stop_after and len(binary_data) >= stop_after:
                break
        if stop_after and len(binary_data) >= stop_after:
            break

    if stop_after is None:
        raise ValueError("No message length found in image.")

    binary_message = binary_data[32:stop_after]
    data = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return bytes([int(b, 2) for b in data])
