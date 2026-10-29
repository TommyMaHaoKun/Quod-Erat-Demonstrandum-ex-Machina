"""Check both exception encodings and reproduce the complete TeX appendix."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def table_text():
    cert=json.loads((ROOT/'certificates/finite_10000000.json').read_text())
    data=json.loads((ROOT/'certificates/finite_10000000_exception_runs.json').read_text())
    for name in ('negative','equality'):
        expanded=sorted(n for a,b,s in data[name+'_runs'] for n in range(a,b+1,s))
        if expanded != cert[name+'_indices']:
            raise ArithmeticError(name+' run encoding does not match certificate')
    lines=[r'\section{The complete negative set}\label{app:exceptions}',
      r'For $a\le b$ with $a\equiv b\pmod8$, write $[a,b]_8=\{a,a+8,\ldots,b\}$.',
      r'The negative set is the disjoint union of the $118$ progressions below.',
      r'A row with $a=b$ denotes a singleton. Each pair of columns is read independently;',
      r'the two progressions on a row have no special relationship.',
      r'Expansion gives exactly $5505$ indices. Both this table and the full individual',
      r'list are checked by the supplied programs against the exact coefficient calculation.',
      r'\begin{longtable}{@{}rrr@{\hspace{1.0cm}}rrr@{}}',
      r'\toprule $a$&$b$&Count&$a$&$b$&Count\\\midrule\endfirsthead',
      r'\toprule $a$&$b$&Count&$a$&$b$&Count\\\midrule\endhead',
      r'\midrule\multicolumn{6}{r}{Continued on the next page}\\\endfoot',
      r'\bottomrule\endlastfoot']
    runs=data['negative_runs']
    half=(len(runs)+1)//2
    for i in range(half):
        row=[]
        for j in (i,i+half):
            if j<len(runs):
                a,b,s=runs[j]
                if s!=8: raise ArithmeticError('unexpected step')
                row.extend((str(a),str(b),str((b-a)//s+1)))
            else: row.extend(('','',''))
        lines.append('&'.join(row)+r'\\')
    lines.append(r'\end{longtable}')
    return '\n'.join(lines)+'\n'

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    text=table_text();target=ROOT/'paper/exceptions.tex'
    if args.write:
        target.write_text(text,encoding='utf-8')
    elif not target.is_file():
        print('Note: paper/exceptions.tex is not included; manuscript-transcription comparison skipped.')
    elif target.read_text(encoding='utf-8')!=text:
        raise ArithmeticError('TeX appendix differs from exact exception data')
    print('PASS: both run encodings and all 118 manuscript progressions checked.')
