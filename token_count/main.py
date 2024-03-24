# main.py
import argparse
from token_count import TokenCount
import logging


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