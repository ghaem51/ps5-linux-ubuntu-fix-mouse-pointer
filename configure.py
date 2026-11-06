#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Enable/remove the Mutter cursor workaround, preserving other environment keys."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import stat
import tempfile

KEY = 'MUTTER_DEBUG_DISABLE_HW_CURSORS'
ENTRY = re.compile(r'^\s*' + KEY + r'\s*=')

def transform(text, enable):
    lines = [line for line in text.splitlines(keepends=True) if not ENTRY.match(line)]
    result = ''.join(lines)
    if enable:
        if result and not result.endswith(('\n', '\r')):
            result += '\n'
        result += KEY + '=1\n'
    return result

def apply(target, enable):
    if target.is_symlink():
        raise SystemExit('Refusing to replace a symlinked environment file.')
    if target.exists() and not target.is_file():
        raise SystemExit('Environment path is not a regular file.')
    metadata = target.stat() if target.exists() else None
    original = target.read_bytes() if metadata else b''
    updated = transform(original.decode('utf-8', errors='surrogateescape'), enable).encode('utf-8', errors='surrogateescape')
    if updated == original:
        return False
    if metadata:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = target.with_name(target.name + '.before-ps5-mouse-' + stamp + '.bak')
        with backup.open('xb') as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(original)
        print('Backup:', backup)
    descriptor, temporary = tempfile.mkstemp(prefix='.ps5-mouse-', dir=target.parent)
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(updated)
            os.fchmod(handle.fileno(), stat.S_IMODE(metadata.st_mode) if metadata else 0o644)
            if metadata:
                os.fchown(handle.fileno(), metadata.st_uid, metadata.st_gid)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['enable', 'disable'])
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('Run this command with sudo.')
    changed = apply(Path('/etc/environment'), args.action == 'enable')
    print('Configuration updated.' if changed else 'Configuration already matches; no change needed.')
    print('Log out of GNOME and log back in, or reboot, to apply this to a new desktop session.')

if __name__ == '__main__':
    main()
