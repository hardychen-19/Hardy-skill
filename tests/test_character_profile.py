"""Exercise persistence, reuse, theme switching and damaged-reference behavior."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/hardy-x-illustrations/scripts/character_profile.py'
REFERENCE = ROOT / 'skills/hardy-x-illustrations/assets/themes/photo-character-demo.png'


class ProfileBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.profile = self.root / 'personal'
        self.notes = self.root / 'identity.md'
        self.notes.write_text('Dark hair, glasses, dark jacket; use the visible reference.', encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def call(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), '--profile-dir', str(self.profile), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return json.loads(result.stdout if success else result.stderr)

    def save(self):
        return self.call('save', '--reference', str(REFERENCE), '--identity-notes', str(self.notes))

    def test_initialize_then_reuse_without_source(self):
        original = self.save()
        self.notes.unlink()
        reused = self.call('resolve')
        self.assertEqual(Path(reused['reference_path']).read_bytes(), REFERENCE.read_bytes())
        self.assertEqual(reused['reference_sha256'], original['reference_sha256'])
        self.assertFalse(reused['user_approved'])
        self.assertEqual(reused['status'], 'ready')

    def test_switch_theme_preserves_identity_and_old_profile(self):
        original = self.save()
        for theme in ('ink-notes', 'watercolor', 'midnight-tech'):
            value = self.call('set-theme', '--theme', theme)
            self.assertEqual(value['reference_sha256'], original['reference_sha256'])
            self.assertEqual(value['active_theme'], theme)
        self.assertEqual(len(list((self.profile / 'profile-history').glob('*.json'))), 3)

    def test_missing_profile_and_missing_reference_do_not_fallback(self):
        self.assertIn('one photo', self.call('resolve', success=False)['error'])
        value = self.save()
        Path(value['reference_path']).unlink()
        self.assertIn('Missing', self.call('resolve', success=False)['error'])

    def test_changed_reference_is_rejected(self):
        value = self.save()
        Path(value['reference_path']).write_bytes(b'damaged')
        self.assertIn('checksum', self.call('resolve', success=False)['error'])

    def test_path_escape_is_rejected(self):
        value = self.save()
        file = self.profile / 'profile.json'
        data = json.loads(file.read_text())
        data['reference_path'] = '../outside.png'
        file.write_text(json.dumps(data))
        self.assertIn('invalid', self.call('resolve', success=False)['error'])


if __name__ == '__main__':
    unittest.main()
