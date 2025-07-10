# extractSrc
A python script to download and extract files from sourcemaps.

## Features
- Downloads sourcemaps for a list of JS bundle URLs
- Extracts and saves original source files
- Organizes output in a user-specified directory
- Shows progress and a summary tree of extracted files

## Installation

1. Clone this repository.
2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Prepare a text file (e.g., `urls.txt`) containing one JS bundle URL per line.

Run the tool with:

```sh
python srcmapper.py -i urls.txt -o my_output_dir
```

- `-i`, `--input-file`: Path to the text file with JS URLs (required)
- `-o`, `--output-dir`: Directory to save extracted sources (required)

Extracted files will be saved under `<output-dir>/output/`.

## Example

Suppose `urls.txt` contains:
```
https://example.com/static/js/main.chunk.js
https://example.com/static/js/vendor.chunk.js
```

Run:
```sh
python srcmapper.py -i urls.txt -o my_sources
```

Sample output:
```
Total number of links: 2
Processing 1/2: https://example.com/static/js/main.chunk.js
Processing of 'main.chunk.js' is complete
Processing 2/2: https://example.com/static/js/vendor.chunk.js
[!] Failed

Directory structure:
my_sources\output
├── src
│   ├── file1.js
│   └── file2.js
└── ...
```

## Notes
- Only the `requests` library is required (see `requirements.txt`).
- The tool prints a summary tree of the output directory at the end.
- If a sourcemap cannot be downloaded or parsed, it will print `[!] Failed` for that entry.
