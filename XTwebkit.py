import requests
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Style
import re
import os
from urllib.parse import urljoin
import time

ascii_art = f"""
{Fore.RED} __   _________           _     _    _ _   
 \\ \\ / /__   __|         | |   | |  (_) |  
  \\ V /   | |_      _____| |__ | | ___| |_ 
   > <    | \\ \\ /\\ / / _ \\ '_ \\| |/ / | __|
  / . \\   | |\\ V  V /  __/ |_) |   <| | |_ 
 /_/ \\_\\  |_| \\_/\\_/ \\___|_.__/|_|\\_\\_|\\__|{Fore.MAGENTA}
<----- XTwebkit_v1.0   by {Fore.RED}JRDP Team {Fore.MAGENTA} ----->
 
 {Style.RESET_ALL}
"""
print(ascii_art)

def clean_content(text):
    clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
    return clean

def download_file(url, output_folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_type = url.split('.')[-1]
            folder_path = os.path.join(output_folder, file_type)
            os.makedirs(folder_path, exist_ok=True)
            file_name = os.path.join(folder_path, url.split('/')[-1])
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"{Fore.CYAN}[Downloaded] {url} to {file_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to download {url}: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error downloading {url}: {e}{Style.RESET_ALL}")

def crawl(url, options, save_strings, output_folder):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        session = requests.Session()
        response = session.get(url)
        print(f"{Fore.WHITE}GET   --->   {url} [Response: {response.status_code}]{Style.RESET_ALL}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if 'images' in options:
                for img_tag in soup.find_all('img'):
                    src = img_tag.get('src')
                    if src:
                        full_url = urljoin(url, src)
                        download_file(full_url, output_folder)
            if 'videos' in options:
                for video_tag in soup.find_all('video'):
                    for source in video_tag.find_all('source'):
                        src = source.get('src')
                        if src:
                            full_url = urljoin(url, src)
                            download_file(full_url, output_folder)
            if 'audio' in options:
                for audio_tag in soup.find_all('audio'):
                    for source in audio_tag.find_all('source'):
                        src = source.get('src')
                        if src:
                            full_url = urljoin(url, src)
                            download_file(full_url, output_folder)

            if save_strings:
                visible_text = soup.get_text(separator='\n', strip=True)
                with open('strings.txt', 'w', encoding='utf-8') as f:
                    f.write(visible_text)

    except requests.exceptions.HTTPError as e:
        print(f"{Fore.RED}HTTP Error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument('-o', '--options', required=True)
    parser.add_argument('-s', '--strings', action='store_true')
    parser.add_argument('-d', '--download', help='Download types', default=None)
    parser.add_argument('-w', '--output', help='Output folder for downloads', default='downloads')
    args = parser.parse_args()

    target_url = args.target
    options = args.options.split(',')
    get_strings = "YES" if args.strings else "NO"

    print(f"{Fore.WHITE}settings: {', '.join(options)}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}get strings? {get_strings}{Style.RESET_ALL}")

    visited_urls = set()
    
    if args.download:
        download_types = args.download.split(',')
        crawl(target_url, options, args.strings, args.output)
        print(f"{Fore.RED}Download completed!{Style.RESET_ALL}")
    else:
        crawl(target_url, options, args.strings, None)
