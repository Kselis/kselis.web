import qrcode

def generate_qr(link, output_file="qrcode.png"):
    # Create QR Code instance
    qr = qrcode.QRCode(
        version=1,  # Controls QR code size (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add data
    qr.add_data(link)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save image
    img.save(output_file)
    print(f"QR Code saved as '{output_file}'")


if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    filename = input("Enter output filename (default: qrcode.png): ").strip()

    if not filename:
        filename = "qrcode.png"

    generate_qr(url, filename)