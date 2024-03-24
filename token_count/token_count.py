import argparse
import tiktoken
import os
import logging
import fnmatch

# Create a logger
logger = logging.getLogger()

class TokenCount:
    def __init__(self, model_name="gpt-3.5-turbo"):
        '''Creating the encoding based on model name'''
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except Exception as e:
            logger.error("Error occurred: {}".format(e))

    def should_ignore(self, file_path, ignore_list):
        for pattern in ignore_list:
            if fnmatch.fnmatch(file_path, pattern):
                print(f'Ignoring {file_path} because it matches {pattern}')
                return True
        return False

    def get_ignore_list(self, repo_path):
        ignore_list = []
        ignore_file_path = None

        gpt_ignore_path = os.path.join(repo_path, ".gptignore")
        git_ignore_path = os.path.join(repo_path, ".gitignore")

        if os.path.exists(gpt_ignore_path):
            ignore_file_path = gpt_ignore_path
        elif os.path.exists(git_ignore_path):
            ignore_file_path = git_ignore_path

        if ignore_file_path:
            with open(ignore_file_path, 'r') as ignore_file:
                for line in ignore_file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    ignore_list.append(line)

        default_ignore_list = ['dist', 'dist/','dist/*','sdist', 'sdist/','sdist/*' '.git/', '/.git/', '.git', '.git/*', '.gptignore', '.gitignore', 'node_modules', 'node_modules/', 'node_modules/*', '__pycache__', '__pycache__/*']
        ignore_list += default_ignore_list

        return ignore_list

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
            ignore_list = self.get_ignore_list(dir_path)
            for entry in os.scandir(dir_path):
                if entry.name.startswith('.') or self.should_ignore(entry.path, ignore_list):
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