# Stow

![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)

This script mimics the functionality of GNU Stow, allowing you to create symlinks to files and directories in a specified path.

## Why did I create `stow`?

It is not possible to install the traditional GNU `stow` command on Windows.

Therefore, I have constructed a [`python` script](/stow.py) that mimics the core behavior of GNU `stow`.

## Installing `stow` on Windows

1. **Obtain the `stow` script**:
   ```bash
   wget https://github.com/dotbrains/stow/-/raw/main/stow.py -O ~/.local/bin/stow
   ```

2. **Make the script executable**:
   ```bash
   chmod +x ~/.local/bin/stow
   ```

3. **Add it to your PATH (optional)**:
   If you want to run the script from anywhere, you can add it to your `PATH`. For example, add the following line to your `.bashrc` or `.zshrc`:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

## Usage

To use the script, simply run it from the command line:

```bash
stow
```

By default, the script will create symlinks to all files and directories in the current directory, excluding those listed in `.stow-local-ignore` to the current users' `$HOME` directory.

## Options

The script accepts the following options:

* `-h, --help`: Print this help message
* `-n, --dry-run`: Perform a dry run and print the resulting file system structure
* `-p, --path`: Specify the path to the directory containing files to stow

## Example Use Cases

* Create symlinks to all files and directories in the current directory:

```bash
stow
```

* Perform a dry run and print the resulting file system structure:

```bash
stow -n
```

* Specify a custom path to the directory containing files to stow:

```bash
stow -p /path/to/directory
```

## Requirements

* Bash shell
* `ln` command (for creating symlinks)
* `mkdir` command (for creating directories)

## Example Run

```text
[+] Using path: /path/to/source
[+] --- Stow Configuration ---
[+] Source Directory: /path/to/source
[+] Ignore List: ['.stow-local-ignore']
[+] Target Directory: /home/user
[+] Dry Run: False
[!] --- Files to Stow ---
[!] - file1
[!] - file2
[!] - file3
[+] --- Stowing Files ---
[!] Would create symlink: /home/user/file1 -> /path/to/source/file1
[!] Would create symlink: /home/user/file2 -> /path/to/source/file2
[!] Would create symlink: /home/user/file3 -> /path/to/source/file3
```
