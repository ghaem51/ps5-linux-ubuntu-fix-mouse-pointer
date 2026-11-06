#!/usr/bin/env python3
import tempfile
from pathlib import Path
import unittest
from configure import KEY, apply, transform

class ConfigureTests(unittest.TestCase):
    def test_preserves_other_settings_and_collapses_duplicates(self):
        original = '# keep this\nPATH=/example/bin\n'+KEY+'=0\n  '+KEY+' = 1\nOTHER=value\n'
        result = transform(original, True)
        self.assertEqual(result, '# keep this\nPATH=/example/bin\nOTHER=value\n'+KEY+'=1\n')
        self.assertEqual(transform(result, True), result)

    def test_remove_preserves_commented_entry(self):
        original = '# '+KEY+'=1\nOTHER=value\n'+KEY+'=1\n'
        self.assertEqual(transform(original, False), '# '+KEY+'=1\nOTHER=value\n')

    def test_file_edit_backup_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/'environment'
            target.write_text('OTHER=value\n'); target.chmod(0o640)
            self.assertTrue(apply(target, True))
            backups = list(Path(directory).glob('*.bak'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'OTHER=value\n')
            self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)
            self.assertEqual(target.stat().st_mode & 0o777, 0o640)
            self.assertFalse(apply(target, True))
            self.assertEqual(len(list(Path(directory).glob('*.bak'))), 1)
            self.assertTrue(apply(target, False))
            self.assertEqual(target.read_text(), 'OTHER=value\n')

    def test_symlink_refused_without_touching_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/'real'; target.write_text('OTHER=value\n')
            link = Path(directory)/'link'; link.symlink_to(target)
            with self.assertRaises(SystemExit): apply(link, True)
            self.assertEqual(target.read_text(), 'OTHER=value\n')

if __name__ == '__main__':
    unittest.main()
