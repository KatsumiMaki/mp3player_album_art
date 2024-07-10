# MP3 Album Art Embedder

This project allows you to embed album art into MP3 files, ensuring that album art is not repeated until all available images have been used. Compression of art and music is the default.

## Features

- Embed album art into MP3 files.
- Track used album art to avoid redundancies.
- Reset album art list when all images have been used.
- Configurable paths for MP3 files, album art images, and used art list.
- Quick mode for using default settings to streamline the process.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/KatsumiMaki/mp3player_album_art.git
    cd mp3player_album_art
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Paths**:
    - Paths can be configured interactively when running the script.
    - Alternatively, you can use the quick mode to use default settings.

## Usage

### Running the Script

1. **Run the Script**:
    ```bash
    python main.py
    ```

2. **Follow the Prompts**:
    - The script will guide you through setting up the image and music directories and applying album art.
    - You will be asked:
        - If you want to reset path directories if they have been changed in prior runs.
        - To enter the image directory, with options to reset to default, skip, or use the last known directory.
        - To enter the music directory, with options to reset to default, skip, or use the last known directory.
        - If you want to preprocess audio into MP3 files, and if so, what bitrate to use.
        - If you want to apply new thumbnails to the audio files.
        - If you want to save the list of used album arts.
        - If you want to run the script again with new settings.

### Quick Mode

For users who prefer to use default settings for a faster setup, you can run the script in quick mode by typing `mp3player` when prompted for the image directory.

**Quick Mode Default Settings**:
- Image directory: `./images`
- Thumbnail directory: `./images/thumbnails`
- Music directory: `./music`
- Audio preprocessing: Converts to MP3 at 96kbps
- Saves used album art list

**Steps in Quick Mode**:
1. Sets image directory to `./images`.
2. Sets thumbnail directory to `./images/thumbnails`.
3. Sets music directory to `./music`.
4. Converts all audio files in the music directory to MP3 at 96kbps.
5. Embeds album art from the thumbnail directory into MP3 files.
6. Saves the list of used album arts.
7. Completes without further prompts.

### ImageMagick Support

If you have ImageMagick installed on your Windows path or have `magick.exe` in the local directory, you can use the provided batch file for faster image processing. ImageMagick is much faster at processing due to its low-level use of hardware in C programming, which is especially useful for compressing large files or many files.

**Batch File Usage**:
0. Ensure ImageMagick is installed and accessible via your system's PATH or place `magick.exe` in the local directory.
1. Place your full-size images in ./images
2. Read .bat files in a program like [Notepad++](https://notepad-plus-plus.org/) before ever using it. You shouldn't trust me, a random internet user.
3. Run the batch file:
    ```bash
    .\magick_process_images.bat
    ```
	or double click it. 
4. CMD will open up and sit there, ominously blank. If you didn't read the .bat file with your eyeballs, this should make you very afraid. But really it will just be churning through your images. You can go to the default output directory (.\images\thumbnails) to see them show up in real time.
5. If the defaults hurts your eyes (jpg at 300x300), just edit the mogrify command in the .bat file. You did read the .bat file, right?

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Contribution

Contributions are welcome! Please create a pull request or open an issue to discuss changes.

## Detailed Steps of the Program

1. **Initialization**:
    - Loads the configuration from `config.json`.
    - Prompts the user to reset path directories if they have been changed in prior runs.

2. **Image Directory Setup**:
    - Prompts for the full path to the image directory or options to reset to default, skip, or use the last known directory.
    - Validates the directory and checks for at least one image file.

3. **Thumbnail Directory Setup**:
    - If image processing is yes, sets up the thumbnail directory.
    - Creates the directory if it doesn't exist and processes images using `preprocess_images.py`.

4. **Music Directory Setup**:
    - Prompts for the full path to the music directory or options to reset to default, skip, or use the last known directory.
    - Validates the directory and checks for at least one audio file.

5. **Audio Preprocessing**:
    - If yes, preprocesses audio files into MP3 format using `preprocess_audio.py` with the specified bitrate.

6. **Album Art Embedding**:
    - Applies new thumbnails to the audio files using `add_album_art.py`.
    - Ensures album art is not repeated until all available images have been used.

7. **Save Used Album Art List**:
    - Prompts to save the list of used album arts to avoid redundancies in future runs.

8. **Run Again Option**:
    - Prompts to run the script again with new settings if desired.

Hope you enjoy your mp3 files, now with random album art.