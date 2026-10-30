$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    New-Item -ItemType Directory -Force -Path 'output' | Out-Null
    for ($pass = 1; $pass -le 2; $pass++) {
        & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output paper/main.tex
        if ($LASTEXITCODE -ne 0) { throw "LaTeX pass $pass failed" }
    }
    Copy-Item -LiteralPath 'output/main.pdf' -Destination 'output/research_paper.pdf' -Force
    Write-Output 'Built output/research_paper.pdf'
} finally {
    Pop-Location
}
