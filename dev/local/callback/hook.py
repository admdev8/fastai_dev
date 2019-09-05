#AUTOGENERATED! DO NOT EDIT! File to edit: dev/15_callback_hook.ipynb (unless otherwise specified).

__all__ = ['Hook', 'hook_output', 'Hooks', 'hook_outputs', 'has_params', 'HookCallback', 'ActivationStats',
           'total_params', 'layer_info']

from ..torch_basics import *
from ..test import *
from ..layers import *
from ..data.all import *
from ..notebook.showdoc import show_doc
from ..optimizer import *
from ..learner import *

@docs
class Hook():
    "Create a hook on `m` with `hook_func`."
    def __init__(self, m, hook_func, is_forward=True, detach=True, cpu=False):
        self.hook_func,self.detach,self.cpu,self.stored = hook_func,detach,cpu,None
        f = m.register_forward_hook if is_forward else m.register_backward_hook
        self.hook = f(self.hook_fn)
        self.removed = False

    def hook_fn(self, module, input, output):
        "Applies `hook_func` to `module`, `input`, `output`."
        if self.detach: input,output = to_detach(input, cpu=self.cpu),to_detach(output, cpu=self.cpu)
        self.stored = self.hook_func(module, input, output)

    def remove(self):
        "Remove the hook from the model."
        if not self.removed:
            self.hook.remove()
            self.removed=True

    def __enter__(self, *args): return self
    def __exit__(self, *args): self.remove()

    _docs = dict(__enter__="Register the hook",
                 __exit__="Remove the hook")

def _hook_inner(m,i,o): return o if isinstance(o,Tensor) or is_listy(o) else list(o)

def hook_output(module, detach=True, cpu=False, grad=False):
    "Return a `Hook` that stores activations of `module` in `self.stored`"
    return Hook(module, _hook_inner, detach=detach, cpu=cpu, is_forward=not grad)

@docs
class Hooks():
    "Create several hooks on the modules in `ms` with `hook_func`."
    def __init__(self, ms, hook_func, is_forward=True, detach=True, cpu=False):
        self.hooks = [Hook(m, hook_func, is_forward, detach, cpu) for m in ms]

    def __getitem__(self,i): return self.hooks[i]
    def __len__(self):       return len(self.hooks)
    def __iter__(self):      return iter(self.hooks)
    @property
    def stored(self):        return [o.stored for o in self]

    def remove(self):
        "Remove the hooks from the model."
        for h in self.hooks: h.remove()

    def __enter__(self, *args): return self
    def __exit__ (self, *args): self.remove()

    _docs = dict(stored = "The states saved in each hook.",
                 __enter__="Register the hooks",
                 __exit__="Remove the hooks")

def hook_outputs(modules, detach=True, cpu=False, grad=False)->Hooks:
    "Return `Hooks` that store activations of all `modules` in `self.stored`"
    return Hooks(modules, _hook_inner, detach=detach, cpu=cpu, is_forward=not grad)

def has_params(m):
    "Check if `m` has at least one parameter"
    return len(list(m.parameters())) > 0

class HookCallback(Callback):
    "`Callback` that can be used to register hooks on `modules`"
    def __init__(self, hook=None, modules=None, do_remove=True, is_forward=True, detach=True, cpu=False):
        self.modules,self.do_remove = modules,do_remove
        self.is_forward,self.detach,self.cpu = is_forward,detach,cpu
        if hook is not None: setattr(self, 'hook', hook)

    def begin_fit(self):
        "Register the `Hooks` on `self.modules`."
        if not self.modules:
            self.modules = [m for m in flatten_model(self.model) if has_params(m)]
        self.hooks = Hooks(self.modules, self.hook, self.is_forward, self.detach, self.cpu)

    def after_fit(self):
        "Remove the `Hooks`."
        if self.do_remove: self._remove()

    def _remove(self):
        if getattr(self, 'hooks', None): self.hooks.remove()

    def __del__(self): self._remove()

@docs
class ActivationStats(HookCallback):
    "Callback that record the mean and std of activations."

    def begin_fit(self):
        "Initialize stats."
        super().begin_fit()
        self.stats = []

    def hook(self, m, i, o): return o.mean().item(),o.std().item()

    def after_batch(self):
        "Take the stored results and puts it in `self.stats`"
        if self.training: self.stats.append(self.hooks.stored)

    def after_fit(self):
        "Polish the final result."
        self.stats = tensor(self.stats).permute(2,1,0)
        super().after_fit()

    _docs = dict(hook="Take the mean and std of the output")

def total_params(m):
    "Give the number of parameters of a module and if it's trainable or not"
    params = sum([p.numel() for p in m.parameters()])
    trains = [p.requires_grad for p in m.parameters()]
    return params, (False if len(trains)==0 else trains[0])

def layer_info(learn):
    def _track(m, i, o):
        return (m.__class__.__name__,)+total_params(m)+(apply(lambda x:x.shape, o),)
    layers = [m for m in flatten_model(learn.model)]
    xb,_ = learn.data.train_dl.one_batch()
    with Hooks(layers, _track) as h:
        _ = learn.model.eval()(apply(lambda o:o[:1], xb))
        return h.stored

def _print_shapes(o, bs):
    if isinstance(o, torch.Size): return ' x '.join([str(bs)] + [str(t) for t in o[1:]])
    else: return [_print_shapes(x, bs) for x in o]

@patch
def summary(self:Learner):
    "Print a summary of the model, optimizer and loss function."
    infos = layer_info(self)
    xb,_ = self.data.train_dl.one_batch()
    n,bs = 64,find_bs(xb)
    inp_sz = _print_shapes(apply(lambda x:x.shape, xb), bs)
    res = f"{self.model.__class__.__name__} (Input shape: {inp_sz})\n"
    res += "=" * n + "\n"
    res += f"{'Layer (type)':<20} {'Output Shape':<20} {'Param #':<10} {'Trainable':<10}\n"
    res += "=" * n + "\n"
    ps,trn_ps = 0,0
    for typ,np,trn,sz in infos:
        if sz is None: continue
        ps += np
        if trn: trn_ps += np
        res += f"{typ:<20} {_print_shapes(sz, bs):<20} {np:<10,} {str(trn):<10}\n"
        res += "_" * n + "\n"
    res += f"\nTotal params: {ps:,}\n"
    res += f"Total trainable params: {trn_ps:,}\n"
    res += f"Total non-trainable params: {ps - trn_ps:,}\n\n"
    res += f"Optimizer used: {self.opt_func}\nLoss function: {self.loss_func}\n\nCallbacks:\n"
    res += '\n'.join(f"  - {cb}" for cb in sort_by_run(self.cbs))
    return PrettyString(res)