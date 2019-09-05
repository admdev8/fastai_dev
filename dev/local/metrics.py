#AUTOGENERATED! DO NOT EDIT! File to edit: dev/20_metrics.ipynb (unless otherwise specified).

__all__ = ['AccumMetric', 'skm_to_fastai', 'accuracy', 'error_rate', 'top_k_accuracy', 'APScore', 'BalancedAccuracy',
           'BrierScore', 'CohenKappa', 'F1Score', 'FBeta', 'HammingLoss', 'Jaccard', 'MatthewsCorrCoef', 'Precision',
           'Recall', 'RocAuc', 'Perplexity', 'perplexity', 'accuracy_multi', 'APScoreMulti', 'BrierScoreMulti',
           'F1ScoreMulti', 'FBetaMulti', 'HammingLossMulti', 'JaccardMulti', 'MatthewsCorrCoefMulti', 'PrecisionMulti',
           'RecallMulti', 'RocAucMulti', 'mse', 'rmse', 'mae', 'msle', 'exp_rmspe', 'ExplainedVariance', 'R2Score',
           'foreground_acc', 'Dice', 'JaccardCoeff']

from .torch_basics import *
from .test import *
from .layers import *
from .data.all import *
from .notebook.showdoc import show_doc
from .optimizer import *
from .learner import *
from .callback.progress import *

class AccumMetric(Metric):
    "Stores predictions and targets on CPU in accumulate to perform final calculations with `func`."
    def __init__(self, func, dim_argmax=None, sigmoid=False, thresh=None, to_np=False, invert_arg=False, **kwargs):
        self.func,self.dim_argmax,self.sigmoid,self.thresh = func,dim_argmax,sigmoid,thresh
        self.to_np,self.invert_args,self.kwargs = to_np,invert_arg,kwargs

    def reset(self): self.targs,self.preds = [],[]

    def accumulate(self, learn):
        pred = learn.pred.argmax(dim=self.dim_argmax) if self.dim_argmax else learn.pred
        if self.sigmoid: pred = torch.sigmoid(pred)
        if self.thresh:  pred = (pred >= self.thresh)
        pred,targ = flatten_check(pred, learn.yb)
        self.preds.append(pred)
        self.targs.append(targ)

    @property
    def value(self):
        preds,targs = torch.cat(self.preds),torch.cat(self.targs)
        if self.to_np: preds,targs = preds.numpy(),targs.numpy()
        return self.func(targs, preds, **self.kwargs) if self.invert_args else self.func(preds, targs, **self.kwargs)

def skm_to_fastai(func, is_class=True, thresh=None, axis=-1, sigmoid=None, **kwargs):
    "Convert `func` from sklearn.metrics to a fastai metric"
    dim_argmax = axis if is_class and thresh is None else None
    sigmoid = sigmoid if sigmoid is not None else (is_class and thresh is not None)
    return AccumMetric(func, dim_argmax=dim_argmax, sigmoid=sigmoid, thresh=thresh,
                     to_np=True, invert_arg=True, **kwargs)

def accuracy(inp, targ, axis=-1):
    "Compute accuracy with `targ` when `pred` is bs * n_classes"
    pred,targ = flatten_check(inp.argmax(dim=axis), targ)
    return (pred == targ).float().mean()

def error_rate(inp, targ, axis=-1):
    "1 - `accuracy`"
    return 1 - accuracy(inp, targ, axis=axis)

def top_k_accuracy(inp, targ, k=5, axis=-1):
    "Computes the Top-k accuracy (`targ` is in the top `k` predictions of `inp`)"
    inp = inp.topk(k=k, dim=axis)[1]
    targ = targ.unsqueeze(dim=axis).expand_as(inp)
    return (inp == targ).sum(dim=-1).float().mean()

def APScore(axis=-1, average='macro', pos_label=1, sample_weight=None):
    "Average Precision for single-label classification problems"
    return skm_to_fastai(skm.average_precision_score, axis=axis,
                         average=average, pos_label=pos_label, sample_weight=sample_weight)

def BalancedAccuracy(axis=-1, sample_weight=None, adjusted=False):
    "Balanced Accuracy for single-label binary classification problems"
    return skm_to_fastai(skm.balanced_accuracy_score, axis=axis,
                         sample_weight=sample_weight, adjusted=adjusted)

