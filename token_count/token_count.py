import argparse
import tiktoken
from gitignore_parser import parse_gitignore
import os

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def main():
    parser = argparse.ArgumentParser(
        description="Count the number of tokens in a text string or file, similar to the Unix 'wc' utility.")
    parser.add_argument("-d", "--directory", type=str, help="directory to count tokens in")
    parser.add_argument("-f", "--file", type=str, help="file to count tokens in")
    parser.add_argument("-t", "--text", type=str, help="text to count tokens in")
    args = parser.parse_args()

    if not any([args.directory, args.file, args.text]):
        print("No input provided")
        parser.print_help()
        return

    if args.directory:
        tokens = num_tokens_from_directory(args.directory)
        print(tokens)

    if args.file:
        tokens = num_tokens_from_file(args.file)
        print(tokens)

    if args.text:
        tokens = num_tokens_from_string(args.text)
        print(tokens)

def num_tokens_from_string(string: str, encoding_name: str = "p50k_base") -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_file(file_path: str, encoding_name: str = "p50k_base") -> int:
    """Returns the number of tokens in a text file."""
    with open(file_path, "r") as f:
        text = f.read()
    num_tokens = len(encoding.encode(text))
    return num_tokens

def num_tokens_from_directory(dir_path: str, encoding_name: str = "p50k_base", ignore_gitignore=True) -> int:
    """Recursively counts the total token count of all files in a directory"""
    total_token_count = 0
    gitignore_path = f'./{dir_path}/.gitignore'
    if ignore_gitignore and os.path.isfile(gitignore_path):
        is_ignored = parse_gitignore(gitignore_path)
    else:
        is_ignored = lambda x: False
    for entry in os.scandir(dir_path):
        if entry.name.startswith('.') or is_ignored(entry.path):
            continue
        if entry.is_file():
            try:
                total_token_count += num_tokens_from_file(entry.path, encoding_name)
            except:
                print(f'Could not read file {entry.path}. Ignoring.')
                continue
        elif entry.is_dir():
            total_token_count += num_tokens_from_directory(entry.path, encoding_name)
    return total_token_count

if __name__ == "__main__":
    main()
