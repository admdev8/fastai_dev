
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev/01_test.ipynb

import numpy as np,torch,operator,sys,os
from typing import Iterable, Iterator, Generator, Callable, Sequence, List, Tuple, Union, Optional
from torch import as_tensor,Tensor
from numpy import array,ndarray
from IPython.core.debugger import set_trace
from fastai_local.export import chk,show_doc

from pathlib import Path
import pandas as pd, re, PIL, os, mimetypes, csv, itertools
import matplotlib.pyplot as plt
from collections import OrderedDict
from enum import Enum
from warnings import warn
from functools import partial,reduce

def test_fail(f, msg='', contains=''):
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"
    try:
        f()
        assert False,f"Expected exception but none raised. {msg}"
    except Exception as e: assert not contains or contains in e.args[0]

def test(a, b, cmp,cname=None):
    "`assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails"
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"

def _all_equal(a,b): return len(a)==len(b) and all(equals(a_,b_) for a_,b_ in zip(a,b))

def equals(a,b):
    "Compares `a` and `b` for equality; supports sublists, tensors and arrays too"
    cmp = (torch.equal    if isinstance(a, Tensor  ) else
           np.array_equal if isinstance(a, ndarray ) else
           operator.eq    if isinstance(a, str     ) else
           _all_equal     if isinstance(a, Iterable) else
           operator.eq)
    return cmp(a,b)

def nequals(a,b):
    "Compares `a` and `b` for `not equals`"
    return not equals(a,b)

def test_eq(a,b):
    "`test` that `a==b`"
    test(a,b,equals, '==')

def test_ne(a,b):
    "`test` that `a!=b`"
    test(a,b,nequals,'!=')

def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')