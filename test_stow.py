import unittest
import os
import tempfile
import shutil

from stow import (
    parse_ignore_file,
    get_files_to_stow,
    stow_files
)

class TestStow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ignore_file = os.path.join(self.temp_dir, '.stow-local-ignore')
        with open(self.ignore_file, 'w') as f:
            f.write('# Comment\n')
            f.write('.git\n')

        self.file1 = os.path.join(self.temp_dir, 'file1.txt')
        with open(self.file1, 'w') as f:
            f.write('Hello, World!')

        self.dir1 = os.path.join(self.temp_dir, 'dir1')
        os.mkdir(self.dir1)
        self.file2 = os.path.join(self.dir1, 'file2.txt')
        with open(self.file2, 'w') as f:
            f.write('Hello, World!')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_parse_ignore_file(self):
        ignore_list = parse_ignore_file(self.ignore_file)
        self.assertEqual(ignore_list, ['.git'])

    def test_get_files_to_stow(self):
        ignore_list = parse_ignore_file(self.ignore_file)
        files_to_stow = get_files_to_stow(self.temp_dir, ignore_list)
        self.assertEqual(len(files_to_stow), 4)
        self.assertIn(self.file1, [file_path for file_path, _ in files_to_stow])
        self.assertIn(self.file2, [file_path for file_path, _ in files_to_stow])

    def test_stow_files(self):
        ignore_list = parse_ignore_file(self.ignore_file)
        files_to_stow = get_files_to_stow(self.temp_dir, ignore_list)
        target_dir = tempfile.mkdtemp()
        stow_files(target_dir, False, files_to_stow)
        # Check that the files exist in the target directory (could be symlink, hardlink, or copy)
        self.assertTrue(os.path.exists(os.path.join(target_dir, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(target_dir, 'dir1', 'file2.txt')))
        # Verify the content is correct
        with open(os.path.join(target_dir, 'file1.txt'), 'r') as f:
            self.assertEqual(f.read(), 'Hello, World!')
        with open(os.path.join(target_dir, 'dir1', 'file2.txt'), 'r') as f:
            self.assertEqual(f.read(), 'Hello, World!')
        shutil.rmtree(target_dir)

    def test_stow_files_dry_run(self):
        ignore_list = parse_ignore_file(self.ignore_file) + ['.stow-local-ignore']
        files_to_stow = get_files_to_stow(self.temp_dir, ignore_list)
        target_dir = tempfile.mkdtemp()
        stow_files(target_dir, True, files_to_stow)
        self.assertFalse(os.path.exists(os.path.join(target_dir, 'file1.txt')))
        self.assertFalse(os.path.exists(os.path.join(target_dir, 'dir1', 'file2.txt')))
        shutil.rmtree(target_dir)

if __name__ == "__main__":
    unittest.main()