@echo off
setlocal
set IMG_DIR=.\images
set OUT_DIR=.\images\thumbnails

if not exist %IMG_DIR% (
    mkdir %IMG_DIR%
	copy NUL %IMG_DIR%\PLACE_IMAGES_HERE
)

if not exist %OUT_DIR% (
    mkdir %OUT_DIR%
)

magick mogrify -path %OUT_DIR% -resize 300x300 -format jpg %IMG_DIR%/*

endlocal
