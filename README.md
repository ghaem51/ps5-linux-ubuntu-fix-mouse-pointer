# PS5 Ubuntu mouse-movement game stutter workaround

On the reported PS5 Slim Ubuntu setup, games lag or stutter when the mouse is moved without this workaround. Setting `MUTTER_DEBUG_DISABLE_HW_CURSORS=1` tells GNOME's Mutter compositor to disable hardware cursors and use software cursor rendering instead.

The repository owner reports this workaround for the mouse-movement symptom. No controlled frame-time measurements or comparison across multiple systems have been performed. This is a compositor workaround, not a USB polling change, game patch, or general fix for all Ubuntu performance problems.

## Enable persistently

```bash
sudo python3 configure.py enable
```

This keeps exactly one active `MUTTER_DEBUG_DISABLE_HW_CURSORS=1` entry in `/etc/environment`, preserving other settings. On a change it creates a root-readable backup alongside the file. If the setting is already correct, nothing is rewritten. File ownership and permissions are preserved; symlinked environment files are refused.

**Log out of GNOME and log back in, or reboot.** Exporting the variable in a terminal does not change the environment of an already-running GNOME Shell. Do not restart the display manager just to apply this: doing so ends the desktop session.

`/etc/environment` is a system-wide PAM environment file, so this affects subsequent sessions for all users whose login stack reads it. This project targets Ubuntu GNOME on Wayland; other desktops/compositors may ignore the setting.

## Verify

Run as the logged-in desktop user, without sudo:

```bash
python3 verify.py
```

It prints only the named setting from the configuration, terminal and accessible GNOME Shell process. It does not dump the full environment. Then test the same game and mouse movement. The variable being present does not prove a performance improvement. Software cursors can have different latency/performance characteristics, so keep the setting only if it improves your setup.

## Disable

```bash
sudo python3 configure.py disable
```

Log out and back in again. This removes only active entries for this key, not the whole environment file. Backups can contain other environment values: keep them private and never commit them. The tool preserves unrelated changes instead of blindly restoring an old backup.

## Scope, source and license

- [Mutter's native cursor implementation](https://github.com/GNOME/mutter/blob/main/src/backends/native/meta-cursor-renderer-native.c) checks this variable for the value `1` before initializing hardware cursor support. It is a debug setting and may change in future versions.
- [Ubuntu pam_env documentation](https://manpages.ubuntu.com/manpages/questing/man8/pam_env.8.html) describes `/etc/environment` as simple KEY=VAL entries.
- The variable was found in the owner's existing local configuration; it was not invented by this project. Shell history and the actual environment file are not distributed.

Scripts were developed with OpenAI Codex assistance. GPL-2.0-only applies to this repository's code; no Mutter source is bundled. This is independent community work, not an official Sony, Ubuntu or GNOME release.

## Tests

```bash
python3 -m unittest -v
```

Tests use temporary files, covering unrelated setting preservation, duplicate normalization, repeat runs, removal, private backups, permission preservation, and symlink refusal. They do not write `/etc/environment` or measure game latency.
