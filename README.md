# vabseq

A Python script for processing `.vab` and `.seq` files, extracting metadata, and exporting the results to a JSON file. Useful for workflows that require pairing VAB/SEQ files and generating structured data for further processing.

## Features

- Parses `.vab` files and their corresponding `.seq` files in a directory.
- Supports processing a specific `.vab` file with all `.seq` files in a directory.
- Outputs results as a JSON file compatible with C# structures.

## Requirements

- Python 3.7 or higher

## Usage

Run the script from the command line:

```sh
python vabseq.py <directory> [output_json] [specific_vab_file]
```

### Arguments

- `<directory>`: Path to the directory containing `.vab` and/or `.seq` files.
- `[output_json]` (optional): Name of the output JSON file (default: `vab_data.json`).
- `[specific_vab_file]` (optional): Path to a specific `.vab` file to use with all `.seq` files in the directory.

### Examples

**Process all `.vab` files with matching `.seq` files:**

```sh
python vabseq.py ./vab_files
```

**Specify output file:**

```sh
python vabseq.py ./vab_files output.json
```

**Process a specific `.vab` file with all `.seq` files:**

```sh
python vabseq.py ./vab_files output.json ./vab_files/game.vab
```

## Output

- The script generates a JSON file containing metadata for each processed file.
- Each entry includes:
  - `load_direct`
  - `source`
  - `name`
  - `filetype`

## License

MIT
