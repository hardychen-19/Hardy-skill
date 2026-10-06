#!/usr/bin/env python3
"""Persist generated personal character references outside the installed skill."""
import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

THEMES = ('soft-3d', 'ink-notes', 'watercolor', 'midnight-tech')


def default_root():
    if os.name == 'nt':
        return Path(os.environ.get('APPDATA', str(Path.home() / 'AppData/Roaming'))) / 'hardy-skill/illustrations'
    return Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'hardy-skill/illustrations'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root):
    p = root / 'profile.json'
    if not p.is_file():
        raise ValueError('No personal character profile. Ask for one photo to initialize it.')
    result = json.loads(p.read_text(encoding='utf-8'))
    if result.get('schema_version') != 1 or result.get('active_theme') not in THEMES:
        raise ValueError('Unsupported character profile format or theme.')
    for key, checksum in (('reference_path', 'reference_sha256'), ('identity_notes_path', 'identity_notes_sha256')):
        relative = Path(result[key])
        target = (root / relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(root) or not target.is_file():
            raise ValueError('Missing or invalid personal character file: ' + str(target))
        if digest(target) != result[checksum]:
            raise ValueError('Personal character checksum mismatch: ' + str(target))
    return result


def write_profile(root, value):
    root.mkdir(parents=True, exist_ok=True)
    profile = root / 'profile.json'
    if profile.exists():
        old = profile.read_bytes()
        history = root / 'profile-history'
        history.mkdir(exist_ok=True)
        (history / (hashlib.sha256(old).hexdigest() + '.json')).write_bytes(old)
    temporary = root / 'profile.json.tmp'
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(profile)


def run(args):
    root = Path(args.profile_dir).expanduser().resolve() if args.profile_dir else default_root().resolve()
    installed = Path(__file__).resolve().parents[1]
    if root == installed or root.is_relative_to(installed):
        raise ValueError('Personal profiles must be stored outside the installed skill directory.')
    if args.command == 'save':
        reference = Path(args.reference).expanduser().resolve()
        notes = Path(args.identity_notes).expanduser().resolve()
        if not reference.is_file() or not notes.is_file():
            raise ValueError('Generated reference and identity notes must exist before saving.')
        data = reference.read_bytes()
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            suffix = '.png'
        elif data.startswith(b'\xff\xd8\xff'):
            suffix = '.jpg'
        elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            suffix = '.webp'
        else:
            raise ValueError('Generated reference must be a PNG, JPEG or WebP image.')
        if not notes.read_text(encoding='utf-8').strip():
            raise ValueError('Identity notes must not be empty.')
        rh, nh = digest(reference), digest(notes)
        directory = root / 'characters' / (rh[:12] + '-' + nh[:12])
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / ('reference' + suffix)
        note_target = directory / 'identity.md'
        for source, destination in ((reference, target), (notes, note_target)):
            if source != destination:
                shutil.copyfile(source, destination)
        value = dict(schema_version=1, created_at=datetime.now(timezone.utc).isoformat(),
                     reference_path=str(target.relative_to(root)), reference_sha256=rh,
                     identity_notes_path=str(note_target.relative_to(root)), identity_notes_sha256=nh,
                     active_theme=args.theme, status='ready', user_approved=False)
        write_profile(root, value)
    elif args.command == 'set-theme':
        value = load(root)
        value['active_theme'] = args.theme
        write_profile(root, value)
    result = load(root)
    for key in ('reference_path', 'identity_notes_path'):
        result[key] = str(root / result[key])
    result['profile_path'] = str(root / 'profile.json')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile-dir', help='Optional personal profile directory (not the installed skill).')
    commands = parser.add_subparsers(dest='command', required=True)
    save = commands.add_parser('save', help='Save an actual generated character and its identity notes.')
    save.add_argument('--reference', required=True)
    save.add_argument('--identity-notes', required=True)
    save.add_argument('--theme', choices=THEMES, default='soft-3d')
    commands.add_parser('resolve', help='Resolve and check existing character files.')
    theme = commands.add_parser('set-theme', help='Remember a visual theme without changing identity.')
    theme.add_argument('--theme', choices=THEMES, required=True)
    try:
        print(json.dumps(run(parser.parse_args()), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
