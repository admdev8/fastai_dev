#AUTOGENERATED! DO NOT EDIT! File to edit: dev/06_vision_core.ipynb (unless otherwise specified).

__all__ = ['Image', 'Imagify', 'image_convert', 'ImageConverter', 'image_resize', 'ImageResizer', 'image2byte',
           'unpermute_image', 'ImageToByteTensor']

from ..imports import *
from ..test import *
from ..core import *
from ..data.pipeline import *
from ..data.core import *
from ..data.external import *

from PIL import Image

class Imagify(Transform):
    "Open an `Image` from path `fn`, show with `cmap` and `alpha`"
    def __init__(self, func=Image.open, cmap=None, alpha=1.): self.func,self.cmap,self.alpha = func,cmap,alpha
    def encodes(self, fn): return Image.open(fn)
    def shows(self, im, ctx=None, figsize=None, cmap=None, alpha=None):
        return show_image(im, ax=ctx, figsize=figsize,
                          cmap=ifnone(cmap,self.cmap),
                          alpha=ifnone(alpha,self.alpha))

def image_convert(img, mode='RGB'):
    "Convert `img` to `mode`"
    return img.convert(mode)

def ImageConverter(mode='RGB'): return partialler(image_convert, mode=mode)

def image_resize(img, size, resample=Image.BILINEAR):
    "Resize image to `size` using `resample"
    return img.resize(size, resample=resample)
image_resize.order=10

class ImageResizer(MappedTransform):
    "Resize image to `size` using `resample"
    def __init__(self, size, resample=Image.BILINEAR, mask=None, mapped=None):
        super().__init__(mask, mapped)
        if not is_listy(size): size=(size,size)
        self.size,self.resample = size,resample

    def _encode_one(self, o): return image_resize(o, size=self.size, resample=self.resample)

def image2byte(img):
    "Transform image to byte tensor in `c*h*w` dim order."
    res = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
    w,h = img.size
    return res.view(h,w,-1).permute(2,0,1)

def unpermute_image(img):
    "Convert `c*h*w` dim order to `h*w*c` (or just `h*w` if 1 channel)"
    return img[0] if img.shape[0] == 1 else img.permute(1,2,0)

class ImageToByteTensor(MappedTransform):
    "Transform image to byte tensor in `c*h*w` dim order."
    order=15
    def _encode_one(self, o): return image2byte(o)
    def _decode_one(self, o): return unpermute_image(o)