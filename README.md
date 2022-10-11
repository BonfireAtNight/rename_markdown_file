# rename_markdown_files
Rename Markdown files in accordance with the title of the document.

## Installation
The script doesn't need to be installed, just download and execute it. However, since you'll need to have Python installed. For ease of use it's convenient to put the script into a directory known to the PATH variable (like `~/.bin`).

## Usage
```bash
rename_markdown_files [FILE]... [OPTIONS]...
```

## Motivation
Markdown files have a name and (usually) a title (H1). In [Obsidian](https://obsidian.md/), the two are used for different purposes. Today, the file names primarily serves as unique identifier. [In the past](https://forum.obsidian.md/t/use-h1-or-front-matter-title-instead-of-or-in-addition-to-filename-as-display-name/687), it had been used in other contexts for which Obsidian now uses titles.

Among the [different possibilities](https://zettelkasten.de/introduction/#the-unique-identifier) to handle file name and title, many users prefer to keep them in sync. There is an Obsidian community plugin, [obsidian-filename-heading-sync](https://github.com/dvcrn/obsidian-filename-heading-sync), that automatically renames title and file if the respective other changes. The plugin cannot well be used to adhere to certain file-naming standards.

Users are often adviced to avoid spaces in their file names and to replace them by either the underscore (`_`) or the hyphen (`-`). More rigorous conventions recommend to replace uppercase letters with lowercase letters and to avoid all symbols other than letters, the underscore, and the hyphen.

The above-explained options account for these different conventions. Umlaute and certain symbols disallowed by Obsidian are removed without giving the option to keep them.

## Examples
```markdown
# Dies ist ein Titel / eine Überschrift!
Einige wichtige Informationen
```

```bash
rename_obsidian_files.py ~/Notes/test.md
# New file name: Dies ist ein Titel  eine Ueberschrift!.md

rename_obsidian_files.py ~/Notes/test.md -u
# New file name: Dies_ist_ein_Titel__eine_Ueberschrift!.md

rename_obsidian_files.py ~/Notes/test.md -ylo
# New file name: dies-ist-ein-titel--eine-ueberschrift.md

# Rename all files in the current directory
rename_obsidian_files.py *
```
