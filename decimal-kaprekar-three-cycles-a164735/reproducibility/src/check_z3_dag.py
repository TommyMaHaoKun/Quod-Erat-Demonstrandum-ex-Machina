"""Independently check a Z3 proof DAG using scoped sequents and cvc5.

No Z3 proof rule is trusted for arithmetic. Every ordinary inference must
pass a small syntactic propositional/equality check or an independent strict cvc5
implication check. Unknown rule names receive that same semantic check;
unknown/timeout results never count as valid. Assertions are read from the
original SMT-LIB file, not trusted from the DAG's assertion list.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import time
import cvc5
from verify_cvc5 import PROOF_OPTIONS, effective_options, inspect_proof, solver_version
from pb_auxiliaries import infer_pb_definitions


ROOT = Path(__file__).resolve().parents[1]


def sexprs(text):
    """Small SMT-LIB expression reader, used only for sort inference."""
    tokens = re.findall(r';[^\n]*|\|[^|]*\||"(?:""|[^"])*"|[^\s()]+|[()]', text)
    stack, roots = [], []
    for token in tokens:
        if token.startswith(';'):
            continue
        if token == '(':
            stack.append([])
        elif token == ')':
            if not stack:
                raise ValueError('Unbalanced SMT-LIB expression.')
            obj = stack.pop()
            (stack[-1] if stack else roots).append(obj)
        else:
            (stack[-1] if stack else roots).append(token)
    if stack:
        raise ValueError('Unbalanced SMT-LIB expression.')
    return roots


def print_sexpr(expr):
    return expr if isinstance(expr, str) else '('+' '.join(map(print_sexpr, expr))+')'


def normalize_definitions(query, dag):
    """Eliminate fresh definitional symbols by global macro substitution.

    Z3's proof-only `~` operator is interpreted as equality and then every
    resulting inference is checked. No intro-def node is accepted as an
    axiom. Its formula must become valid after the fresh substitution.
    """
    original_names = {entry[1] for entry in sexprs(query)
                      if isinstance(entry, list) and entry
                      and entry[0] in ('declare-fun', 'declare-const')}

    def normalize(expr):
        if isinstance(expr, str):
            return expr
        return ['=' if part == '~' else normalize(part) for part in expr]

    def expand_lets(expr, environment=None):
        environment = {} if environment is None else environment
        if isinstance(expr, str):
            return environment.get(expr, expr)
        if expr[0] == 'let':
            bindings = {name: expand_lets(value, environment) for name, value in expr[1]}
            return expand_lets(expr[2], dict(environment, **bindings))
        return [expand_lets(part, environment) for part in expr]

    # Preserve the shared formula table. Parsing every formula into nested
    # Python lists at once can multiply a large certificate's memory usage.
    formulas = [print_sexpr(normalize(sexprs(text)[0])) if '~' in text else text
                for text in dag['formulas']]
    definitions = {}
    for node in dag['nodes']:
        if node['rule'] != 'apply-def' or not node['formula_args']:
            continue
        expression = expand_lets(sexprs(formulas[node['formula_args'][-1]])[0])
        if not isinstance(expression, list) or len(expression) != 3 or expression[0] != '=':
            continue
        left, right = expression[1:]
        for name, value in ((right, left), (left, right)):
            if (isinstance(name, str) and name not in original_names
                    and name not in ('true', 'false') and not re.fullmatch(r'[0-9]+', name)):
                if name in definitions and definitions[name] != value:
                    raise ValueError('Inconsistent candidate fresh definitions for '+name)
                definitions[name] = value
                break

    def atoms(expr):
        if isinstance(expr, str):
            return {expr}
        return set().union(*(atoms(part) for part in expr))

    remaining = dict(definitions)
    ordered = {}
    while remaining:
        ready = [name for name, value in remaining.items()
                 if not atoms(value).intersection(remaining)]
        if not ready:
            raise ValueError('Cyclic fresh definitions cannot be eliminated.')
        for name in ready:
            ordered[name] = print_sexpr(remaining.pop(name))
    return formulas, ordered


def infer_fresh_declarations(original, formula_text, supplied=None):
    """Assign consistent Bool/Int sorts to genuinely fresh proof symbols.

    This does not grant fresh symbols any axioms. Every subsequent inference
    is checked under these declarations, so even an ambiguous sort choice
    cannot turn an invalid derivation into a trusted one.
    """
    known = {}
    for entry in sexprs(original):
        if isinstance(entry, list) and entry and entry[0] == 'declare-fun':
            if entry[2] or entry[3] not in ('Int', 'Bool'):
                raise ValueError('Only nullary Int/Bool input declarations supported.')
            known[entry[1]] = entry[3]
    original_names = set(known)
    if supplied is not None:
        for declaration in supplied:
            entries = sexprs(declaration)
            if len(entries) != 1:
                raise ValueError('Malformed proof declaration.')
            entry = entries[0]
            if (not isinstance(entry, list) or len(entry) != 4
                    or entry[0] != 'declare-fun' or entry[2]
                    or entry[3] not in ('Int', 'Bool')):
                raise ValueError('Unsupported proof declaration.')
            name, sort = entry[1], entry[3]
            if name in known and known[name] != sort:
                raise ValueError('Proof changes an original symbol sort.')
            known[name] = sort
        return {name: known[name] for name in sorted(set(known)-original_names)}
    unresolved = set()

    def visit(expr, expect=None, local=None):
        local = {} if local is None else local
        if isinstance(expr, str):
            if expr in ('true', 'false'):
                got = 'Bool'
            elif re.fullmatch(r'[0-9]+', expr):
                got = 'Int'
            elif expr in local:
                value, outer, cached_sort = local[expr]
                got = cached_sort or visit(value, expect, outer)
                local[expr][2] = got
                if expect is not None and got is not None and got != expect:
                    raise ValueError('Let-bound sort mismatch for '+expr)
                return got
            else:
                got = known.get(expr)
                if got is None:
                    if expect is None:
                        unresolved.add(expr)
                        return None
                    known[expr] = got = expect
            if expect is not None and got != expect:
                raise ValueError('Inconsistent sort for ' + str(expr))
            return got
        if not expr or not isinstance(expr[0], str):
            raise ValueError('Unsupported indexed operator in proof formula.')
        op, args = expr[0], expr[1:]
        if op == 'let':
            extended = dict(local)
            # SMT-LIB let bindings are simultaneous; preserve their outer scope.
            for name, value in args[0]:
                extended[name] = [value, local, visit(value, None, local)]
            return visit(args[1], expect, extended)
        if op == '!':
            return visit(args[0], expect, local)
        if op in ('and', 'or', 'not', '=>', 'xor'):
            for arg in args:
                visit(arg, 'Bool', local)
            got = 'Bool'
        elif op in ('+', '-', '*', 'div', 'mod', 'abs'):
            for arg in args:
                visit(arg, 'Int', local)
            got = 'Int'
        elif op in ('<', '<=', '>', '>='):
            for arg in args:
                visit(arg, 'Int', local)
            got = 'Bool'
        elif op in ('=', 'distinct'):
            sorts = [visit(arg, None, local) for arg in args]
            nonempty = {s for s in sorts if s is not None}
            if len(nonempty) > 1:
                raise ValueError('Mixed-sort equality in proof.')
            inner = next(iter(nonempty)) if nonempty else None
            if inner is not None:
                for arg in args:
                    visit(arg, inner, local)
            got = 'Bool'
        elif op == 'ite':
            visit(args[0], 'Bool', local)
            left = visit(args[1], expect, local)
            right = visit(args[2], expect or left, local)
            got = expect or left or right
            if got is not None:
                visit(args[1], got, local)
                visit(args[2], got, local)
        else:
            raise ValueError('Unsupported proof formula operator: ' + op)
        if expect is not None and got is not None and got != expect:
            raise ValueError('Operator result sort mismatch: ' + op)
        return got

    for _ in range(3):
        for text in formula_text:
            visit(sexprs(text)[0], 'Bool')
    for name in unresolved - set(known):
        known[name] = 'Int'
    for text in formula_text:
        visit(sexprs(text)[0], 'Bool')
    return {name: known[name] for name in sorted(set(known)-original_names)}


class Checker:
    def __init__(self, query, formulas, fresh, timeout, definitions=None, term_dag=None):
        definitions = {} if definitions is None else definitions
        self.tm = cvc5.TermManager()
        self.solver = cvc5.Solver(self.tm)
        self.solver.setLogic('QF_LIA')
        for key, value in dict(PROOF_OPTIONS, incremental='true',
                               **{'tlimit-per': str(timeout)}).items():
            self.solver.setOption(key, value)
        self.parser = cvc5.InputParser(self.solver)
        self.symbols = self.parser.getSymbolManager()
        self.commands(query, original=True)
        self.original_assertions = list(self.solver.getAssertions())
        self.assertions = frozenset(self.original_assertions)
        source_terms, pending = set(), list(self.original_assertions)
        while pending:
            term = pending.pop()
            if term in source_terms:
                continue
            source_terms.add(term)
            pending.extend(term)
        source_constants = {term for term in source_terms
                            if term.getKind() == cvc5.Kind.CONSTANT}
        self.solver.resetAssertions()
        self.commands('\n'.join('(declare-fun %s () %s)' % pair
                                for pair in fresh.items()))
        if term_dag is not None:
            self.formulas, self.term_definitions = self.logical_term_dag(
                term_dag, fresh, source_constants)
            self.stats = Counter()
            self.cache = set()
            return
        self.formulas = []
        for offset in range(0, len(formulas), 1000):
            batch = formulas[offset:offset+1000]
            self.parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,
                                       '\n'.join(batch), 'proof-formulas')
            for _ in batch:
                term = self.parser.nextTerm()
                if term.isNull() or not term.getSort().isBoolean():
                    raise ValueError('Missing or non-Boolean proof formula.')
                self.formulas.append(term)
            if not self.parser.nextTerm().isNull():
                raise ValueError('Unexpected extra formula data.')
        if definitions:
            definition_input = '\n'.join(name+'\n'+value for name, value in definitions.items())
            self.parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,
                                       definition_input, 'fresh-substitution')
            variables, values = [], []
            for name in definitions:
                variable = self.parser.nextTerm()
                value = self.parser.nextTerm()
                if variable in source_constants:
                    raise ValueError('A fresh definition would alter an original input symbol.')
                if variables:
                    value = value.substitute(variables, values)
                variables.append(variable)
                values.append(value)
            self.formulas = [term.substitute(variables, values) for term in self.formulas]
        self.stats = Counter()
        self.cache = set()

    def logical_term_dag(self, dag, fresh, source_constants):
        """Construct a shared, typed logical DAG, with fresh definitions removed.

        Every constructor is an ordinary cvc5 logical/arithmetic operator.
        There are no assertions added by this process. Redirection of a
        fresh constant to its defining expression is uniform substitution.
        """
        terms, roots = dag['terms'], dag['formula_roots']
        names = sorted({record['name'] for record in terms if record['op'] == 'symbol'})
        self.parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,
                                   '\n'.join(names), 'logical-symbols')
        symbols = {name: self.parser.nextTerm() for name in names}
        if any(term.isNull() for term in symbols.values()):
            raise ValueError('Missing logical-term declaration.')
        definitions = infer_pb_definitions(dag, fresh)
        for node in dag['nodes']:
            if node['rule'] != 'apply-def' or not node['formula_args']:
                continue
            equation = terms[roots[node['formula_args'][-1]]]
            if equation['op'] not in ('=', '~') or len(equation['args']) != 2:
                continue
            left, right = equation['args']
            for variable, value in ((right, left), (left, right)):
                record = terms[variable]
                if record['op'] == 'symbol' and record['name'] in fresh:
                    name = record['name']
                    if symbols[name] in source_constants:
                        raise ValueError('Fresh substitution would alter an original input symbol.')
                    if name in definitions and definitions[name] != value:
                        raise ValueError('Inconsistent fresh term-DAG definitions.')
                    definitions[name] = value
                    break
        if any(symbols[name] in source_constants for name in definitions):
            raise ValueError('Fresh substitution would alter an original input symbol.')
        kinds = {
            'and': cvc5.Kind.AND, 'or': cvc5.Kind.OR, 'not': cvc5.Kind.NOT,
            '=>': cvc5.Kind.IMPLIES, 'xor': cvc5.Kind.XOR,
            '=': cvc5.Kind.EQUAL, '~': cvc5.Kind.EQUAL, 'distinct': cvc5.Kind.DISTINCT,
            'ite': cvc5.Kind.ITE, 'if': cvc5.Kind.ITE,
            '+': cvc5.Kind.ADD, '*': cvc5.Kind.MULT,
            '<=': cvc5.Kind.LEQ, '>=': cvc5.Kind.GEQ,
            '<': cvc5.Kind.LT, '>': cvc5.Kind.GT,
            'div': cvc5.Kind.INTS_DIVISION, 'mod': cvc5.Kind.INTS_MODULUS,
            'abs': cvc5.Kind.ABS,
        }
        built = [None]*len(terms)
        active = set()
        for root in roots:
            pending = [(root, False)]
            while pending:
                index, finishing = pending.pop()
                if not isinstance(index, int) or not 0 <= index < len(terms):
                    raise ValueError('Invalid logical-term reference.')
                if built[index] is not None:
                    continue
                record = terms[index]
                if record['sort'] not in ('Bool', 'Int'):
                    raise ValueError('Unsupported logical-term sort: '+record['sort'])
                redirect = definitions.get(record.get('name')) if record['op'] == 'symbol' else None
                children = [redirect] if redirect is not None else record['args']
                if not finishing:
                    if index in active:
                        raise ValueError('Cyclic logical terms or fresh definitions.')
                    active.add(index)
                    pending.append((index, True))
                    pending.extend((child, False) for child in reversed(children))
                    continue
                active.remove(index)
                args = [built[child] for child in children]
                op = record['op']
                if redirect is not None:
                    result = args[0]
                elif op == 'symbol':
                    if args:
                        raise ValueError('Only nullary logical symbols are supported.')
                    result = symbols[record['name']]
                elif op == 'numeral':
                    if args or record['sort'] != 'Int':
                        raise ValueError('Only integer numeral leaves are supported.')
                    result = self.tm.mkInteger(record['value'])
                elif op in ('true', 'false'):
                    if args:
                        raise ValueError('Boolean constants cannot have arguments.')
                    result = self.tm.mkBoolean(op == 'true')
                elif op == '-':
                    if not args:
                        raise ValueError('Empty subtraction.')
                    result = self.tm.mkTerm(cvc5.Kind.NEG, args[0]) if len(args) == 1 else args[0]
                    for arg in args[1:]:
                        result = self.tm.mkTerm(cvc5.Kind.SUB, result, arg)
                elif op in ('pbeq', 'pbge', 'at-least'):
                    parameters = record.get('params')
                    expected = 1 if op == 'at-least' else len(args)+1
                    if (not isinstance(parameters, list) or len(parameters) != expected
                            or any(type(value) is not int for value in parameters)
                            or any(not arg.getSort().isBoolean() for arg in args)):
                        raise ValueError('Missing or malformed pseudo-Boolean parameters.')
                    bound = parameters[0]
                    weights = [1]*len(args) if op == 'at-least' else parameters[1:]
                    summands = [self.tm.mkTerm(cvc5.Kind.ITE, arg,
                                              self.tm.mkInteger(str(weight)), self.tm.mkInteger(0))
                                for arg, weight in zip(args, weights)]
                    if not summands:
                        total = self.tm.mkInteger(0)
                    elif len(summands) == 1:
                        total = summands[0]
                    else:
                        total = self.tm.mkTerm(cvc5.Kind.ADD, *summands)
                    relation = cvc5.Kind.EQUAL if op == 'pbeq' else cvc5.Kind.GEQ
                    result = self.tm.mkTerm(relation, total, self.tm.mkInteger(str(bound)))
                elif op in kinds:
                    if op in ('+', '*', 'and', 'or') and len(args) == 1:
                        result = args[0]
                    else:
                        result = self.tm.mkTerm(kinds[op], *args)
                else:
                    raise ValueError('Unsupported logical-term operator: '+op)
                actual_sort = 'Bool' if result.getSort().isBoolean() else (
                    'Int' if result.getSort().isInteger() else 'unsupported')
                if actual_sort != record['sort']:
                    raise ValueError('Logical-term sort does not match its constructor.')
                built[index] = result
        formulas = [built[root] for root in roots]
        if any(not formula.getSort().isBoolean() for formula in formulas):
            raise ValueError('A proof formula is not Boolean.')
        return formulas, definitions

    def commands(self, data, original=False):
        self.parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6, data, 'input')
        while True:
            cmd = self.parser.nextCommand()
            if cmd.isNull():
                break
            name = cmd.getCommandName()
            if name in ('check-sat', 'set-info'):
                continue
            if name == 'set-logic':
                continue  # Logic was fixed before parsing any declarations.
            if name not in ('declare-fun', 'declare-const', 'assert'):
                raise ValueError('Unexpected input command: ' + name)
            if name == 'assert' and not original:
                raise ValueError('Fresh declarations must not add assertions.')
            cmd.invoke(self.solver, self.symbols)

    def neg(self, term):
        return self.tm.mkTerm(cvc5.Kind.NOT, term)

    @staticmethod
    def literal(term):
        polarity = True
        while term.getKind() == cvc5.Kind.NOT:
            polarity = not polarity
            term = term[0]
        if term.isBooleanValue():
            return (polarity == term.getBooleanValue(), 0)
        return polarity, term.getId()+1

    def clause(self, term):
        pending, out = [term], set()
        while pending:
            item = pending.pop()
            if item.getKind() == cvc5.Kind.OR:
                pending.extend(item)
            else:
                literal = self.literal(item)
                if literal != (False, 0):
                    out.add(literal)
        return frozenset(out)

    @staticmethod
    def false(term):
        return term.isBooleanValue() and not term.getBooleanValue()

    def local_implication(self, premises, conclusion):
        key = (frozenset(premises), conclusion)
        if key in self.cache:
            self.stats['cached_semantic_steps'] += 1
            return
        # No input assertion is present in this solver. Only this inference's
        # premise conclusions and the negated conclusion are assumed.
        # cvc5 exposes the previous checkSatAssuming assumptions through
        # getAssertions until the next check/reset; clear them explicitly.
        self.solver.resetAssertions()
        if self.solver.getAssertions():
            raise ValueError('Unexpected persistent assertion in local checker.')
        result = self.solver.checkSatAssuming(*premises, self.neg(conclusion))
        if not result.isUnsat():
            raise ValueError('Local implication failed: ' + str(result))
        proof = self.solver.getProof()[0]
        proof_statistics = inspect_proof(proof)
        self.stats['local_proof_nodes'] += proof_statistics['unique_nodes']
        self.cache.add(key)
        self.stats['strict_cvc5_steps'] += 1

    def syntactic(self, rule, premises, conclusion):
        if conclusion in premises or any(self.false(p) for p in premises):
            return True
        if conclusion.isBooleanValue() and conclusion.getBooleanValue():
            return True
        if conclusion.getKind() == cvc5.Kind.EQUAL and conclusion[0] == conclusion[1]:
            return True
        literals = self.clause(conclusion)
        if (True, 0) in literals or any((not p, a) in literals for p, a in literals):
            return True
        if rule == 'unit-resolution' and premises:
            remaining = set(self.clause(premises[0]))
            for premise in premises[1:]:
                unit = self.clause(premise)
                if len(unit) != 1:
                    return False
                polarity, atom = next(iter(unit))
                complement = (not polarity, atom)
                if complement not in remaining:
                    return False
                remaining.remove(complement)
            return remaining.issubset(literals)
        if rule in ('mp', 'mp~') and len(premises) == 2:
            for equality, fact in (premises, premises[::-1]):
                if equality.getKind() == cvc5.Kind.EQUAL:
                    if ((equality[0] == fact and equality[1] == conclusion)
                            or (equality[1] == fact and equality[0] == conclusion)):
                        return True
        if (rule in ('trans', 'symm', 'monotonicity')
                and conclusion.getKind() == cvc5.Kind.EQUAL
                and all(p.getKind() == cvc5.Kind.EQUAL for p in premises)):
            parent = {}

            def representative(term):
                key = term.getId()
                parent.setdefault(key, key)
                while parent[key] != key:
                    parent[key] = parent[parent[key]]
                    key = parent[key]
                return key

            for equality in premises:
                parent[representative(equality[0])] = representative(equality[1])

            def congruent(left, right):
                if representative(left) == representative(right):
                    return True
                if (left.getNumChildren() == 0 or left.getNumChildren() != right.getNumChildren()
                        or left.getKind() != right.getKind() or left.getSort() != right.getSort()
                        or not left.hasOp() or not right.hasOp() or left.getOp() != right.getOp()):
                    return False
                return all(congruent(a, b) for a, b in zip(left, right))

            if congruent(conclusion[0], conclusion[1]):
                return True
        if rule == 'and-elim' and len(premises) == 1:
            pending = [premises[0]]
            while pending:
                item = pending.pop()
                if item == conclusion:
                    return True
                if item.getKind() == cvc5.Kind.AND:
                    pending.extend(item)
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dag', type=Path, default=ROOT/'certificates/classification.z3.dag.json.gz')
    ap.add_argument('--query', type=Path, default=ROOT/'certificates/classification.smt2')
    ap.add_argument('--timeout', type=int, default=10000, help='Per local inference, milliseconds.')
    ap.add_argument('--report', type=Path, default=ROOT/'certificates/z3_dag_verification.json')
    ap.add_argument('--bridge-assertions', action='store_true',
                    help='Strictly prove each transformed DAG assertion from its corresponding original assertion.')
    args = ap.parse_args()
    started = time.monotonic()
    query = args.query.read_text(encoding='utf-8')
    with gzip.open(args.dag, 'rt', encoding='utf-8') as stream:
        dag = json.load(stream)
    if dag.get('format') == 'logical-term-dag-v1':
        if 'declarations' not in dag:
            raise ValueError('Shared logical DAG must supply typed symbol declarations.')
        fresh = infer_fresh_declarations(query, [], dag['declarations'])
        checker = Checker(query, [], fresh, args.timeout, term_dag=dag)
        definitions = checker.term_definitions
        del dag['terms'], dag['formula_roots']
    else:
        normalized_formulas, definitions = normalize_definitions(query, dag)
        fresh = infer_fresh_declarations(query, normalized_formulas, dag.get('declarations'))
        checker = Checker(query, normalized_formulas, fresh, args.timeout, definitions)
        # The shared cvc5 term table owns the parsed formulas. Release text.
        del normalized_formulas, dag['formulas']
    embedded_list = [checker.formulas[i] for i in dag['assertions']]
    embedded = frozenset(embedded_list)
    if embedded != checker.assertions:
        if not args.bridge_assertions or len(embedded_list) != len(checker.original_assertions):
            raise ValueError('DAG assertion list does not equal the original input assertions.')
        for original, transformed in zip(checker.original_assertions, embedded_list):
            if original != transformed:
                checker.local_implication([original], transformed)
                checker.stats['assertion_bridges'] += 1
        # These have now each been derived from an original assumption, never
        # assumed solely because they appeared in the proof data.
        checker.assertions = checker.assertions.union(embedded)
    nodes = dag['nodes']
    root = dag['root']
    completed, visiting, order = set(), set(), []
    stack = [(root, False)]
    while stack:
        index, finishing = stack.pop()
        if index in completed:
            continue
        if finishing:
            visiting.remove(index)
            completed.add(index)
            order.append(index)
            continue
        if index in visiting:
            raise ValueError('Cycle in proof DAG.')
        if not isinstance(index, int) or not 0 <= index < len(nodes):
            raise ValueError('Invalid proof-node reference.')
        visiting.add(index)
        stack.append((index, True))
        stack.extend((j, False) for j in reversed(nodes[index]['premises']))
    conclusions, assumptions = [None]*len(nodes), [0]*len(nodes)
    hypothesis_bits, literal_hypotheses = {}, {}
    rules = Counter()
    for ordinal, index in enumerate(order):
        node = nodes[index]
        rule = node['rule']
        rules[rule] += 1
        if not node['formula_args']:
            raise ValueError('Proof node has no explicit conclusion: ' + str(index))
        conclusion = checker.formulas[node['formula_args'][-1]]
        premises = [conclusions[j] for j in node['premises']]
        open_hypotheses = 0
        for j in node['premises']:
            open_hypotheses |= assumptions[j]
        if rule == 'asserted':
            if premises or conclusion not in checker.assertions:
                raise ValueError('Untrusted asserted formula at node ' + str(index))
            open_hypotheses = 0
        elif rule == 'hypothesis':
            if premises:
                raise ValueError('Hypothesis unexpectedly has premises.')
            if conclusion not in hypothesis_bits:
                bit = 1 << len(hypothesis_bits)
                hypothesis_bits[conclusion] = bit
                literal = checker.literal(conclusion)
                literal_hypotheses[literal] = literal_hypotheses.get(literal, 0) | bit
            open_hypotheses = hypothesis_bits[conclusion]
        elif rule == 'lemma':
            if len(premises) != 1 or not checker.false(premises[0]):
                raise ValueError('Lemma must discharge a single false derivation.')
            literals = checker.clause(conclusion)
            discharged = 0
            for polarity, atom in literals:
                discharged |= literal_hypotheses.get((not polarity, atom), 0)
            # Each removed h follows syntactically from not(conclusion).
            # All unrecognized assumptions remain open; none are discarded.
            discharged &= open_hypotheses
            open_hypotheses &= ~discharged
            checker.stats['hypotheses_discharged'] += bin(discharged).count('1')
        elif checker.syntactic(rule, premises, conclusion):
            checker.stats['syntactic_steps'] += 1
        else:
            try:
                checker.local_implication(premises, conclusion)
            except Exception as exc:
                raise ValueError('Invalid node %s (%s): %s' % (index, rule, exc)) from exc
        conclusions[index] = conclusion
        assumptions[index] = open_hypotheses
        if (ordinal+1) % 1000 == 0:
            print(json.dumps({'checked': ordinal+1, 'total': len(order),
                              'seconds': time.monotonic()-started,
                              'stats': dict(checker.stats)}), flush=True)
    if not checker.false(conclusions[root]):
        raise ValueError('The root conclusion is not false.')
    if assumptions[root]:
        raise ValueError('The root retains %s open hypotheses.' % bin(assumptions[root]).count('1'))
    report = {'result': 'PASS', 'scope': 'independent scoped proof-DAG verification',
              'proof_nodes_checked': len(order), 'rules': dict(rules),
              'cvc5': solver_version(checker.solver), 'strict_internal_proof_check': True,
              'effective_options': effective_options(checker.solver),
              'fresh_declarations': fresh, 'eliminated_definitions': definitions,
              'stats': dict(checker.stats),
              'query_sha256': hashlib.sha256(args.query.read_bytes()).hexdigest(),
              'dag_sha256': hashlib.sha256(args.dag.read_bytes()).hexdigest(),
              'seconds': time.monotonic()-started}
    args.report.write_text(
        json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
