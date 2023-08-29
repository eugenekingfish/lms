# Computational searches for fractional Calabi-Yau algebras

This repository was created whilst working on my 2023 [LMS URB](https://www.lms.ac.uk/grants/undergraduate-research-bursaries) project: 
Computational searches for fractional Calabi-Yau algebras, supervised by Dr Joseph Grant (UEA).

## Mathematical Motivation

Given $n \geq 3$, we can construct the linear quiver $Q_n$. This is a quiver of the form $$1 \rightarrow 2 \rightarrow \ldots \rightarrow n-1 \rightarrow n,$$
with the vertices naturally labelled by elements of $\mathbb{N}$. By then choosing a field $k$, 
we can use $Q_n$ to form the path algebra $kQ_n$, on which we can introduce relations. A relation is a non-zero path (of length $\geq 2$) which we define to be zero. 
Embedding this property into a path algebra involves forming the quotient algebra $kQ_n / I$, where $I$ is the principal ideal generated by the relations.
***
It is known that, if $I = ()$, then $kQ_n/I$ is fractional Calabi-Yau (fCY) for any $n$. However, less is known when $I$ is generated by other non-trivial relations.
This repository's major goal was to produce code that allows for testing whether $kQ_n/I$ is fCY. This is implemented in two different ways: by testing whether the matrix obtained from the projective resolution has finite order,
and by repeatedly applying the Serre functor until resolved, and hence obtaining the fCY dimension of the path algebra.

## Dependencies
This code has been written and tested for Python 3.10.12, though probably works on other versions. <br> 
NumPy is the only required library.


## Getting Started
The best place to get started is by following the interactive tutorial ``tutorial.ipynb`` (requires Jupyter) in the ``py_src`` directory, or the less-extensive ``tutorial.py`` in the same directory.
