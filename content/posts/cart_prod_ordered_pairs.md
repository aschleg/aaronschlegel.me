Title: Cartesian Product and Ordered and Unordered Pairs
Date: 2018-01-26
Tags: R, set theory
Category: R
Slug: cartestian-product-ordered-unordered-pairs
Author: Aaron Schlegel
Summary: A pair set is a set with two members, for example, {2, 3}, which can also be thought of as an unordered pair, in that {2, 3}={3, 2}. However, we seek a more a strict and rich object that tells us more about two sets and how their elements are ordered.

Ordered and Unordered Pairs
---------------------------

A pair set is a set with two members, for example, ${2, 3}$, which can
also be thought of as an unordered pair, in that ${2, 3}={3, 2}$. However,
we seek a more a strict and rich object that tells us more about two
sets and how their elements are ordered. Call this object ⟨2, 3⟩, which
specifies that 2 is the first component and 3 is the second component.
We also make the requirement that ⟨2, 3⟩≠⟨3, 2⟩. We can also represent
this object, generalized as ⟨$x$, $y$⟩, as:

$$ \large{\langle x, y\rangle = \langle u, v \rangle} $$

Therefore $x = u$ and $y = v$. This property is useful in the formal
definition of an ordered pair, which is stated here but not explored
in-depth. The currently accepted definition of an ordered pair was given
by Kuratowski in 1921 (Enderton, 1977, pp. 36), though there exist
several other definitions.

$$ \large{\langle x, y \rangle = \big\{\{x\}, \{x, y\} \big\}} $$

The pair ⟨$x, y$⟩ can be represented as a point on a Cartesian
coordinate plane.

Cartesian Product
-----------------

The Cartesian product $A × B$ of two sets $A$ and $B$ is the
collection of all ordered pairs ⟨$x, y$⟩ with $x ∈ A$ and $y ∈ B$.
Therefore, the Cartesian product of two sets is a set itself consisting
of ordered pair members. A set of ordered pairs is defined as a
'relation.'

For example, consider the sets $A = {1, 2, 3}$ and $B = {2, 4, 6}$. The
Cartesian product $A × B$ is then:

$$ A × B = {{1, 2},{1, 4},{1, 6},{2, 2},{2, 4},{2, 6},{3, 2},{3, 4},{3, 6}} $$

Whereas the Cartesian product $B × A$ is:

$$ B × A = {{2, 1},{2, 2},{2, 3},{4, 1},{4, 2},{4, 3},{6, 1},{6, 2},{6, 3}} $$

The following function implements computing the Cartesian product of two
sets $A$ and $B$.

    cartesian <- function(a, b) {
      axb <- list()
      k <- 1
      for (i in a) {
        for (j in b) {
          axb[[k]] <- c(i,j)
          k <- k + 1
        }
      }
      return(axb)
    }

Let's use the function to calculate the Cartesian product $A × B$ and
$B × A$ to see if it aligns with our results above.

    a <- c(1,2,3)
    b <- c(2,4,6)

    as.data.frame(cartesian(a, b))

    ##   c.1..2. c.1..4. c.1..6. c.2..2. c.2..4. c.2..6. c.3..2. c.3..4. c.3..6.
    ## 1       1       1       1       2       2       2       3       3       3
    ## 2       2       4       6       2       4       6       2       4       6

    as.data.frame(cartesian(b, a))

    ##   c.2..1. c.2..2. c.2..3. c.4..1. c.4..2. c.4..3. c.6..1. c.6..2. c.6..3.
    ## 1       2       2       2       4       4       4       6       6       6
    ## 2       1       2       3       1       2       3       1       2       3

Both outputs agree to our previous results. One could also simply use
the `expand.grid()` function like so to get the same result for the
Cartesian product.

    t(expand.grid(a, b))

    ##      [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9]
    ## Var1    1    2    3    1    2    3    1    2    3
    ## Var2    2    2    2    4    4    4    6    6    6

Some Cartesian Product Theorems
-------------------------------

We can state some theorems related to the Cartesian product of two sets.
The first theorem states:

If $A$ is a set, then $A × ⌀ = ⌀$ and $⌀ × A = ⌀$.

We can demonstrate this theorem with our `cartesian()` function.

    cartesian(a, c()) # c() represents the empty set.

    ## list()

    cartesian(c(), a)

    ## list()

The outputs are an empty list which is equivalent to the empty set ⌀ for
our purposes of demonstration.

The next theorem involves three sets $A$, $B$, $C$.

-   $A × (B ∩ C)=(A × B)∩(A × C)$
-   $A × (B ∪ C)=(A × B)∪(A × C)$
-   $(A ∩ B) × C = (A × C) ∩ (B × C)$
-   $(A ∪ B) × C = (A × C) ∪ (B × C)$

