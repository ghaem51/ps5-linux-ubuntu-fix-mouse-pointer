# Publication review

The fourth repository was prepared locally without publication. No Bash history, original environment file, backups, credentials, personal home paths or mouse hardware identifiers are distributed. Git authorship uses the public GitHub handle and no-reply email.

The README describes the owner's report that mouse movement causes in-game lag without the setting. It does not claim controlled performance measurements, universal Ubuntu applicability, or invention of the existing Mutter switch. Upstream source and Ubuntu documentation are credited; no third-party code was copied into these scripts.

Four local tests passed, covering environment preservation, duplicate normalization, idempotence, targeted removal, private backups, permission preservation and symlink refusal using temporary files. The verifier confirmed the persistent setting on the local machine; desktop-process environment access was unavailable in the restricted agent session. A new login and physical in-game comparison are still the owner's verification steps. The new editing helper was not run against the real system configuration during repository preparation, since the setting already exists.

This is a limited source/privacy review, not an independent security or legal certification. GitHub Actions has not run. The helper preserves unrelated environment values but changes a system-wide setting, so users should read the documented enable/disable scope.
