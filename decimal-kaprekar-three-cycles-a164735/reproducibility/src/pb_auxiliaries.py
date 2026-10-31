"""Suggest uniform substitutions for Z3's fresh pseudo-Boolean aliases.

The suggestions are not trusted axioms. Every affected proof inference must
still be checked after substitution, against the unchanged original query.
"""


def infer_pb_definitions(dag, fresh):
    """Return fresh Bool name -> existing term index, with no fresh RHS symbols.

The actual certificate names aliases in equality tautologies of the form
``not (v = P) or not v or P`` or ``not (v = P) or v or not P``.
These clauses alone do not assert ``v = P``. We use their shape only to guess
the substitution ``v := P``; independent checking of the whole substituted
proof supplies the justification. No assumptions are introduced here.
"""
    terms, roots = dag['terms'], dag['formula_roots']
    definitions = {}

    def literal(index):
        record = terms[index]
        if record['op'] == 'not' and len(record['args']) == 1:
            return False, record['args'][0]
        return True, index

    for node in dag['nodes']:
        if (node['rule'] != 'def-axiom' or node['premises']
                or len(node['formula_args']) != 1):
            continue
        clause = terms[roots[node['formula_args'][0]]]
        if clause['op'] != 'or' or len(clause['args']) != 3:
            continue
        literals = {literal(index) for index in clause['args']}
        for polarity, equality_index in literals:
            equality = terms[equality_index]
            if polarity or equality['op'] != '=' or len(equality['args']) != 2:
                continue
            left, right = equality['args']
            for variable, value in ((left, right), (right, left)):
                record = terms[variable]
                if (record['op'] != 'symbol' or record['sort'] != 'Bool'
                        or not record['name'].startswith('pb!')
                        or fresh.get(record['name']) != 'Bool'
                        or terms[value]['sort'] != 'Bool'):
                    continue
                remainder = literals - {(False, equality_index)}
                if remainder not in ({(False, variable), (True, value)},
                                      {(True, variable), (False, value)}):
                    continue
                pending, seen = [value], set()
                while pending:
                    index = pending.pop()
                    if index in seen:
                        continue
                    seen.add(index)
                    part = terms[index]
                    if part['op'] == 'symbol' and part['name'] in fresh:
                        raise ValueError('PB alias candidate depends on a fresh symbol.')
                    pending.extend(part['args'])
                name = record['name']
                if name in definitions and definitions[name] != value:
                    raise ValueError('Inconsistent PB alias candidate: ' + name)
                definitions[name] = value
    return dict(sorted(definitions.items()))
