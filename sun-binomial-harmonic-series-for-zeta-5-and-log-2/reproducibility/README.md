# Reproducibility supplement

Run the commands in the parent README from this directory.

```console
python -m pip install -r requirements.txt
python src/verify.py
python src/independent_gosper_certificate.py
python src/independent_coefficients.py
python src/build_pdf.py
```

The final command rebuilds `output/research_paper.pdf`. The distributed
PDF is `../paper.pdf`. `STATUS.md` records the completed mathematical scope.
