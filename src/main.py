import networkx as nx
import os


class DirReader(object):
    def __init__(self, d_path, header=None, allowed_ext=None):
        if allowed_ext is None:
            allowed_ext = ['.txt']

        if header is None:
            header = ['Names', 'Seq']

        self._d_path = d_path
        self._header = header
        self._allowed_ext = allowed_ext
        self._allowed_seq_syms = set('CGTA')

    def __enter__(self):
        if not os.path.exists(self._d_path):
            return []
        f_paths = []
        for fn in os.listdir(self._d_path):
            p = os.path.join(self._d_path, fn)
            if self._check_file(p):
                f_paths.append(p)

        return [os.path.split(p) for p in f_paths]

    def __exit__(self, exc_ty, exc_val, tb):
        pass

    def _check_file(self, fpath):
        if os.path.splitext(fpath)[1] not in self._allowed_ext:
            return False

        with open(os.path.join(fpath)) as f:
            if f.readline().split() != self._header:
                return False

            for line in f.readlines():
                sp = line.split()
                length = len(sp)
                if length == 1 or length % 2 != 1:
                    return False

                s = set(sp[-1]).difference(self._allowed_seq_syms)
                if len(s) != 0:
                    return False

        return True


class ScienceGraph:
    def __init__(self, d=None):
        self.gr = nx.Graph(d)

    def _read_from_file(self, file_path):
        with open(file_path) as f:
            f.readline()  # for header
            for line in f.readlines():
                words = line.split()
                scientists = []
                for i in range(0, len(words) - 1, 2):
                    first = words[i]
                    second = words[i+1]
                    scientists.append(first + ' ' + second)

                for i in range(len(scientists) - 1):
                    for j in range(i + 1, len(scientists)):
                        self.gr.add_edge(scientists[i], scientists[j])

    def read_dir(self, dir_path):
        with DirReader(dir_path) as file_names:
            for h, t in file_names:
                self._read_from_file(os.path.join(h, t))


def print_iter(res_file='result.txt'):
    def printed_next(self):
        ans = next(self._gen)
        with open(res_file, 'a') as f:
            f.write(str(sorted(ans)) + '\n')
        return ans

    def decorate(cls):
        setattr(cls, '__next__', printed_next)
        return cls

    return decorate


@print_iter()
class GraphIterator(object):
    def __init__(self, gr):
        if isinstance(gr, ScienceGraph):
            self._gen = nx.connected_components(gr.gr)
        elif isinstance(gr, nx.Graph):
            self._gen = nx.connected_components(gr)
        else:
            self._gen = None

    def __next__(self):
        return next(self._gen)

    def __iter__(self):
        return self


if __name__ == '__main__':
    path = "../test/scigraph/case3"
    graph = ScienceGraph()
    graph.read_dir(path)
    for comp in GraphIterator(graph):
        print(comp == {'A a', 'B b', 'C c'})
        print(comp)
