#!/bin/bash

python3 - <<EOF
import os
from pathlib import Path
from filecmp import cmp
  
subDirectories=(
        ["DOCUMENTS"]=(".pdf" ".docx" ".txt")
        ["AUDIO"]=(".m4a" ".m4b" ".mp3")
        ["IMAGES"]=(".jpg" ".jpeg" ".png")
        ["CSVS"]=(".csv")
        ["CODE"]=(".py" ".html" ".java")
        )

pick_directory() {
    local value="$1"
    for category in "${!subDirectories[@]}"; do
        for suffix in "${subDirectories[$category]}"; do
            if [[ "$suffix" == "$value" ]]; then
                echo "$category"
                return
            fi
        done
    done
}

organizeDir() {
    for item in *; do

        # Skip directories, process files only
        if [[ -d "$item" ]]; then
            continue
        fi

        fileType="${item##*.}"
        directory=$(pick_directory ".$fileType")

        # Skip if directory is not defined for the extension
        if [[ -z "$directory" ]]; then
            continue
        fi

        # Create directory if not present
        if [[ ! -d "$directory" ]]; then
            mkdir "$directory"
        fi

        mv "$item" "$directory/$item"
    done
}

path="$1"
DATA_DIR="$path"
files=($(ls "$DATA_DIR"))

declare -A duplicateFiles

for file_x in "${files[@]}"; do
  
    if_dupl=false
  
    for class_ in "${!duplicateFiles[@]}"; do
        if cmp -s "$DATA_DIR/$file_x" "$DATA_DIR/$class_"; then
            if_dupl=true
            duplicateFiles["$class_"]="${duplicateFiles[$class_]} $file_x"
            break
        fi
    done

    if ! $if_dupl; then
        duplicateFiles["$file_x"]="$file_x"
    fi
done

for files in "${!duplicateFiles[@]}"; do
    echo "${duplicateFiles[$files]}"
done
organizeDir
EOF
