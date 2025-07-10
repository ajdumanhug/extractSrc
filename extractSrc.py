import os
import json
import requests
from urllib.parse import urljoin, urlparse

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def download_sourcemap(js_url):
    sm_url = js_url + ".map"
    try:
        response = requests.get(sm_url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[!] Failed to download or parse sourcemap: {sm_url}\n    Error: {e}")
        return None

def save_sources(smap, base_url, output_dir):
    sources = smap.get("sources", [])
    contents = smap.get("sourcesContent", [])

    base_output_dir = os.path.join(output_dir, "output")

    for i, source_path in enumerate(sources):
        content = contents[i] if i < len(contents) else ''

        parsed_path = urlparse(source_path)
        cleaned_path = parsed_path.path.lstrip('/')
        local_path = os.path.join(base_output_dir, cleaned_path)
        local_path = os.path.normpath(local_path)

        abs_base_output_dir = os.path.abspath(base_output_dir)
        abs_local_path = os.path.abspath(local_path)
        if not abs_local_path.startswith(abs_base_output_dir + os.sep):
            print(f"[!] Skipping suspicious path: {local_path}")
            continue

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)

def process_file(input_file, output_dir):
    with open(input_file, 'r') as f:
        js_urls = [line.strip() for line in f if line.strip()]

    total = len(js_urls)
    print(f"Total number of links: {total}")

    for idx, js_url in enumerate(js_urls, 1):
        print(f"Processing {idx}/{total}: {js_url}")
        smap = download_sourcemap(js_url)
        if smap:
            save_sources(smap, js_url, output_dir)
            filename = os.path.basename(js_url)
            print(f"Processing of '{filename}' is complete")
        else:
            print("[!] Failed")

    base_output_dir = os.path.join(output_dir, "output")
    print("\nDirectory structure:")
    import subprocess
    try:
        result = subprocess.run(["tree", base_output_dir], capture_output=True, text=True, check=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Could not display directory tree: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and extract files from sourcemaps.")
    parser.add_argument("-i", "--input-file", required=True, help="Text file containing list of JS URLs")
    parser.add_argument("-o", "--output-dir", required=True, help="Directory to save extracted sources")

    args = parser.parse_args()
    process_file(args.input_file, args.output_dir)
