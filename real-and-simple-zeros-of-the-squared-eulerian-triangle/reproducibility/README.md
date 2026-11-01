# Exact verification supplement

Run `python src/verify_all.py` with Python 3.9 or later and no third-party packages. Do not use `-O`.

The entry point runs nine mandatory exact checks. Finite sign certificates cover every row through n=250; the other checks certify the rational constants in the uniform analytic proof. The source-to-claim map is Appendix A of the paper and PROOF_MAP.md. The complete clean-run output is verification.log.

The three source subdirectories group the scalar estimates by their derivation. All needed helper modules are included. No network connection, root-finding package or computer algebra system is needed.
