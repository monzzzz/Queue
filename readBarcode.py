from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode_from_image(image_path):
    """
    Opens an image, decodes any barcodes in it, and prints the barcode data.
    Returns the first barcode data if found, otherwise returns None.
    """
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
    except Exception as e:
        print("Error opening image:", e)
        return None

    # Decode barcodes from the image
    barcodes = decode(img)
    if not barcodes:
        print("No barcode detected in the image.")
        return None

    # Loop through all detected barcodes and print their data and type
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Detected barcode: {barcode_data} (Type: {barcode_type})")

    # Return the first barcode's data
    return barcodes[0].data.decode('utf-8')

