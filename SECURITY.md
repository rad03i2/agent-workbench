# Security Policy

## Supported version

The latest release on `main` receives security fixes.

## Data and trust model

Agent Workbench is local-only and does not make network requests. Workspace JSON can contain task titles and notes, so treat it as potentially sensitive. The default workspace filename is ignored by Git to reduce accidental commits, but the file is **not encrypted**.

The application does not execute task content, shell commands, prompts, or notes. Imported/edited workspace files are validated before normal operations, but users should still keep untrusted files separate from sensitive data.

## Reporting

Please report a vulnerability through GitHub's private vulnerability reporting feature when enabled. Otherwise open a minimal issue that does not include exploit secrets or private user data and request a private channel from the maintainer.
