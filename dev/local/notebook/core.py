#AUTOGENERATED! DO NOT EDIT! File to edit: dev/90_notebook_core.ipynb (unless otherwise specified).

__all__ = ['in_ipython', 'IN_IPYTHON', 'in_colab', 'IN_COLAB', 'in_notebook', 'IN_NOTEBOOK', 'DocsTestClass']

from ..imports import *

def in_ipython():
    "Check if the code is running in the ipython environment (jupyter including)"
    program_name = os.path.basename(os.getenv('_', ''))
    if ('jupyter-notebook' in program_name or # jupyter-notebook
        'ipython'          in program_name or # ipython
        'JPY_PARENT_PID'   in os.environ):    # ipython-notebook
        return True
    else:
        return False

IN_IPYTHON = in_ipython()

def in_colab():
    "Check if the code is running in Google Colaboratory"
    try:
        from google import colab
        return True
    except: return False

IN_COLAB = in_colab()

def in_notebook():
    "Check if the code is running in a jupyter notebook"
    if in_colab(): return True
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell': return True   # Jupyter notebook, Spyder or qtconsole
        elif shell == 'TerminalInteractiveShell': return False  # Terminal running IPython
        else: return False  # Other type (?)
    except NameError: return False      # Probably standard Python interpreter

IN_NOTEBOOK = in_notebook()

class DocsTestClass:
    def test(): pass