We can demonstrate each in turn with a combination of our `cartesian()`
from above, and the `set.union()` and `set.intersection()` functions
from a previous post on set unions and
intersections. The base R functions `union()`
and `intersect()` can be used instead of the functions we defined
previously.

    a <- c(1,2,3)
    b <- c(2,4,6)
    c <- c(1,4,7)

The first identity $A × (B ∩ C) = (A × B) ∩ (A × C)%.

    ident1.rhs <- cartesian(a, set.intersection(b, c)) # Right-hand Side
    ident1.lhs <- set.intersection(cartesian(a, b), cartesian(a, c)) # Left-hand Side

    isequalset(ident1.rhs, ident1.lhs)

    ## [1] TRUE

    as.data.frame(ident1.rhs)

    ##   c.1..4. c.2..4. c.3..4.
    ## 1       1       2       3
    ## 2       4       4       4

    as.data.frame(ident1.lhs)

    ##   c.1..4. c.2..4. c.3..4.
    ## 1       1       2       3
    ## 2       4       4       4

The second identity $A × (B ∪ C)=(A × B) ∪ (A × C)$.

    ident2.rhs <- cartesian(a, set.union(b, c))
    ident2.lhs <- set.union(cartesian(a, b), cartesian(a, c))

    isequalset(ident2.rhs, ident2.lhs)

    ## [1] TRUE

    as.data.frame(ident2.rhs)

    ##   c.1..2. c.1..4. c.1..6. c.1..1. c.1..7. c.2..2. c.2..4. c.2..6. c.2..1.
    ## 1       1       1       1       1       1       2       2       2       2
    ## 2       2       4       6       1       7       2       4       6       1
    ##   c.2..7. c.3..2. c.3..4. c.3..6. c.3..1. c.3..7.
    ## 1       2       3       3       3       3       3
    ## 2       7       2       4       6       1       7

    as.data.frame(ident2.lhs)

    ##   c.1..2. c.1..4. c.1..6. c.2..2. c.2..4. c.2..6. c.3..2. c.3..4. c.3..6.
    ## 1       1       1       1       2       2       2       3       3       3
    ## 2       2       4       6       2       4       6       2       4       6
    ##   c.1..1. c.1..7. c.2..1. c.2..7. c.3..1. c.3..7.
    ## 1       1       1       2       2       3       3
    ## 2       1       7       1       7       1       7

The third identity $(A ∩ B) × C = (A × C) ∩ (B × C)$.

    ident3.rhs <- cartesian(set.intersection(a, b), c)
    ident3.lhs <- set.intersection(cartesian(a, c), cartesian(b, c))

    isequalset(ident3.rhs, ident3.lhs)

    ## [1] TRUE

    as.data.frame(ident3.rhs)

    ##   c.2..1. c.2..4. c.2..7.
    ## 1       2       2       2
    ## 2       1       4       7

    as.data.frame(ident3.lhs)

    ##   c.2..1. c.2..4. c.2..7.
    ## 1       2       2       2
    ## 2       1       4       7

We finish the post with the fourth identity
$(A ∪ B) × C = (A × C) ∪ (B × C)$.

    ident4.rhs <- cartesian(set.union(a,b), c)
    ident4.lhs <- set.union(cartesian(a,c), cartesian(b,c))

    isequalset(ident4.rhs, ident4.lhs)

    ## [1] TRUE

    as.data.frame(ident4.rhs)

    ##   c.1..1. c.1..4. c.1..7. c.2..1. c.2..4. c.2..7. c.3..1. c.3..4. c.3..7.
    ## 1       1       1       1       2       2       2       3       3       3
    ## 2       1       4       7       1       4       7       1       4       7
    ##   c.4..1. c.4..4. c.4..7. c.6..1. c.6..4. c.6..7.
    ## 1       4       4       4       6       6       6
    ## 2       1       4       7       1       4       7

    as.data.frame(ident4.lhs)

    ##   c.1..1. c.1..4. c.1..7. c.2..1. c.2..4. c.2..7. c.3..1. c.3..4. c.3..7.
    ## 1       1       1       1       2       2       2       3       3       3
    ## 2       1       4       7       1       4       7       1       4       7
    ##   c.4..1. c.4..4. c.4..7. c.6..1. c.6..4. c.6..7.
    ## 1       4       4       4       6       6       6
    ## 2       1       4       7       1       4       7

References
----------

Enderton, H. (1977). Elements of set theory (1st ed.). New York:
Academic Press.

MacGillivray, G. Cartesian Products and Relations. Victoria, BC.
Retrieved from <http://www.math.uvic.ca/faculty/gmacgill/guide/RF.pdf>

Stacho, Juraj (n.d.). Cartesian Product [PowerPoint slides]. Retrieved
from <http://www.cs.toronto.edu/~stacho/macm101.pdf>
