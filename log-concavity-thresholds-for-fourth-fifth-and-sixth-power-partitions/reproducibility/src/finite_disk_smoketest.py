"""Checks disk recurrence, interrupted suffix recovery, and corrupt-block rejection."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run():
    directory=ROOT/'certificates'/'finite_disk_smoketest'
    if directory.exists():
        raise FileExistsError('Use a fresh test directory; existing test evidence is preserved')
    exe=ROOT/'src'/'finite_disk.exe'
    base=[str(exe)]
    common=['4','100000',str(directory)]
    def execute(args,code=0):
        result=subprocess.run(base+args,capture_output=True,text=True)
        if result.returncode!=code:
            raise ArithmeticError(result.stdout+'\n'+result.stderr)
        return result
    execute(['generate']+common+['7777','14'],3)
    work=directory/'disk_generate'
    state=(work/'state.txt').read_text().splitlines()
    stage=int(state[3]);position=int(state[4])
    with (work/('stage_%03d.bin'%stage)).open('ab') as f:
        f.write(b'uncommitted bytes discarded on restart')
    with (work/('stage_%03d.blocks.tsv'%stage)).open('a') as f:
        f.write('%d\t1\tuncommitted checksum\n'%position)
    execute(['generate']+common+['7777'])
    execute(['verify']+common+['12345','138'],3)
    work=directory/'disk_verify'
    stage=int((work/'state.txt').read_text().splitlines()[3])
    payload=work/('stage_%03d.bin'%stage)
    with payload.open('r+b') as f:
        saved=f.read(1);f.seek(0);f.write(bytes([saved[0]^1]))
    result=execute(['verify']+common+['12345'],1)
    if 'checksum mismatch' not in result.stderr:
        raise ArithmeticError('Corruption was not rejected for the expected reason')
    with payload.open('r+b') as f:
        f.write(saved)
    execute(['verify']+common+['12345'])
    limit=100001;counts=[1]+[0]*limit;j=1
    while j**4<=limit:
        coin=j**4
        for n in range(coin,limit+1):
            counts[n]+=counts[n-coin]
        j+=1
    expected=b''.join(n.to_bytes(16,'little') for n in counts)
    if expected!=(directory/'coefficients_u128le.bin').read_bytes() or expected!=(directory/'checker_coefficients_u128le.bin').read_bytes():
        raise ArithmeticError('Disk results differ from Python arbitrary precision')
    signs=bytes((((counts[n]**2-counts[n-1]*counts[n+1])>0)-((counts[n]**2-counts[n-1]*counts[n+1])<0))%256 for n in range(1,100001))
    if signs!=(directory/'signs_i8.bin').read_bytes():
        raise ArithmeticError('Disk signs differ from Python arbitrary precision')
    report={'result':'PASS','k':4,'coefficient_range':[0,100001],
            'determinant_range':[1,100000],
            'checks':['bytewise coefficients against Python arbitrary precision',
                      'bytewise determinants against Python arbitrary precision',
                      'ascending 64-bit and descending 32-bit limb calculations',
                      'resume during a noninitial coin in both modes',
                      'discard uncommitted data and journal suffix',
                      'reject damaged committed block, restore and resume'],
            'disk_source_sha256':hashlib.sha256((ROOT/'src'/'finite_disk.cs').read_bytes()).hexdigest(),
            'test_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'certificates'/'finite_disk_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    run()
