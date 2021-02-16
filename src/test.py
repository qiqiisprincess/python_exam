import pytest
from main import DirReader, ScienceGraph, print_iter, GraphIterator
from typing import Any
import os


class Case:
    def __init__(self, fun: str, name: str, path: str, answer: Any):
        self.path = path
        self.name = name
        self.answer = answer
        self.fun = fun

    def __str__(self) -> str:
        return '{}_test_{}'.format(self.fun, self.name)


TEST_CASES_CHECK_F = [
    Case(
        fun='check_file',
        name='base',
        path='test/checkfile/case1_ok.txt',
        answer=True
    ),
    Case(
        fun='check_file',
        name='empty',
        path='test/checkfile/case2_f.txt',
        answer=False
    ),
    Case(
        fun='check_file',
        name='not sequence',
        path='test/checkfile/case3_f.txt',
        answer=False
    ),
    Case(
        fun='check_file',
        name='incorrect header',
        path='test/checkfile/case4_f.txt',
        answer=False
    ),
    Case(
        fun='check_file',
        name='2 lines',
        path='test/checkfile/case5_ok.txt',
        answer=True
    ),
    Case(
        fun='check_file',
        name='incorrect ext',
        path='test/checkfile/case6_f.rtf',
        answer=False
    ),
]


TEST_CASES_SCIENCE_G = [
    Case(
        fun='scigraph',
        name='base',
        path='test/scigraph/case1',
        answer=[{'A a', 'C c', 'B b'}]
    ),
    Case(
        fun='scigraph',
        name='base',
        path='test/scigraph/case2',
        answer=[
            {'C c', 'B b', 'A a'},
            {'G c', 'E b', 'D a'}
        ]
    ),
    Case(
        fun='scigraph',
        name='base',
        path='test/scigraph/case3',
        answer=[
            {'H h', 'D d', 'F f'},
            {'B b', 'A a', 'C c', 'E e', 'G g'}
        ]
    ),
]


@pytest.mark.parametrize('case', TEST_CASES_CHECK_F, ids=str)
def test_check_file(case: Case) -> None:
    dr = DirReader(case.path)
    answer = dr._check_file(case.path)
    assert answer == case.answer


@pytest.mark.parametrize('case', TEST_CASES_SCIENCE_G, ids=str)
def test_scigraph(case: Case) -> None:
    print(os.getcwd())
    graph = ScienceGraph()
    graph.read_dir(case.path)
    answer = []
    for conn in GraphIterator(graph):
        answer.append(conn)

    assert len(answer) == len(case.answer)
    for a in answer:
        assert a in case.answer
    for a in case.answer:
        assert a in answer
