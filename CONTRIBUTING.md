# Contributing

Thanks for improving Agent Workbench.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e .`.
3. Run `python -m unittest discover -s tests -v` before submitting changes.
4. Add tests for behavior changes and keep the standard-library-only runtime unless a dependency has a clear benefit.
5. Keep workspace schema changes backward-compatible or include an explicit migration.
6. Never commit real agent transcripts, credentials, tokens, or private workspace files.

Please keep pull requests small, explain the user-visible behavior, and update both README language sections when commands or features change.
