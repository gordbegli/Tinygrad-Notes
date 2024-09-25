import os
import numpy as np
import matplotlib.pyplot as plt
from tinygrad import Tensor, dtypes


with open('data/names.txt', 'r') as f:
    words = f.read().splitlines()
Tensor.manual_seed(42)

chars = sorted(list(set(''.join(words))))
stoi = {s:i+1 for i,s in enumerate(chars)}
stoi['.'] = 0
itos = {i:s for s,i in stoi.items()}

xs = []
ys = []

for w in words[:1]:
    chs = ['.'] + list(w) + ['.']
    for ch1, ch2 in zip(chs, chs[1:]):
        ix1 = stoi[ch1]
        ix2 = stoi[ch2]
        xs.append(ix1)
        ys.append(ix2)

xs = Tensor(xs)
ys = Tensor(ys)
num = len(xs)
W = Tensor.randn((27, 27), requires_grad=True)

# Add this after initializing W
g = Tensor.manual_seed(2147483647)

for k in range(1):
    xenc = xs.one_hot(27).float()
    logits = xenc @ W 
    counts = logits.exp() #Formatting
    probs = counts / counts.sum(1, keepdim=True)

    loss = -probs[Tensor.arange(num), ys].log().mean() + 0.01 * (W**2).mean() # fancy indexing
    print(loss.numpy())
    W.grad = None
    loss.backward()

    W = W - (0.1 * W.grad) #This is slow as hell. Tinygrad doesn't support in place operations, but the real way is to use an optimizer anyway to run things?
