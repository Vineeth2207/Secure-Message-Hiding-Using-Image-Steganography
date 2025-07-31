import sys
from crypto_utils import encrypt_message, decrypt_message
from stego_image import encode_image, decode_image

def hide_message(image_in, message, password, image_out):
    encrypted_msg = encrypt_message(message.encode(), password)
    encode_image(image_in, encrypted_msg, image_out)

def reveal_message(stego_image, password):
    encrypted_msg = decode_image(stego_image)
    try:
        decrypted_msg = decrypt_message(encrypted_msg, password)
        return decrypted_msg.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def main():
    print("1. Hide message")
    print("2. Reveal message")
    choice = input("Choose option (1 or 2): ")

    if choice == '1':
        img_in = input("Input image path (PNG/BMP recommended): ")
        msg = input("Enter message to hide: ")
        pwd = input("Enter password: ")
        img_out = input("Output stego image path: ")
        hide_message(img_in, msg, pwd, img_out)

    elif choice == '2':
        stego_img = input("Input stego image path: ")
        pwd = input("Enter password: ")
        message = reveal_message(stego_img, pwd)
        print("Hidden message:")
        print(message)

    else:
        print("Invalid option!")

if __name__ == "__main__":
    main()
 