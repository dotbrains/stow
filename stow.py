#!/usr/bin/env python

import os
import argparse
import sys

# ANSI color codes with reset properly defined
class TerminalColors:
    SUCCESS = "\033[92m"  # Green
    INFO = "\033[34m"     # Blue
    WARNING = "\033[93m"  # Yellow
    ERROR = "\033[91m"    # Red
    DEBUG = "\033[96m"    # Cyan
    RESET = "\033[0m"     # Reset

# Log prefixes for consistency
LOG_PREFIXES = {
    "INFO": "[i]",
    "WARN": "[!]",
    "SUCCESS": "[✔]",
    "ERROR": "[X]",
    "DEBUG": "[D]"
}

# Logging functions
def log_info(message):
    """Log informational messages."""
    print(f"{TerminalColors.INFO}{LOG_PREFIXES['INFO']} {message}{TerminalColors.RESET}")

def log_warn(message):
    """Log warning messages."""
    print(f"{TerminalColors.WARNING}{LOG_PREFIXES['WARN']} {message}{TerminalColors.RESET}")

def log_success(message):
    """Log success messages."""
    print(f"{TerminalColors.SUCCESS}{LOG_PREFIXES['SUCCESS']} {message}{TerminalColors.RESET}")

def log_error(message):
    """Log error messages."""
    print(f"{TerminalColors.ERROR}{LOG_PREFIXES['ERROR']} {message}{TerminalColors.RESET}")

def log_debug(message):
    """Log debug messages."""
    print(f"{TerminalColors.DEBUG}{LOG_PREFIXES['DEBUG']} {message}{TerminalColors.RESET}")

# Core functionality
def parse_ignore_file(ignore_file):
    """Parse the ignore file to get a list of files/directories to ignore."""
    try:
        with open(ignore_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        log_warn(f"Ignore file '{ignore_file}' not found. Proceeding without it.")
        return []

def get_files_to_stow(path, ignore_list):
    """Get all files and directories to be stowed, excluding ignored paths."""
    files_to_stow = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            if any(relative_path.startswith(ignore) for ignore in ignore_list):
                continue
            files_to_stow.append((file_path, relative_path))

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            relative_path = os.path.relpath(dir_path, path)
            if any(relative_path.startswith(ignore) for ignore in ignore_list):
                continue
            files_to_stow.append((dir_path, relative_path))

    return files_to_stow

def stow_files(target_dir, dry_run, files_to_stow):
    """Create symlinks for files and directories to the target directory."""
    for file_path, relative_path in files_to_stow:
        target_path = os.path.join(target_dir, relative_path)

        if dry_run:
            log_warn(f"Would create symlink: {target_path} -> {file_path}")
            continue

        try:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            if os.path.exists(target_path) or os.path.islink(target_path):
                os.remove(target_path)
            os.symlink(file_path, target_path)
            log_success(f"Created symlink: {target_path} -> {file_path}")
        except OSError as e:
            log_error(f"Error creating symlink for {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Stow files from a directory to your home directory',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-n', '--dry-run', action='store_true', help='Perform a dry run and print the resulting file system structure')
    parser.add_argument('-p', '--path', default=os.getcwd(), help='Specify the path to the directory containing files to stow (default: current directory)')
    args = parser.parse_args()

    source_path = os.path.abspath(args.path)
    target_dir = os.path.expanduser('~')

    if not os.path.isdir(source_path):
        log_error(f"Error: Path '{source_path}' does not exist or is not a directory.")
        sys.exit(1)

    ignore_file = os.path.join(source_path, '.stow-local-ignore')
    ignore_list = parse_ignore_file(ignore_file) + ['.stow-local-ignore']
    files_to_stow = get_files_to_stow(source_path, ignore_list)

    log_info(f"Using path: {source_path}")
    log_info("--- Stow Configuration ---")
    log_info(f"Source Directory: {source_path}")
    log_info(f"Ignore List: {ignore_list}")
    log_info(f"Target Directory: {target_dir}")
    log_info(f"Dry Run: {args.dry_run}")

    if not files_to_stow:
        log_warn("No files or directories found to stow.")
    else:
        log_info("--- Files to Stow ---")
        for _, relative_path in files_to_stow:
            log_info(f"- {relative_path}")

        log_info("--- Stowing Files ---")
        stow_files(target_dir, args.dry_run, files_to_stow)

if __name__ == "__main__":
    main()
