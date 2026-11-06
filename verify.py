#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Show only the workaround setting, never the whole environment."""
import os
from pathlib import Path
from configure import ENTRY, KEY

path = Path('/etc/environment')
lines = path.read_text(errors='replace').splitlines() if path.exists() else []
matches = [line.strip() for line in lines if ENTRY.match(line)]
print('Persistent cursor setting:', ', '.join(matches) if matches else 'absent')
print('Current terminal:', KEY + '=' + os.environ.get(KEY, '<unset>'))
found = False
for process in Path('/proc').iterdir():
    if not process.name.isdigit():
        continue
    try:
        if process.stat().st_uid != os.getuid() or (process/'comm').read_text().strip() != 'gnome-shell':
            continue
        found = True
        entry = next((item for item in (process/'environ').read_bytes().split(b'\0') if item.startswith((KEY+'=').encode())), None)
        print('GNOME Shell:', entry.decode(errors='replace') if entry else KEY+'=<unset>')
    except OSError:
        continue
if not found:
    print('GNOME Shell process unavailable; run as your logged-in desktop user.')
print('A configured value alone does not establish improved game performance; test mouse movement in-game.')
