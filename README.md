# Stow [![Python application](https://github.com/dotbrains/stow/actions/workflows/python-app.yml/badge.svg)](https://github.com/dotbrains/stow/actions/workflows/python-app.yml)

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

## Tests

To run the tests, execute the following command:

```bash
python3 test_stow.py
```

### Running the tests within Git Bash on Windows in PyCharm

To run the tests within Git Bash on Windows in PyCharm, you need to set the `SHELL` environment variable to `bash.exe`:

1. Open the `Run/Debug Configurations` dialog.
2. Select the `stow` configuration.
3. Add the following environment variable:
   * Name: `SHELL`
   * Value: `bash.exe`
   * Description: `Path to the shell executable`
4. Click `OK` to save the configuration.
5. Run the tests.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

