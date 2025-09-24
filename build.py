from yeastr.bootstrapped import *
from pathlib import Path
import shutil
import sys
sys.path.remove((here := __file__.rsplit('/', 1)[0]))
import build

PN = 'yeastr_test'
PV = '0.0.1'
_dir = Path(here) / 'src' / PN

for pep425 in (f'py{v}-none-any' for v in ('313', '38')):
    for _filepath in (_dir / fname for fname in (
        'macros',
        'macros_test',
        'loops',
        'call2comp',
        'match_game',
        'test_match_game',
    )):
        with open(f'{_filepath}.ypy', 'r') as in_:
            ying = BuildTimeTransformer(in_.read(), pep425, autoimport=True)
            with open(f'{_filepath}.py', 'w') as out:
                out.write(ying.yang(_macros))
    # BUILD

    builder = build.ProjectBuilder('.')
    builder.build('sdist', 'dist')
    shutil.move(f'dist/{PN}-{PV}.tar.gz', f'dist/{PN}-{PV}-{pep425}.tar.gz')
    builder.build('wheel', 'dist')
    shutil.move(f'dist/{PN}-{PV}-py3-none-any.whl', f'dist/{PN}-{PV}-{pep425}.whl')

