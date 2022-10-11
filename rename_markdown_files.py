#!/usr/bin/env python

import argparse

import os
import sys
import string


def parse_args():
    cli_parser = argparse.ArgumentParser(
        prog="obsidian_renamer",
        usage="%(prog)s [options] path(s)",
        description="Rename Obsidian file(s) in accordance with Markdown title",
        allow_abbrev=False,
    )

    space_replacement = cli_parser.add_mutually_exclusive_group()

    cli_parser.add_argument(
        "files",
        # metavar="file",
        nargs="*",
        type=str,
        default=(None if sys.stdin.isatty() else sys.stdin),
        action="store",
        help="the file to be renamed",
    )

    space_replacement.add_argument(
        "-u",
        "--underscore",
        action="store_true",
        help="replace spaces with underscores",
    )

    space_replacement.add_argument(
        "-y",
        "--hyphen",
        action="store_true",
        help="replace spaces with hyphens",
    )

    cli_parser.add_argument(
        "-l",
        "--lower",
        action="store_true",
        help="enable to generate all lowercase file names",
    )

    cli_parser.add_argument(
        "-o",
        "--only_letters",
        action="store_true",
        help="remove all symbols other than letters, underscore, or hyphen",
    )

    parsed_args = cli_parser.parse_args()

    return parsed_args


def replace_umlaut(umlaut):
    match umlaut:
        case "ä":
            return "ae"
        case "ö":
            return "oe"
        case "ü":
            return "ue"
        case "Ä":
            return "Ae"
        case "Ö":
            return "Oe"
        case "Ü":
            return "Ue"


def replace_space(args):
    if args.underscore:
        return "_"
    elif args.hyphen:
        return "-"


def spaces_should_be_replaced(args):
    if args.underscore or args.hyphen:
        return True
    else:
        return False


def is_forbidden_symbol(symbol):
    strictly_illegal_symbols = ["\\", "/", ":"]
    imprudent_symbols = ["#", "|", "^", "[", "]"]

    if symbol in strictly_illegal_symbols or symbol in imprudent_symbols:
        return True
    else:
        return False


def is_recommended_for_filename(symbol):
    alphabet = list(string.ascii_letters)

    if symbol in alphabet or symbol == "_" or symbol == "-":
        return True
    else:
        return False


def rename_file(path, args):
    new_filename = ""

    with open(path, "r") as file:
        line = file.readline().rstrip()
        while line[:2] != "# ":
            line = file.readline().rstrip()
        title = line[2:]
        file.close()

    for i in range(len(title)):
        if is_forbidden_symbol(title[i]):
            continue
        elif title[i] in "ÄÖÜäöü":
            if args.lower:
                new_filename += replace_umlaut(title[i]).lower()
            else:
                new_filename += replace_umlaut(title[i])
        elif title[i] == " ":
            if spaces_should_be_replaced(args):
                new_filename += replace_space(args)
            else:
                new_filename += title[i]
        elif args.lower and title[i].isupper():
            new_filename += title[i].lower()
        elif not is_recommended_for_filename(title[i]):
            if args.only_letters:
                continue
            else:
                new_filename += title[i]
        else:
            new_filename += title[i]

    filename_with_extension = new_filename + ".md"
    if not os.path.exists(filename_with_extension):
        os.rename(path, filename_with_extension)
        print(path + " was renamed to " + filename_with_extension)
    else:
        print("Cannot create file. " + filename_with_extension + " already exists.")


def main():
    """Rename Obsidian file in accordance with title of Markdown document.
    If no file is given, the program reads stdin.

    Keyword arguments:
    file -- the file to be renamed
    underscore (default False) -- replace spaces by underscores
    hyphen (default False) -- replace spaces by hyphens
    lower (default False) -- replace uppercase letters by lowercase letters
    only_letters (default False) -- remove symbols that are not letters, '_', or '-'
    """
    args = parse_args()
    list_of_files = args.files
    use_underscore = args.underscore
    use_hyphen = args.hyphen
    use_all_lower = args.lower
    use_only_letters = args.only_letters

    for file in list_of_files:
        rename_file(file, args)


if __name__ == "__main__":
    main()
