import numpy as np
import matplotlib.pyplot as plt
import timeit

# ipython notebook --pylab=inline

#--------------------- numpy
# high performance scientific computing and data analysis
# ndarray - a fast and space-efficient multidimensional array
#         - vectorized arithmetic operations and sophisticated broadcasting capabilities
# mathematical functions for fast operations on arrays (without loops)
# linear algebra, random number generation

#----------------- ndarray basics
# N-dimensional array

# create from data
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data)
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)

arr2.shape # shape of array
arr2.dtype # type of data

#basic operations
arr = np.ones((3,6))
arr + arr
arr * 10
arr * (arr * 5) # NOTE: does not do matrix multiplication

# casting
arr = np.array([1, 2, 3, 4, 5])
float_arr = arr.astype(np.float64)
numeric_strings = np.array(['1.25', '-9.6', '42'], dtype=np.string_)
numeric_strings = numeric_strings.astype(float)

# test casting
arr = np.empty(1000) # uninitialized garbage values
%timeit arr.astype(int)
%timeit [int(n) for n in arr]

list_str = [str(i) for i in range(1000)]
arr_str = np.array(list_str, dtype=np.string_)
%timeit [int(n) for n in list_str]
%timeit arr_str.astype(int)

# array version of range
%timeit np.arange(1000) ** 2
%timeit [x ** 2 for x in range(1000)]

# test with 2d arrays
list_mat = [[1.0 for j in range(100)] for i in range(100)]
arr2d = np.ones((100,100))
%timeit [[i * 5 for i in line] for line in list_mat]
%timeit arr2d * 5
# test adding 2d arrays
%timeit [[i + i for i in line] for line in list_mat]
%timeit arr2d + arr2d

# basic indexing and slicing
arr = np.arange(10)
# array slices are views of the original array - modifications are reflected in the source
arr[5:7] = 12
arr_slice = arr[5:7]; arr_slice[0] = 1234
# slicing 3d
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
arr3d[:1, :1, :2]
# slicing 2d
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
arr2d[:, :1] # column

# boolean indexing
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = randn(7, 4)
data[(names == 'Bob') | (names == 'Will')]
data[names == 'Bob']
data[data < 0] = 0

data = randn(1000,1000)
ldata = data.tolist()
def f(ldata):
    for line in ldata:
        for i in range(len(line)):
            if line[i] < 0: line[i] = 0
%timeit data[data < 0] = 0
%timeit f(ldata)

# fancy indexing
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
arr[1,0]
arr[[1,0]]

# transposing arrays
arr = np.arange(15).reshape((3, 5))
np.dot(arr, arr.T)
np.dot(arr.T, arr)
arr.swapaxes(0,1) # also works for 3d arrays

# universal functions: Fast Element-wise Array Functions
# sqrt square ceil etc.
# add multiply greater greater_equal etc.


#----------------- Data processing with ndarray

# perform data processing tasks as concise array expressions
# avoid writing loops
# replacing loops with array expressions: vectorization
# vectorized operations 1-2 orders of magnitude faster than pure Python implementations

# meshgrid example
points = np.arange(-5, 5, 0.01) # 1000 equally spaced points
xs, ys = np.meshgrid(points, points)
z = np.sqrt(xs ** 2 + ys ** 2)

plt.imshow(z, cmap=plt.cm.gray); plt.colorbar()
plt.title("Image plot of $\sqrt{x^2 + y^2}$ for a grid of values")

# conditional logic 
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])
np.where(cond, xarr, yarr)

arr1 = np.ones(1000)
arr2 = np.ones(1000) * 2
cond = np.random.binomial(1, 0.5, 1000)
%timeit np.where(cond, arr1, arr2)
%timeit [(a1 if c else a2) for a1, a2, c in zip(arr1, arr2, cond)]

arr = randn(100, 100)
np.where(arr > 0, 2, -2)
np.where(arr > 0, 2, arr)

# math and statistics
# aggregations: sum, mean, std (standard deviation), min, max
# other methods: cumsum, cumprod

# use of boolean arrays
arr = randn(100)
(arr > 0).sum() # Number of positive values
(arr > 0).any()
(arr > 0).all()

# sorting
arr = np.arange(100)
np.random.shuffle(arr)
arr.sort()
# sorting ndimension array
np.random.shuffle(arr)
arr = arr.reshape((10, 10))
arr.sort(1)

# set logic: intersect1d, union1d, setdiff1d etc.
data = np.arange(100)
arr1 = data[data % 2 == 0]
arr2 = data[data % 2 == 1]
arr3 = data[data % 3 == 0]
np.intersect1d(arr1, arr3)

#------------------- Linear Algebra

#linear algebra: dot, transpose, inverse and determinant: numpy.linalg (inv, qr)
from numpy.linalg import inv, qr
X = randn(5, 5)
mat = X.T.dot(X)
inv(mat)
result = mat.dot(inv(mat))
# prooving this is I (matricea unitate)
where((result > 1e-10) | (result < -1e-10) , 1, 0)
# QR decomposition
q, r = qr(mat)
np.round(r)

#-------------------- Random number generation
# efficiently generating arrays of sample values of probability distributions:
# normal, binomial, uniform etc.
from random import normalvariate
N = 1000000
%timeit samples = [normalvariate(0, 1) for _ in range(N)]
%timeit samples = np.random.normal(size=N)

# random walks example
import random

def random_walk(nsteps=1000):
    position = 0
    walk = [position]
    for i in range(nsteps):
        step = 1 if random.randint(0, 1) else -1
        position += step
        walk.append(position)
    return walk

def random_walk_np(nsteps=1000):
    draws = np.random.randint(0, 2, size=nsteps)
    steps = np.where(draws > 0, 1, -1)
    walk = steps.cumsum()
    return walk

walk = random_walk_np(1000)
# extract statistics
walk.min()
walk.max()
# first time crossing 10/-10 border
walk.argmax()
(np.abs(walk) >= 10).argmax()

plt.plot(walk)

# multiple random walks at once
def random_walks_np(nwalks=5000, nsteps=1000):
    draws = np.random.randint(0, 2, size=(nwalks, nsteps))
    steps = np.where(draws > 0, 1, -1)
    walk = steps.cumsum(1)
    return walk

walks = random_walks_np()

#---------------- Advanced - ndarray internals
# - pointer to data
# - data type: dtype
# - shape (tuple)
# - strides: the number of bytes to “step” in order to advance one element along a dimension

arr = np.ones((3, 4, 5)
arr.strides # navigtion in memory

# Reshaping - returns a view of the same array but with a different shape
arr = np.arange(8)
arr_view = arr.reshape((4,2)).reshape((2,4))
np.random.shuffle(arr_view)
arr.strides
arr_view.strides

#----------------- Performance tips
# - Convert Python loops and conditional logic to array operations 
#   and boolean array operations
# - Avoid copying data using array views (slicing)
# - Use universal functions
