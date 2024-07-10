import os
from PIL import Image

def preprocess_images(image_folder, thumbnail_folder):
    square_images = []
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        try:
            with Image.open(img_path) as img:
                if img.width == img.height:
                    square_images.append(img_name)
                    img.thumbnail((300, 300))
                    img.save(os.path.join(thumbnail_folder, img_name))
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    return square_images
