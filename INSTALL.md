# Safe installation (development branch only)

1. Open the `technovation-2027` branch of `glebmediannikov/altrisk-academy`.
2. Upload `learning_assessment.py`, `question_bank.py`, and `TECHNOVATION_DEVLOG.md` to the repository root.
3. Upload `tests/test_learning_assessment.py` into the existing `tests/` directory.
4. Do not upload `INSTALL.md` unless you want to retain these instructions.
5. Run from the repository root: `python -m unittest discover -s tests -p 'test_learning_assessment.py' -v`.
6. Review questions and code before integration. No edits to `app.py` are included; existing deployment behavior remains unchanged.

This is a prototype with six questions per form, not a completed 12-question validated study. It does not store individual student results.