def BrierScore(axis=-1, sample_weight=None, pos_label=None):
    "Brier score for single-label classification problems"
    return skm_to_fastai(skm.brier_score_loss, axis=axis,
                         sample_weight=sample_weight, pos_label=pos_label)

def CohenKappa(axis=-1, labels=None, weights=None, sample_weight=None):
    "Cohen kappa for single-label classification problems"
    return skm_to_fastai(skm.cohen_kappa_score, axis=axis,
                         sample_weight=sample_weight, pos_label=pos_label)

def F1Score(axis=-1, labels=None, pos_label=1, average='binary', sample_weight=None):
    "F1 score for single-label classification problems"
    return skm_to_fastai(skm.f1_score, axis=axis,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def FBeta(beta, axis=-1, labels=None, pos_label=1, average='binary', sample_weight=None):
    "FBeta score with `beta` for single-label classification problems"
    return skm_to_fastai(skm.fbeta_score, axis=axis,
                beta=beta, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def HammingLoss(axis=-1, labels=None, sample_weight=None):
    "Cohen kappa for single-label classification problems"
    return skm_to_fastai(skm.hamming_loss, axis=axis,
                         labels=labels, sample_weight=sample_weight)

def Jaccard(axis=-1, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Jaccard score for single-label classification problems"
    return skm_to_fastai(skm.jaccard_similarity_score, axis=axis,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def MatthewsCorrCoef(axis=-1, sample_weight=None):
    "Matthews correlation coefficient for single-label binary classification problems"
    return skm_to_fastai(skm.matthews_corrcoef, axis=axis, sample_weight=sample_weight)

def Precision(axis=-1, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Precision for single-label classification problems"
    return skm_to_fastai(skm.precision_score, axis=axis,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def Recall(axis=-1, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Recall for single-label classification problems"
    return skm_to_fastai(skm.recall_score, axis=axis,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def RocAuc(axis=-1, average='macro', sample_weight=None, max_fpr=None):
    "Area Under the Receiver Operating Characteristic Curve for single-label binary classification problems"
    return skm_to_fastai(skm.recall_score, axis=axis,
                         laverage=average, sample_weight=sample_weight, max_fpr=max_fpr)

class Perplexity(AvgLoss):
    "Perplexity (exponential of cross-entropy loss) for Language Models"
    @property
    def value(self): return torch.exp(self.total/self.count) if self.count != 0 else None
    @property
    def name(self):  return "perplexity"

perplexity = Perplexity()

def accuracy_multi(inp, targ, thresh=0.5, sigmoid=True):
    "Compute accuracy when `inp` and `targ` are the same size."
    inp,targ = flatten_check(inp,targ)
    if sigmoid: inp = inp.sigmoid()
    return ((inp>thresh)==targ.bool()).float().mean()

def APScoreMulti(thresh=0.5, sigmoid=True, average='macro', pos_label=1, sample_weight=None):
    "Average Precision for multi-label classification problems"
    return skm_to_fastai(skm.average_precision_score, thresh=thresh, sigmoid=sigmoid,
                         average=average, pos_label=pos_label, sample_weight=sample_weight)

def BrierScoreMulti(thresh=0.5, sigmoid=True, sample_weight=None, pos_label=None):
    "Brier score for multi-label classification problems"
    return skm_to_fastai(skm.brier_score_loss, thresh=thresh, sigmoid=sigmoid,
                         sample_weight=sample_weight, pos_label=pos_label)

def F1ScoreMulti(thresh=0.5, sigmoid=True, labels=None, pos_label=1, average='binary', sample_weight=None):
    "F1 score for multi-label classification problems"
    return skm_to_fastai(skm.f1_score, thresh=thresh, sigmoid=sigmoid,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def FBetaMulti(beta, thresh=0.5, sigmoid=True, labels=None, pos_label=1, average='binary', sample_weight=None):
    "FBeta score with `beta` for multi-label classification problems"
    return skm_to_fastai(skm.fbeta_score, thresh=thresh, sigmoid=sigmoid,
                beta=beta, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def HammingLossMulti(thresh=0.5, sigmoid=True, labels=None, sample_weight=None):
    "Cohen kappa for multi-label classification problems"
    return skm_to_fastai(skm.hamming_loss, thresh=thresh, sigmoid=sigmoid,
                         labels=labels, sample_weight=sample_weight)

def JaccardMulti(thresh=0.5, sigmoid=True, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Jaccard score for multi-label classification problems"
    return skm_to_fastai(skm.jaccard_similarity_score, thresh=thresh, sigmoid=sigmoid,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def MatthewsCorrCoefMulti(thresh=0.5, sigmoid=True, sample_weight=None):
    "Matthews correlation coefficient for multi-label classification problems"
    return skm_to_fastai(skm.matthews_corrcoef, thresh=thresh, sigmoid=sigmoid, sample_weight=sample_weight)

def PrecisionMulti(thresh=0.5, sigmoid=True, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Precision for multi-label classification problems"
    return skm_to_fastai(skm.precision_score, thresh=thresh, sigmoid=sigmoid,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def RecallMulti(thresh=0.5, sigmoid=True, labels=None, pos_label=1, average='binary', sample_weight=None):
    "Recall for multi-label classification problems"
    return skm_to_fastai(skm.recall_score, thresh=thresh, sigmoid=sigmoid,
                         labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)

def RocAucMulti(thresh=0.5, sigmoid=True, average='macro', sample_weight=None, max_fpr=None):
    "Area Under the Receiver Operating Characteristic Curve for multi-label binary classification problems"
    return skm_to_fastai(skm.recall_score, thresh=thresh, sigmoid=sigmoid,
                         laverage=average, sample_weight=sample_weight, max_fpr=max_fpr)

def mse(inp,targ):
    "Mean squared error between `inp` and `targ`."
    return F.mse_loss(*flatten_check(inp,targ))

def _rmse(inp, targ): return torch.sqrt(F.mse_loss(inp, targ))
rmse = AccumMetric(_rmse)
rmse.__doc__ = "Root mean squared error"

def mae(inp,targ):
    "Mean absolute error between `inp` and `targ`."
    inp,targ = flatten_check(inp,targ)
    return torch.abs(inp - targ).mean()

def msle(inp, targ):
    "Mean squared logarithmic error between `inp` and `targ`."
    inp,targ = flatten_check(inp,targ)
    return F.mse_loss(torch.log(1 + inp), torch.log(1 + targ))

def _exp_rmspe(inp,targ):
    inp,targ = torch.exp(inp),torch.exp(targ)
    return torch.sqrt(((targ - inp)/targ).pow(2).mean())
exp_rmspe = AccumMetric(_exp_rmspe)
exp_rmspe.__doc__ = "Root mean square percentage error of the exponential of  predictions and targets"

def ExplainedVariance(sample_weight=None):
    "Explained variance betzeen predictions and targets"
    return skm_to_fastai(skm.explained_variance_score, is_class=False, sample_weight=sample_weight)

def R2Score(sample_weight=None):
    "R2 score betzeen predictions and targets"
    return skm_to_fastai(skm.r2_score, is_class=False, sample_weight=sample_weight)

def foreground_acc(inp, targ, bkg_idx=0, axis=1):
    "Computes non-background accuracy for multiclass segmentation"
    targ = targ.squeeze(1)
    mask = targ != bkg_idx
    return (inp.argmax(dim=axis)[mask]==targ[mask]).float().mean()

class Dice(Metric):
    "Dice coefficient metric for binary target in segmentation"
    def __init__(self, axis=1): self.axis = axis
    def reset(self): self.inter,self.union = 0,0
    def accumulate(self, learn):
        pred,targ = flatten_check(learn.pred.argmax(dim=self.axis), learn.yb)
        self.inter += (pred*targ).float().sum().item()
        self.union += (pred+targ).float().sum().item()

    @property
    def value(self): return 2. * self.inter/self.union if self.union > 0 else None

class JaccardCoeff(Dice):
    "Implemetation of the jaccard coefficient that is lighter in RAM"
    @property
    def value(self): return self.inter/(self.union-self.inter) if self.union > 0 else None