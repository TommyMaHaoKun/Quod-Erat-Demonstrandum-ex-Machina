"""Exact coefficient check of the indexing and typo in JIS Conjecture 11.

This verifies identities between printed formulas, not the array-count theorem.
Python standard library only. Coefficients are stored in ascending degree order.
"""
from math import comb
import json

TARGET = [
    [1, 25, 158, 650, 2275, 4680, 4680],
    [16, 198, 1133, 3900, 8125, 9360, 4680],
    [105, 1087, 4922, 12350, 17875, 14040, 4680],
    [496, 4148, 14783, 28600, 31525, 18720, 4680],
    [1759, 12121, 35258, 55250, 49075, 23400, 4680],
]
last = [5052, 19370, 28405, 18720, 4680]
TARGET.append([sum(last[k-j] * [1, 2, 1][j]
                   for j in range(3) if 0 <= k-j < len(last))
               for k in range(7)])
PRINTED_LOW = [
    [20736, 42768, 40788], [20045, 42128, 40692],
    [19712, 42256, 40788], [20493, 42768, 40788],
    [20288, 42128, 40692], [19496, 42256, 40788],
]


def compose(coefficients, offset):
    """Coefficient vector for P(6*m + offset), exactly over Z."""
    result = [0] * len(coefficients)
    for i, coefficient in enumerate(coefficients):
        for j in range(i + 1):
            result[j] += coefficient * comb(i, j) * 6**j * offset**(i-j)
    return result


def main():
    differences = []
    for r in range(6):
        coefficients = PRINTED_LOW[(r-1) % 6] + [23400, 8125, 1560, 130]
        actual = compose(coefficients, r-1)
        difference = [actual[i] - 1296 * TARGET[r][i] for i in range(7)]
        expected = [27 if r == 0 else 0] + [0] * 6
        assert difference == expected, (r, difference)
        differences.append(difference)
        if r == 0:
            coefficients[0] = 19469
        assert compose(coefficients, r-1) == [1296 * c for c in TARGET[r]]
    result = {
        'status': 'PASS',
        'identity': 'printed_B(n-1)-target_a(n) = 1/48 if n%6==0, else 0',
        'coefficient_differences_with_denominator_1296': differences,
        'corrected_constant_for_printed_residue_5': 19469,
        'printed_B_at_5_numerator': 16159851,
        'printed_B_at_5_denominator': 1296,
        'target_a_at_6': sum(TARGET[0]),
    }
    assert result['printed_B_at_5_numerator'] == 1296 * result['target_a_at_6'] + 27
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
