import argparse
import tiktoken
from gitignore_parser import parse_gitignore
import os
import logging

# Create a logger
logger = logging.getLogger()

class TokenCount:
    def __init__(self, model_name="gpt-3.5-turbo"):
        '''Creating the encoding based on model name'''
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except Exception as e:
            logger.error("Error occurred: {}".format(e))

    def num_tokens_from_string(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        try:
            num_tokens = len(self.encoding.encode(string))
            return num_tokens
        except Exception as e:
            logger.error("Error occurred: {}".format(e))

    def num_tokens_from_file(self, file_path: str) -> int:
        """Returns the number of tokens in a text file."""
        try:
            with open(file_path, "r") as f:
                text = f.read()
            num_tokens = len(self.encoding.encode(text))
            return num_tokens
        except Exception as e:
            logger.error("Error occurred: {}".format(e))

    def num_tokens_from_directory(self, dir_path: str, ignore_gitignore=True) -> int:
        """Recursively counts the total token count of all files in a directory"""
        try:
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
                        total_token_count += self.num_tokens_from_file(entry.path)
                    except:
                        print(f'Could not read file {entry.path}. Ignoring.')
                        continue
                elif entry.is_dir():
                    total_token_count += self.num_tokens_from_directory(entry.path)
            return total_token_count
        except Exception as e:
            logger.error("Error occurred: {}".format(e))

def main():
    parser = argparse.ArgumentParser(
        description="Count the number of tokens in a text string or file, similar to the Unix 'wc' utility.")
    parser.add_argument("-m", "--model_name", type=str, help="model name", default="gpt-3.5-turbo")
    parser.add_argument("-d", "--directory", type=str, help="directory to count tokens in")
    parser.add_argument("-f", "--file", type=str, help="file to count tokens in")
    parser.add_argument("-t", "--text", type=str, help="text to count tokens in")

    args = parser.parse_args()

    token_count = TokenCount(args.model_name)

    if not any([args.directory, args.file, args.text]):
        logger.info("No input provided")
        parser.print_help()
        return

    if args.directory:
        tokens = token_count.num_tokens_from_directory(args.directory)
        print(tokens)

    if args.file:
        tokens = token_count.num_tokens_from_file(args.file)
        print(tokens)

    if args.text:
        tokens = token_count.num_tokens_from_string(args.text)
        print(tokens)

if __name__ == "__main__":
    main()