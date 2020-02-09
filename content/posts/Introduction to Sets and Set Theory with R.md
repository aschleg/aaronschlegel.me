Title: Introduction to Sets and Set Theory with R
Date: 2018-01-01
Tags: R, set theory
Category: R
Slug: set-theory-r
Author: Aaron Schlegel
Summary: Sets define a 'collection' of objects, or things typically referred to as 'elements' or 'members.' The concept of sets arises naturally when dealing with any collection of objects, whether it be a group of numbers or anything else.

Sets define a 'collection' of objects, or things typically referred to
as 'elements' or 'members.' The concept of sets arises naturally when
dealing with any collection of objects, whether it be a group of numbers
or anything else. Conceptually, the following examples can be defined as
a 'set':

-   {1, 2, 3, 4}
-   {Red, Green, Blue}
-   {Cat, Dog}

The first example is the set of the first four natural numbers. The
second defines a set of the primary colors while the third example
denotes a set of common household pets.

Since its development beginning in the 1870s with Georg Cantor and
Richard Dedekind, set theory has become a foundational system of
mathematics, and therefore its concepts constantly arise in the study of
mathematics and is also an area of active research today.

This post will introduce some of the basic concepts of set theory,
specifically the Zermelo-Fraenkel axiomatic system (more on that later),
with R code to demonstrate these concepts.

Set Notation
------------

Sets can be defined with lowercase, uppercase, script or Greek letters
(in addition to subscripts and the like). Using several types of letters
helps when dealing with hierarchies. Before diving into set theory, it's
best to define the common notation employed. One benefit of set theory
being ubiquitousness in mathematics is learning its notation also helps
in the understanding of other mathematical concepts.

-   ∀*x* - for every set *x*
-   ∃*x* - there exists such a set *x* that
-   ¬ - not
-   ∧ - and
-   ∨ - or (one or the other or both)
-   ⇒ - implies
-   ⇔ - iff, if and only if.
-   *A* ∪ *B* - union of sets *A* and *B*
-   *A* ∩ *B* - intersection of sets *A* and *B*
-   *x* ∈ *A* - x is an element of a set *A*
-   *x* ∉ *A* - x is not an element of a set *A*

The ⇒ notation for implies can be thought of like an if statement in
that it denotes the relation 'if a then b.'

Set Membership
--------------

Set membership is written similar to:

*x* ∈ *A*

Which can be stated as '*x* is an element of the set *A*.' If *x* is not
a member of *A*, we write:

*x* ∉ *A*

The symbol ∈ to denote set membership originated with Giuseppe Peano
(Enderton, pp. 26).

Which is read '*x* is not an element of the set *A*.' We can write an R
function to implement the concept of set membership. Note there already
exists a function `is.element()` in base R that it is recommended for
practical applications.

    iselement <- function(x, A) {
      if (x %in% A) {
        return(TRUE)
      }
      return(FALSE)
    }

Let's use our simple function to test if there exists some members in
the set, *A* = {3, 5, 7, 11}.

    A <- c(3, 5, 7, 11)
    eles <- c(3, 5, 9, 10, (5 + 6))
    for (i in 1:length(eles)) {
      print(iselement(i, A))
    }

    ## [1] FALSE
    ## [1] FALSE
    ## [1] TRUE
    ## [1] FALSE
    ## [1] TRUE

Set membership leads into one of the first axioms of set theory under
the Zermelo-Fraenkel system, the Principle of Extensionality.

Principle of Extensionality
---------------------------

The principle of extensionality states if two sets have the same
members, they are equal. The formal definition of the principle of
extensionality can be stated more concisely using the notation given
above:

∀*A*∀*B*(∀*x*(*x* ∈ *A* ⇔ *x* ∈ *B*)⇒*A* = *B*)

Stated less concisely but still using set notation:

If two sets *A* and *B* are such that for every element (member) *x*:

*x* ∈ *A*  *i**f**f*  *x* ∈ *B*
 Then *A* = *B*.

We can express this axiom through an R function to test for set
equality. Base R also has a function `setequal()` that performs the same
operation.

    isequalset <- function(a, b) {
      
      a <- unique(a)
      b <- unique(b)
      
      an <- length(a)
      
      if (an != length(b)) {
        return(FALSE)
      }
      
      for (i in 1:an) {
        if (!(a[i]) %in% b) {
          return(FALSE)
        }
      }
      
      return(TRUE)
    }

We can now put the principle of extensionality in action with our R
function!

    # original set A to compare
    A <- c(3, 5, 7, 11)

    # define some sets to test for equality
    B <- c(5, 7, 11, 3)
    C <- c(3, 4, 6, 5)
    D <- c(3, 5, 7, 11, 13)
    E <- c(11, 7, 5, 3)
    G <- c(3, 5, 5, 7, 7, 11)

    # collect sets into a list to iterate
    sets <- list(B, C, D, E, G)

    # using the isequalset() function, print the results of the equality tests.
    for (i in sets) {
      print(isequalset(i, A))
    }

    ## [1] TRUE
    ## [1] FALSE
    ## [1] FALSE
    ## [1] TRUE
    ## [1] TRUE

Empty Sets and Singletons
-------------------------

So far we have only investigated sets with two or more members. The
empty set, denoted ⌀, is defined as a set containing no elements and
occurs surprisingly frequently in set-theoretic operations despite is
seemingly straightforward and simple nature.

The empty set axiom, states the existence of an empty set concisely:

∃*B*∀*x*  *x* ∉ *B*
 Which can also be stated as 'there is a set having no members.'

A set ⌀ can be formed whose only member is ⌀. It is important to note
⌀ ≠ ⌀ because ⌀ ∈ ⌀ but ⌀ ∉ ⌀. One can conceptually think of ⌀ as a
container with nothing in it.

A singleton is a set with exactly one element, denoted typically by *a*.
A nonempty set is, therefore, a set with one or more element. Thus a
singleton is also nonempty. We can define another quick function to test
if a given set is empty, a singleton or a nonempty set.

    typeofset <- function(a) {
      if (length(a) == 0) {
        return('empty set')
      }
      
      else if (length(a) == 1) {
        return('singleton')
      }
      
      else if (length(a) > 1) {
        return('nonempty set')
      }
      
      else {
        stop('could not determine type of set')
      }
    }

    A <- c()
    B <- c(0)
    C <- c(1, 2)
    D <- list(c())

    set_types <- list(A, B, C, D)

    for (i in set_types) {
      print(typeofset(i))
    }

    ## [1] "empty set"
    ## [1] "singleton"
    ## [1] "nonempty set"
    ## [1] "singleton"

Note *D* is defined as a singleton because the set contains one element,
the empty set ⌀.

Summary
-------

This post introduced some of the basic concepts of axiomatic set theory
using the Zermelo-Fraenkel axioms by exploring the idea of set, set
membership and some particular cases of sets such as the empty set and
singletons. Set notation that will be used throughout not just
set-theoretic applications but throughout mathematics was also
introduced.

References
----------

Barile, Margherita. "Singleton Set." From MathWorld--A Wolfram Web
Resource, created by Eric W. Weisstein.
<http://mathworld.wolfram.com/SingletonSet.html>

[Enderton, H. (1977). Elements of set theory (1st ed.). New York:
Academic Press.](https://amzn.to/2SsiA5g)

Weisstein, Eric W. "Empty Set." From MathWorld--A Wolfram Web Resource.
<http://mathworld.wolfram.com/EmptySet.html>

Weisstein, Eric W. "Nonempty Set." From MathWorld--A Wolfram Web
Resource. <http://mathworld.wolfram.com/NonemptySet.html>
