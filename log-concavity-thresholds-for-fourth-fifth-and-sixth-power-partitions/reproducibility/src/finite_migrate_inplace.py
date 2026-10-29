"""Idempotently migrate an interrupted two-file checker to one-file storage.

The prefix source remains intact throughout copying. After an exact prefix
comparison and checksum verification, its removal is a separate explicit step.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil

def verify_blocks(path, journal, end):
    reached=0
    with path.open('rb') as f:
        for line in journal.read_text().splitlines():
            start,count,digest=line.split('\t');start=int(start);count=int(count)
            if start>=end:
                break
            if start!=reached or start+count>end:
                raise ArithmeticError('Invalid block coverage')
            data=f.read(16*count)
            if len(data)!=16*count or hashlib.sha256(data).hexdigest()!=digest:
                raise ArithmeticError('Block digest mismatch')
            reached+=count
    if reached!=end:
        raise ArithmeticError('Incomplete block coverage')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('case',type=Path)
    args=parser.parse_args();case=args.case.resolve();old=case/'disk_verify';work=case/'disk_verify_inplace';work.mkdir(exist_ok=True)
    k,bound,mode,stage,next_index,block=(old/'state.txt').read_text().splitlines()
    k,bound,stage,next_index,block=map(int,[k,bound,stage,next_index,block]);total=bound+2
    if mode!='verify' or stage<2:
        raise ValueError('Migration expects an interrupted noninitial verifier coin')
    source=old/('stage_%03d.bin'%stage);previous=old/('stage_%03d.bin'%(stage-1));target=case/'checker_coefficients_u128le.bin'
    if not previous.exists() and target.exists():
        previous=target
    for p in [source,previous,target]:
        if case not in p.resolve().parents:
            raise ValueError('Path escaped case directory')
    marker=work/'migration.json'
    if marker.exists():
        record=json.loads(marker.read_text())
        if record['stage']!=stage or record['next_index']!=next_index:
            raise ArithmeticError('Migration parameters changed')
        inplace_state=work/'state.txt'
        if inplace_state.exists():
            current=inplace_state.read_text().splitlines()
            if list(map(int,current))!=[k,bound,stage,next_index,block]:
                raise ArithmeticError('In-place computation has advanced; refusing to roll it back')
            if record['status']=='copied_verified_ready' and not source.exists():
                print(json.dumps(record,indent=2))
                return
    else:
        verify_blocks(previous,old/('stage_%03d.blocks.tsv'%(stage-1)),total)
        verify_blocks(source,old/('stage_%03d.blocks.tsv'%stage),next_index)
        record={'stage':stage,'next_index':next_index,'block':block,'source':str(source.relative_to(case)),
                'target':'checker_coefficients_u128le.bin','prefix_bytes':16*next_index,
                'status':'copying','reason':'Recover the same exact checkpoint using one coefficient file.'}
        marker.write_text(json.dumps(record,indent=2)+'\n')
    # Overwriting the same target bytes from the unchanged source is idempotent.
    with source.open('rb') as inp,previous.open('r+b') as out:
        remaining=16*next_index
        while remaining:
            data=inp.read(min(4*1024*1024,remaining))
            if not data:
                raise ArithmeticError('Truncated migration prefix')
            out.write(data);remaining-=len(data)
        out.flush();os.fsync(out.fileno())
    verify_blocks(previous,old/('stage_%03d.blocks.tsv'%stage),next_index)
    if previous!=target:
        os.replace(previous,target)
    shutil.copyfile(old/('stage_%03d.blocks.tsv'%(stage-1)),work/('stage_%03d.blocks.tsv'%(stage-1)))
    shutil.copyfile(old/('stage_%03d.blocks.tsv'%stage),work/('stage_%03d.blocks.tsv'%stage))
    (work/'state.txt').write_text('\n'.join(map(str,[k,bound,stage,next_index,block]))+'\n')
    record['status']='copied_verified_ready';marker.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':
    main()
