import os
import json
from pathlib import Path
from typing import Dict, Any


def parse_vab_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a .vab file and extract its metadata.
    
    Args:
        file_path: Path to the .vab file
        
    Returns:
        Dictionary containing parsed .vab data matching C# structure
    """
    try:
        absolute_path = os.path.abspath(file_path)
        
        return {
            'load_direct': True,
            'source': absolute_path,
            'name': os.path.basename(file_path),
            'filetype': 0xFFFFFF0F
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def parse_seq_file(file_path: str, vab_index: int) -> Dict[str, Any]:
    """
    Parse a .seq file and extract its metadata.
    
    Args:
        file_path: Path to the .seq file
        vab_index: Zero-based index of the corresponding VAB file (doubled)
        
    Returns:
        Dictionary containing parsed .seq data matching C# structure
    """
    try:
        absolute_path = os.path.abspath(file_path)
        filetype = 0x01020000 + vab_index
        
        return {
            'load_direct': True,
            'source': absolute_path,
            'name': Path(file_path).stem,
            'filetype': filetype
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def process_vab_directory(directory: str, output_json: str = 'vab_data.json') -> None:
    """
    Process all .vab files in a directory that have corresponding .seq files.
    Both files are added to the JSON with derived filetypes.

    Args:
        directory: Path to directory containing .vab files
        output_json: Path to output JSON file
    """
    vab_files = list(Path(directory).glob('*.vab'))

    if not vab_files:
        print(f"No .vab files found in {directory}")
        return

    data = []
    vab_pair_index = 0

    for vab_file in vab_files:
        seq_file = vab_file.with_suffix('.seq')

        # Only process VAB if corresponding SEQ file exists
        if not seq_file.exists():
            continue

        print(f"Processing: {vab_file.name}")
        file_data = parse_vab_file(str(vab_file))
        if file_data:
            data.append(file_data)

        print(f"Processing: {seq_file.name}")
        seq_data = parse_seq_file(str(seq_file), vab_pair_index * 2)
        if seq_data:
            data.append(seq_data)

        vab_pair_index += 1

    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully processed {len(data)} files")
    print(f"Output saved to: {output_json}")


def process_with_specific_vab(directory: str, vab_file_path: str, output_json: str = 'vab_data.json') -> None:
    """
    Process a specific .vab file and all .seq files in the directory that depend on it.

    Args:
        directory: Path to directory containing .seq files
        vab_file_path: Path to the specific .vab file to use
        output_json: Path to output JSON file
    """
    vab_path = Path(vab_file_path)

    if not vab_path.exists():
        print(f"Error: VAB file '{vab_file_path}' not found")
        return

    seq_files = list(Path(directory).glob('*.seq'))

    if not seq_files:
        print(f"No .seq files found in {directory}")
        return

    data = []

    # Add the specified VAB file
    print(f"Processing: {vab_path.name}")
    file_data = parse_vab_file(str(vab_path))
    if file_data:
        data.append(file_data)

    # Process all SEQ files with vab_index 0 (all depend on the first VAB)
    for seq_file in seq_files:
        print(f"Processing: {seq_file.name}")
        seq_data = parse_seq_file(str(seq_file), 0)
        if seq_data:
            data.append(seq_data)

    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully processed {len(data)} files")
    print(f"Output saved to: {output_json}")


def main() -> None:
    """Main entry point for the script."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python vabseq.py <directory> [output_json] [specific_vab_file]")
        print("Example: python vabseq.py ./vab_files output.json")
        print("Example: python vabseq.py ./vab_files output.json ./vab_files/game.vab")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found")
        sys.exit(1)

    # Check if a specific VAB file is provided as third argument
    if len(sys.argv) > 3:
        specific_vab = sys.argv[3]
        output_json = sys.argv[2] if len(sys.argv) > 2 else 'vab_data.json'
        process_with_specific_vab(directory, specific_vab, output_json)
    else:
        output_json = sys.argv[2] if len(sys.argv) > 2 else 'vab_data.json'
        process_vab_directory(directory, output_json)


if __name__ == '__main__':
    main()
