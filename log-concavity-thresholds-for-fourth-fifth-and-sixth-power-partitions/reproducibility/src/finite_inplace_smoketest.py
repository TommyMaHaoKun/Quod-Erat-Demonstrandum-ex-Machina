"""Small reproducible test of one-file recurrence and both recovery branches."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    directory = Path(tempfile.mkdtemp(prefix='finite_inplace_test_', dir=str(ROOT/'certificates')))
    compiler = Path(os.environ.get('WINDIR', 'C:/Windows'))/'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
    executable = directory/'finite_inplace.exe'
    source = ROOT/'src/finite_inplace.cs'
    subprocess.run([str(compiler), '/nologo', '/optimize+', '/checked-', '/platform:x64', '/out:'+str(executable), str(source)], check=True)
    bound, block = 10000, 777
    command = [str(executable), '4', str(bound), str(directory), str(block)]

    def execute(stop=0, expected=0):
        result = subprocess.run(command+[str(stop)], capture_output=True, text=True)
        if result.returncode != expected:
            raise ArithmeticError(result.stdout+'\n'+result.stderr)
        return result

    execute(14, 3)  # First block of the second (noninitial) coin.
    work = directory/'disk_verify_inplace'
    data = directory/'checker_coefficients_u128le.bin'
    state = list(map(int, (work/'state.txt').read_text().splitlines()))
    stage, start = state[2:4]
    if stage != 2 or start != block:
        raise ArithmeticError('Unexpected test checkpoint')
    with data.open('r+b') as f:
        f.seek(16*start)
        original = f.read(16*block)
        damaged = bytes([original[0]^1])+original[1:]
        f.seek(16*start)
        f.write(damaged)
    digest = lambda b: hashlib.sha256(b).hexdigest()
    (work/'undo.bin').write_bytes(original)
    (work/'intent.txt').write_text('\n'.join(map(str, [stage,start,block,digest(original),digest(damaged)]))+'\n')
    with (work/('stage_%03d.blocks.tsv'%stage)).open('a') as f:
        f.write('%d\t%d\t%s\n'%(start,block,digest(damaged)))
    execute(1, 3)  # Must undo the uncommitted write before recomputing.
    with data.open('rb') as f:
        f.seek(16*start)
        committed = f.read(16*block)
    (work/'undo.bin').write_bytes(original)
    (work/'intent.txt').write_text('\n'.join(map(str, [stage,start,block,digest(original),digest(committed)]))+'\n')
    execute(1, 3)  # A committed intent must retain the new data.
    with data.open('r+b') as f:
        saved = f.read(1)
        f.seek(0)
        f.write(bytes([saved[0]^1]))
    rejected = execute(expected=1)
    if 'checksum mismatch' not in rejected.stderr:
        raise ArithmeticError('Corruption failed for an unexpected reason')
    with data.open('r+b') as f:
        f.write(saved)
    execute()
    counts = [1]+[0]*(bound+1)
    j = 1
    while j**4 <= bound+1:
        coin = j**4
        for n in range(coin, bound+2):
            counts[n] += counts[n-coin]
        j += 1
    if data.read_bytes() != b''.join(n.to_bytes(16, 'little') for n in counts):
        raise ArithmeticError('Recovered coefficients differ from Python arbitrary precision')
    report = {
        'result': 'PASS', 'k': 4, 'coefficient_range': [0,bound+1],
        'checks': ['resume a noninitial coin', 'restore an uncommitted write from undo',
                   'retain a committed write with an outstanding intent',
                   'reject corrupt committed data', 'all coefficients equal independent Python arbitrary precision'],
        'inplace_source_sha256': digest(source.read_bytes()),
        'test_source_sha256': digest(Path(__file__).read_bytes()),
        'test_directory': directory.name,
    }
    (ROOT/'certificates/finite_inplace_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: one-file recurrence and minimal recovery tests; certificates/finite_inplace_validation.json')


if __name__ == '__main__':
    main()
