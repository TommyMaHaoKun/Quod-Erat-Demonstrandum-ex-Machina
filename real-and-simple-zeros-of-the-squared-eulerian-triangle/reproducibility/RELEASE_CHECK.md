# Release verification

Date: 1 November 2026.

## Mathematical result

Every P_n for n>=1 has a simple zero at 0 and n-1 distinct negative zeros; P_0=1. The root count in Section 7 completes the Eulerian part of the stated conjecture. All proof obligations in PROOF_MAP.md are closed.

## Exact computation

A minimal copy containing twelve Python files and the finite certificate was executed from an unrelated working directory. Python's standard library was sufficient. All nine checks passed, with exit status 0, in 47.7 seconds. The full output is retained in verification.log in the published supplement, and in final_verification.log in the local output directory.

No verifier logic changed after this run; release text files use LF line endings. Exact sign certificates cover every row through n=250; scalar verifiers check the uniform proof constants.

## Typesetting and page review

The eight final source files were copied to an empty build directory and compiled with pdfLaTeX, BibTeX and two further pdfLaTeX passes. After minor endpoint and notation clarifications, two final passes succeeded. The final log contains no warnings, undefined references, duplicate labels or overfull boxes.

The PDF has 26 pages. Every page was rendered at 115 dpi and visually inspected: pages 1-7 by the main reviewer, 8-14, 15-21 and 22-26 by three separate reviewers. After the final text corrections, the PDF was rendered again. Image comparison showed that only pages 3, 13, 19 and 20 changed; all four were inspected again and passed. Correcting the primary-source conjecture number then changed only pages 1 and 26; both were rendered and inspected again, with no layout defects. Text, displayed formulas, tables, references, page numbers and margins are legible and unobstructed.

The title and PDF metadata credit Claude Opus 5.5 and GPT-6 Astra. The abstract and Theorem 1.1 state the same all-n result as the proof. The manuscript contains no drafting history, irrelevant OpenAI references, absolute local paths or unresolved placeholders.

Final PDF SHA-256:

    74b66a67f55121d4e316d1d74c8bb47e691b42b528fdfcbe47fe9b895491a24b
