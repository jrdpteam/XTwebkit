# XTwebkit_v1.0

XTwebkit_v1.0 is a tool for scanning and downloading resources from specified websites. It allows you to extract data such as images, videos, audio, and forms, and saves them in an organized folder structure.

## Features

- **Scraping**: Extract visible data such as text, images, links, audio, and videos.
- **Downloading**: Automatically download multimedia files to a specified folder on disk.
- **Error Handling**: Provides information about HTTP errors, such as 404, with retry options.
- **File Organization**: Files are saved in subfolders based on their type (e.g., `images`, `videos`, `audio`).

## Requirements

- Python 3.x
- Libraries: `requests`, `beautifulsoup4`, `colorama`

## Installation

1. Clone the repository to your local system:

   ```bash
   git clone https://github.com/jrdpteam/XTwebkit
   cd XTwebkit
2. Install the dependencies:
   
       bash install_dependencies.sh

3. Now you can run XTwebkit:

       python3 XTwebkit.py -h

4. Example usage:

       python XTwebkit.py -t "http://example.com" -o "images,videos,audio" -d "images,videos,audio" -w "downloaded_files"
