"""Focused corruption checks; no release data is modified."""
from copy import deepcopy
from fractions import Fraction
import json
from seam_inventory import DATA, load_tables, validate_inventory


def main():
    atlas, seams = load_tables()
    rejected = []
    def reject(name, rows):
        try:
            validate_inventory(atlas, rows)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError('Corruption accepted: ' + name)
    rows = deepcopy(seams)
    rows[0]['t'] = str(Fraction(rows[0]['t']) / 2)
    reject('mismatched rational label', rows)
    rows = deepcopy(seams)
    rows[0]['base'] = 9 - rows[0]['base']
    reject('mismatched base label', rows)
    rows = deepcopy(seams)
    rows[0]['c'] += 1
    reject('mismatched parameter pair', rows)
    reject('duplicate record', deepcopy(seams) + [deepcopy(seams[0])])
    rows = deepcopy(seams)
    duplicate = deepcopy(rows[0])
    t = Fraction(duplicate['t'])
    duplicate['t'] = f'{2*t.numerator}/{2*t.denominator}'
    reject('duplicate rational identifier in unreduced notation', rows + [duplicate])
    reject('missing required seam', deepcopy(seams[1:]))
    rows = deepcopy(seams)
    rows[-1] = deepcopy(rows[0])
    reject('duplicate replacing a missing seam', rows)
    result = dict(valid_records=len(seams), corruptions_rejected=rejected)
    (DATA/'seam_negative_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'Accepted {len(seams)} valid seams; rejected all {len(rejected)} corrupt inventories.')


if __name__ == '__main__':
    main()
