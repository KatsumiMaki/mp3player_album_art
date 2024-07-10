import os
import random
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC


def embed_album_art(mp3_path, image_path):
    audio = MP3(mp3_path, ID3=ID3)

    if audio.tags is None:
        audio.add_tags()

    # Remove existing album art
    tags_to_remove = [tag for tag in audio.tags.keys() if tag.startswith('APIC:')]
    for tag in tags_to_remove:
        del (audio.tags[tag])

    # Add new album art
    with open(image_path, 'rb') as img_file:
        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=img_file.read()
            )
        )
    audio.save()
    print(f"Added album art to {os.path.basename(mp3_path)}")


def load_used_art_list(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_used_art_list(file_path, used_art_list):
    with open(file_path, 'w') as file:
        json.dump(used_art_list, file)


def get_available_art_list(image_folder, used_art_list):
    all_images = [img for img in os.listdir(image_folder) if img.endswith(('.jpg', '.jpeg', '.png'))]
    available_images = [img for img in all_images if img not in used_art_list]

    if not available_images:
        print("All images have been used. Resetting the used art list.")
        used_art_list = []
        available_images = all_images

    return available_images, used_art_list


def add_album_art(mp3_folder, image_folder, used_art_file='used_art_list.json'):
    used_art_list = load_used_art_list(used_art_file)
    available_images, used_art_list = get_available_art_list(image_folder, used_art_list)
    random.shuffle(available_images)

    for idx, filename in enumerate(os.listdir(mp3_folder)):
        if filename.endswith('.mp3'):
            mp3_path = os.path.join(mp3_folder, filename)
            image_path = os.path.join(image_folder, available_images[idx % len(available_images)])
            embed_album_art(mp3_path, image_path)
            used_art_list.append(os.path.basename(image_path))

    save_used_art_list(used_art_file, used_art_list)
    print("List of used album arts has been saved.")
