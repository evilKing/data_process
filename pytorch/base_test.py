#coding:utf-8

from __future__ import print_function
import torch

x = torch.rand(5, 3)
print(x)

import torch
support_cuda = torch.cuda.is_available()
print(support_cuda)

import numpy as np

np_data = np.arange(6).reshape((2, 3))


