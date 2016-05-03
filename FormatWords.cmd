if "%1%" == "" (
    FormatWords.py "source.html" > result.txt
) else (
    FormatWords.py %1% > result.txt
)
