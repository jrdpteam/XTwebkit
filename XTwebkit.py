import requests
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Style
import re
from urllib.parse import urljoin
import os

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

def crawl(url, save_strings, download_types, output_folder):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        session = requests.Session()
        response = session.get(url)
        print(f"{Fore.WHITE}GET   --->   {url} [Response: {response.status_code}]{Style.RESET_ALL}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            visible_text = soup.get_text(separator='\n', strip=True)

            for input_tag in soup.find_all('input'):
                print(f"{Fore.YELLOW}[Input] {url} --> {input_tag}{Style.RESET_ALL}")

            for img_tag in soup.find_all('img'):
                src = img_tag.get('src')
                if src:
                    full_url = urljoin(url, src)
                    print(f"{Fore.MAGENTA}[Image] {url} --> {src} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                    if 'images' in download_types:
                        download_file(full_url, output_folder, 'images')

            for link_tag in soup.find_all('a'):
                link = link_tag.get('href')
                if link:
                    full_url = urljoin(url, link)
                    print(f"{Fore.GREEN}[Link] {link} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                    with open('links.txt', 'a', encoding='utf-8') as f:
                        f.write(full_url + '\n')

            video_sources = set()
            for video_tag in soup.find_all('video'):
                for source in video_tag.find_all('source'):
                    src = source.get('src')
                    if src and src not in video_sources:
                        video_sources.add(src)
                        full_url = urljoin(url, src)
                        print(f"{Fore.BLUE}[Video] {url} --> {src} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                        if 'videos' in download_types:
                            download_file(full_url, output_folder, 'videos')

            audio_sources = set()
            for audio_tag in soup.find_all('audio'):
                for source in audio_tag.find_all('source'):
                    src = source.get('src')
                    if src and src not in audio_sources:
                        audio_sources.add(src)
                        full_url = urljoin(url, src)
                        print(f"{Fore.CYAN}[Audio] {url} --> {src} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                        if 'audio' in download_types:
                            download_file(full_url, output_folder, 'audio')

            for css_tag in soup.find_all('link', rel='stylesheet'):
                href = css_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    print(f"{Fore.WHITE}[CSS] {url} --> {href} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                    if 'css' in download_types:
                        download_file(full_url, output_folder, 'css')

            for script_tag in soup.find_all('script'):
                src = script_tag.get('src')
                if src:
                    full_url = urljoin(url, src)
                    print(f"{Fore.GREEN}[JS] {url} --> {src} -> {full_url} [Response: {response.status_code}]{Style.RESET_ALL}")
                    if 'js' in download_types:
                        download_file(full_url, output_folder, 'js')

            for meta_tag in soup.find_all('meta'):
                content = meta_tag.get('content')
                name = meta_tag.get('name')
                if name and content:
                    print(f"{Fore.YELLOW}[Meta] {url} --> {name}: {content}{Style.RESET_ALL}")

            if save_strings:
                with open('strings.txt', 'w', encoding='utf-8') as f:
                    f.write(visible_text)

    except Exception as e:
        print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")

def download_file(url, output_folder, file_type):
    try:
        session = requests.Session()
        response = session.get(url)
        if response.status_code == 200:
            if not os.path.exists(os.path.join(output_folder, file_type)):
                os.makedirs(os.path.join(output_folder, file_type))
            file_name = os.path.basename(url)
            with open(os.path.join(output_folder, file_type, file_name), 'wb') as f:
                f.write(response.content)
            print(f"{Fore.CYAN}Downloaded: {url} to {output_folder}/{file_type}/{file_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to download {url}: {response.status_code}{Style.RESET_ALL}")
            retry = input("Retry? (yes/no): ").strip().lower()
            if retry == 'yes':
                download_file(url, output_folder, file_type)
    except Exception as e:
        print(f"{Fore.RED}Error downloading {url}: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='XTwebkit - A web crawling tool for scraping web content.')
    parser.add_argument('-t', '--target', required=True, help='Target URL to crawl.')
    parser.add_argument('-s', '--strings', action='store_true', help='Save visible text content to strings.txt.')
    parser.add_argument('-d', '--download', help='Comma-separated types of files to download. Available types: [images, videos, audio, css, js].')
    parser.add_argument('-w', '--output', default='downloads', help='Output folder for downloaded files (default: downloads).')
    
    args = parser.parse_args()

    target_url = args.target
    download_types = args.download.split(',') if args.download else []
    
    visited_urls = set()
    crawl(target_url, args.strings, download_types, args.output)
