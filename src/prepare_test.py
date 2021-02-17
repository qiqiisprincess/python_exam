import os


def create_file(path, content=None):
    h, t = os.path.split(path)
    os.makedirs(h, mode=0o777, exist_ok=True)
    with open(path, 'w') as f:
        if isinstance(content, list):
            f.write('\n'.join(content))
        elif isinstance(content, str):
            f.write(content)


def remove_dir_r(path):
    for r, d, f in os.walk(path):
        print(r, d, f)

    for r, d, f in os.walk(path):
        for file in f:
            os.remove(os.path.join(r, file))

    for r, d, f in os.walk(path):
        for direct in d:
            p = os.path.join(r, direct)
            if len(os.listdir(p)) == 0:
                os.removedirs(p)

    for r, d, f in os.walk(path):
        print(r, d, f)


if __name__ == '__main__':
    print(os.getcwd())
    remove_dir_r('test')
    header = 'Names Seq'

    # test check_file
    create_file('test/checkfile/case1_ok.txt', [header, 'A a B b C c CTAG'])
    create_file('test/checkfile/case2_f.txt', '')
    create_file('test/checkfile/case3_f.txt', [header, 'A a B b C c CTAGDBI'])
    create_file('test/checkfile/case4_f.txt', ['Header Seqth', 'A a B b C c CTAGTT'])
    create_file('test/checkfile/case5_ok.txt',
                [
                    header,
                    'A a B b C c CTCCTAG',
                    'C c D d G g CTTAGG'
                ])
    create_file('test/checkfile/case6_f.rtf', [header, 'A a B b C CTAG'])

    # test science_graph
    create_file('test/scigraph/case1/1.txt', [header, 'A a B b C c CTAG'])

    create_file('test/scigraph/case2/1.txt', [header, 'A a B b C c CCTAGG'])
    create_file('test/scigraph/case2/2.txt', [header, 'D a E b G c CCTAACTGG'])

    create_file('test/scigraph/case3/1.txt', [header, 'A a B b C c CCTAACTGG'])
    create_file('test/scigraph/case3/2.txt', [header, 'A a E e G g CCTAATTGG'])
    create_file('test/scigraph/case3/3.txt', [header, 'D d F f H h CCTAACTGG'])
