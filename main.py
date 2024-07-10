import os
import json
from pathlib import Path
from preprocess_images import preprocess_images
from preprocess_audio import preprocess_audio
from add_album_art import add_album_art

CONFIG_FILE = "config.json"
USED_ART_FILE = "used_art_list.json"


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def prompt_directory(prompt_text, default_value):
    user_input = input(f"{prompt_text} (default: \"{default_value}\"): ").strip()
    if user_input.lower() == "default":
        return "default"
    elif user_input.lower() == "no":
        return "no"
    elif user_input.lower() == "mp3player":
        return "mp3player"
    else:
        return os.path.abspath(user_input) if user_input else default_value


def verify_directory(path, types):
    if not os.path.isdir(path):
        if verbose:
            print(f"Directory {path} does not exist.")
        return False
    valid_files = any(file.suffix.lower() in types for file in Path(path).rglob('*'))
    if not valid_files:
        if verbose:
            print(f"No valid files found in {path}.")
        return False
    return True


def reset_default_paths(config):
    config["image_folder"] = "./images"
    config["music_folder"] = "./music"
    config["thumbnail_folder"] = None


def run_default_workflow():
    image_folder = "./images"
    thumbnail_folder = os.path.join(image_folder, "thumbnails")
    os.makedirs(thumbnail_folder, exist_ok=True)
    preprocess_images(image_folder, thumbnail_folder)
    music_folder = "./music"
    preprocess_audio(music_folder, output_format='mp3', bitrate='96k')
    add_album_art(music_folder, thumbnail_folder, USED_ART_FILE)
    print("Default workflow completed.")


def main():
    global verbose
    verbose = input("Enable verbose mode? (default: no): ").strip().lower() == "yes"

    config = load_json(CONFIG_FILE)
    if not config:
        reset_default_paths(config)

    if config.get("image_folder") != "./images" or config.get("music_folder") != "./music":
        reset_defaults = input("Do you want to reset to default directories? (default: no): ").strip().lower() == 'yes'
        if reset_defaults:
            reset_default_paths(config)
            save_json(config, CONFIG_FILE)

    # Step 1: Image Directory
    image_folder = prompt_directory("Enter the full path to the image directory or write 'default' to reset or 'no' to skip", config.get("image_folder", "./images"))

    if image_folder.lower() == "mp3player":
        run_default_workflow()
        return

    if image_folder.lower() == "no":
        thumbnail_folder = prompt_directory("Enter the full path to the thumbnail directory or write 'default' to reset", config.get("thumbnail_folder", "./images/thumbnails"))
        if thumbnail_folder == "default":
            thumbnail_folder = "./images/thumbnails"
        if not verify_directory(thumbnail_folder, {'.jpg', '.jpeg', '.png', '.webp'}):
            return
    else:
        if image_folder == "default":
            image_folder = "./images"
        if not verify_directory(image_folder, {'.jpg', '.jpeg', '.png', '.webp'}):
            return
        thumbnail_folder = os.path.join(image_folder, "thumbnails")
        os.makedirs(thumbnail_folder, exist_ok=True)
        preprocess_images(image_folder, thumbnail_folder)
        config["image_folder"] = image_folder
        config["thumbnail_folder"] = thumbnail_folder

        if not config.get("image_folder"):
            save_image_paths = input("Do you want to save this image directory for future runs? (default: no): ").strip().lower() == 'yes'
            if save_image_paths:
                save_json(config, CONFIG_FILE)

    # Step 2: Music Directory
    music_folder = prompt_directory("Enter the full path to the music directory or write 'default' to reset or 'no' to skip", config.get("music_folder", "./music"))

    if music_folder.lower() != "no":
        if music_folder == "default":
            music_folder = "./music"
        if not verify_directory(music_folder, {'.mp3', '.m4a', '.opus'}):
            return
        preprocess_choice = input("Do you want to preprocess audio into MP3 files? (default: yes): ").strip().lower() != 'no'
        if preprocess_choice:
            bitrate = input("Enter the bitrate (default: 96k): ").strip() or '96k'
            preprocess_audio(music_folder, output_format='mp3', bitrate=bitrate)
        config["music_folder"] = music_folder

        if not config.get("music_folder"):
            save_music_paths = input("Do you want to save this music directory for future runs? (default: no): ").strip().lower() == 'yes'
            if save_music_paths:
                save_json(config, CONFIG_FILE)

    # Step 3: Add Album Art
    if music_folder.lower() != "no":
        apply_art_choice = input("Do you want to apply new thumbnails to the audio files? (default: yes): ").strip().lower() != 'no'
        if apply_art_choice:
            add_album_art(music_folder, thumbnail_folder, USED_ART_FILE)

    # Option to run again
    run_again_choice = input("Do you want to run the script again with new settings? (default: no): ").strip().lower() == 'yes'
    if run_again_choice:
        main()
    else:
        print("Exiting the program.")


if __name__ == "__main__":
    main()
