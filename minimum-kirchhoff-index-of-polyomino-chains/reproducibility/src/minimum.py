"""Exact minimum Kirchhoff index of an n-cell geometric polyomino chain.

The unique minimizing graph is the staircase zigzag, up to graph isomorphism.
The evaluator uses O(n) integer arithmetic operations and O(n) storage; this
does not claim O(n) bit complexity. Its implementation uses only the standard
library. The accompanying paper supplies the all-n proof.

Examples, from the project directory:
    python src/minimum.py 15
    python src/minimum.py 8 --json --cells
    python src/minimum.py --table 30 --json --output data/formula_values.json
    python src/minimum.py --verify --output data/formula_checks.json
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def _check_n(n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('The number of square cells must be a positive integer.')


def _sequences(n: int) -> tuple[list[int], list[int]]:
    """Return q[0:n+1] and B[0:n]; q[-1] is mathematically zero."""
    q = [1]
    previous = 0
    for _ in range(n):
        previous, current = q[-1], 4*q[-1]-previous
        q.append(current)
    B = [0]+[2*k*q[k]+q[k-1] for k in range(1,n)]
    return q,B


def minimum_kirchhoff(n: int) -> Fraction:
    """Return the exact minimum as a reduced Fraction, for every integer n>=1."""
    _check_n(n)
    q,B = _sequences(n)
    alternating_prefix = 0  # P_(j-1) at iteration j.
    quadratic = 0
    for j in range(1,n-1):
        quadratic += B[n-1-j]*(B[j]-2*alternating_prefix)
        alternating_prefix = B[j]-alternating_prefix
    numerator = (n+1)**2*((n+3)*q[n]-q[n-1])-3*quadratic
    return Fraction(numerator,3*q[n])


def linear_kirchhoff(n: int) -> Fraction:
    """Return the exact Kirchhoff index of the straight n-cell chain."""
    _check_n(n)
    q,_ = _sequences(n)
    return Fraction((n+1)**2*((n+3)*q[n]-q[n-1]),3*q[n])


def zigzag_cells(n: int) -> list[tuple[int,int]]:
    """Lower-left unit-square coordinates, ordered along a minimizing chain."""
    _check_n(n)
    return [((k+1)//2,k//2) for k in range(n)]


def value_record(n: int, include_cells: bool = False) -> dict:
    result = {'n':n,'minimum':str(minimum_kirchhoff(n))}
    if include_cells:
        result['cell_coordinates'] = zigzag_cells(n)
        result['coordinate_meaning'] = 'lower-left corners of unit squares in chain order'
    return result


def verify(project: Path | None = None, recurrence_upto: int = 100) -> dict:
    """Run exact finite checks; these supplement, rather than prove, the theorem."""
    if project is None:
        project = Path(__file__).resolve().parents[1]
    source = project/'data'/'exhaustive_geometric.json'
    exhaustive = json.loads(source.read_text(encoding='utf-8'))['results']
    checked = []
    for row in exhaustive:
        n = row['n']
        assert minimum_kirchhoff(n) == Fraction(row['minimum']), ('minimum',n)
        assert linear_kirchhoff(n) == Fraction(row['maximum']), ('maximum',n)
        checked.append(n)

    # This separately derived edge-attachment calculation uses no q/B/P sum.
    from recurrence_check import INITIAL, extend
    zigzag_state = linear_state = INITIAL
    for n in range(1,recurrence_upto+1):
        if n > 1:
            zigzag_state = extend(zigzag_state, -1 if n % 2 == 0 else 1)
            linear_state = extend(linear_state,0)
        assert minimum_kirchhoff(n) == zigzag_state.K, ('zigzag recurrence',n)
        assert linear_kirchhoff(n) == linear_state.K, ('linear recurrence',n)

    expected_small = {1:Fraction(5),2:Fraction(71,5),3:Fraction(233,8)}
    assert all(minimum_kirchhoff(n) == value for n,value in expected_small.items())
    return {
        'status':'passed',
        'arithmetic':'exact integers and fractions.Fraction; no floating-point comparisons',
        'proof_boundary':'These finite checks validate implementations; the paper proves the theorem for all n.',
        'checks':[
            {
                'name':'formula minima and straight-chain maxima against complete geometric enumeration',
                'source':'data/exhaustive_geometric.json',
                'checked_n':checked,
                'comparisons':2*len(checked),
            },
            {
                'name':'formula minima against independently derived alternating edge-attachment recurrence',
                'source':'src/recurrence_check.py',
                'inclusive_range':[1,recurrence_upto],
                'comparisons':recurrence_upto,
            },
            {
                'name':'straight-chain formula against straight edge-attachment recurrence',
                'source':'src/recurrence_check.py',
                'inclusive_range':[1,recurrence_upto],
                'comparisons':recurrence_upto,
            },
            {
                'name':'exceptional sizes',
                'exact_values':{str(n):str(value) for n,value in expected_small.items()},
                'comparisons':len(expected_small),
            },
        ],
    }


def _positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('expected a positive integer') from exc
    if value < 1:
        raise argparse.ArgumentTypeError('expected a positive integer')
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('n',nargs='?',type=_positive_int,help='number of square cells')
    parser.add_argument('--table',type=_positive_int,metavar='UPTO',help='evaluate every n from 1 through UPTO')
    parser.add_argument('--json',action='store_true',help='emit machine-readable exact values')
    parser.add_argument('--cells',action='store_true',help='include minimizing cell coordinates; requires --json')
    parser.add_argument('--verify',action='store_true',help='run the recorded exact implementation checks')
    parser.add_argument('--output',type=Path,help='save output to this file instead of standard output')
    args = parser.parse_args()
    if sum((args.n is not None,args.table is not None,args.verify)) != 1:
        parser.error('choose exactly one of n, --table UPTO, or --verify')
    if args.cells and (not args.json or args.verify):
        parser.error('--cells requires --json and an n or --table request')

    if args.verify:
        rendered = json.dumps(verify(),indent=2)
    elif args.table is not None:
        records = [value_record(n,args.cells) for n in range(1,args.table+1)]
        if args.json:
            rendered = json.dumps({'arithmetic':'exact rational','results':records},indent=2)
        else:
            rendered = '\n'.join(f"{row['n']}\t{row['minimum']}" for row in records)
    elif args.json:
        rendered = json.dumps(value_record(args.n,args.cells),indent=2)
    else:
        rendered = str(minimum_kirchhoff(args.n))

    if args.output is None:
        print(rendered)
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered+'\n',encoding='utf-8')
        print(f'Saved {args.output}')


if __name__ == '__main__':
    main()
