import argparse
import tiktoken
from gitignore_parser import parse_gitignore
import os
import logging

# Create a logger
logger = logging.getLogger()

class TokenCount:
    def __init__(self):
        '''Parsing the arguements. Creating the encoding based on model name'''
        try:
            self.parser = argparse.ArgumentParser(
                description="Count the number of tokens in a text string or file, similar to the Unix 'wc' utility.")
            self.parser.add_argument("-m", "--model_name", type=str, help="model name", default = "gpt-3.5-turbo")
            self.parser.add_argument("-d", "--directory", type=str, help="directory to count tokens in")
            self.parser.add_argument("-f", "--file", type=str, help="file to count tokens in")
            self.parser.add_argument("-t", "--text", type=str, help="text to count tokens in")

            self.args = self.parser.parse_args()

            self.encoding = tiktoken.encoding_for_model(self.args.model_name)

        except Exception as e:
            logger.error("Error occured: {}".format(e))

    def num_tokens_from_string(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        try:
            num_tokens = len(self.encoding.encode(string))
            return num_tokens
        except Exception as e:
            logger.error("Error occured: {}".format(e))

    def num_tokens_from_file(self, file_path: str) -> int:
        """Returns the number of tokens in a text file."""
        try:
            with open(file_path, "r") as f:
                text = f.read()
            num_tokens = len(self.encoding.encode(text))
            return num_tokens
        except Exception as e:
            logger.error("Error occured: {}".format(e))

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
                        total_token_count += num_tokens_from_file(entry.path)
                    except:
                        print(f'Could not read file {entry.path}. Ignoring.')
                        continue
                elif entry.is_dir():
                    total_token_count += num_tokens_from_directory(entry.path)
            return total_token_count
        except Exception as e:
            logger.error("Error occured: {}".format(e))

    def token_count(self):
        try:
            if not any([self.args.directory, self.args.file, self.args.text]):
                logger.info("No input provided")
                self.parser.print_help()
                return

            if self.args.directory:
                tokens = self.num_tokens_from_directory(self.args.directory)
                print(tokens)

            if self.args.file:
                tokens = self.num_tokens_from_file(self.args.file)
                print(tokens)

            if self.args.text:
                tokens = self.num_tokens_from_string(self.args.text)
                print(tokens)
        except Exception as e:
            logger.error("Error occured: {}".format(e))

if __name__ == "__main__":
    token_count = TokenCount()
    token_count.token_count()
