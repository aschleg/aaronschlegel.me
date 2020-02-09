Title: Algebra of Sets with R
Date: 2018-01-25
Tags: R, set theory
Category: R
Slug: set-algebra-r
Author: Aaron Schlegel
Summary: The set operations, union and intersection, the relative complement − and the inclusion relation (subsets) are known as the algebra of sets. The algebra of sets can be used to find many identities related to set relations.

The set operations, union and intersection,
the relative complement − and the inclusion relation (subsets) $\subseteq$ are
known as the algebra of sets. The algebra of sets can be used to find
many identities related to set relations that will be discussed later.
We turn now to introducing the relative complement.

Relative Complement
-------------------

The relative complement of two sets $A$ and $B$ is defined as the
members of $A$ not in $B$ and is denoted $A − B$ (or $A/B$). More
formally, the relative complement of two sets is defined as:

$$ \large{A - B = \{x \in A \space | \space x \notin B \}} $$

Just like the set operations union and intersection, the relative
complement can be visualized using Venn diagrams.

![](figure/set_algebra/rel_comp.png)

The shaded area represents the relative complement $A$ − $B$.

For example, consider the following three sets $A$, $B$, $C$.

-   Let $A$ be the set of all Calico cats
-   Let $B$ be the set of all Manx cats
-   Let $C$ be the set of all male cats

What are the elements of the set $A ∪ (B − C)$? Start with the
relative complement in parentheses, which is the set of all nonmale Manx
cats. It wouldn't be as correct to state $B − C$ is the set of all
female Manx cats as it hasn't been explicitly defined that the cats not
in the set $C$ are female. Then the union of $A$ and this set is,
therefore, the set of all cats who are either Calico or Manx nonmales
(or both).

Determining the elements of the set $(A ∪ B)−C$ proceeds in the same
way. The union of $A$ and $B$ represents the set of all cats who are
Calico or Manx or both. Thus the relative complement of this set $C$ is
then the set of all nonmale cats who are either or both Calico or Manx.

The set $(A − C) ∪ (B − C)$ simplifies to one of the sets discussed
above. The relative complement $A − C$ is the set of all nonmale
Calico cats while $B − C$ is the set of all nonmale Manx cats. The
union of these two sets thus results in the set of all nonmale cats who
are either Calico or Manx, which is the same as the set $(A ∪ B)−C$.

We can define an R function to find the relative complement of two sets.

    relcomp <- function(a, b) {
      
      comp <- vector()
      
      for (i in a) {
        if (i %in% a && !(i %in% b)) {
          comp <- append(comp, i)
        }
      }
      
      return(comp)
    }

Find the relative complements of the sets $A = {1, 2, 3, 4, 5}$ and
$B$ = {1, 3, 5, 7}$.

    a <- c(1,2,3,4,5)
    b <- c(1,3,5,7)

    print(relcomp(a, b))

    ## [1] 2 4

    print(relcomp(b, a))

    ## [1] 7

Set Identities
--------------

Many identities can be formed using the set operations we have explored.

Commutative Laws

$$ \large{A \cup B = B \cup A} $$
$$ \large{A \cap B = B \cap A} $$

We can show this identity using the `isequalset()` and `set.union()`
functions we created in the previous post on union and
intersections.

    a <- c(1,2,3,4,5)
    b <- c(1,3,5,7)

    isequalset(set.union(a, b), set.union(b, a))

    ## [1] TRUE

    isequalset(set.intersection(a, b), set.intersection(b, a))

    ## [1] TRUE

Associative Laws

$$ \large{A \cup (B \cup C) = (A \cup B) \cup C} $$
$$ \large{A \cap (B \cap C) = (A \cap B) \cap C} $$

Create a third set $c$.

    c <- c(2,3,4,6)

Starting with the first associative law
$A ∪ (B ∪ C)=(A ∪ B) ∪ C$

    assoc.rhs <- set.union(a, set.union(b, c)) # Right-hand Side
    assoc.lhs <- set.union(set.union(a, b), c) # Left-hand Side
    print(rbind(assoc.rhs, assoc.lhs))

    ##           [,1] [,2] [,3] [,4] [,5] [,6] [,7]
    ## assoc.rhs    1    2    3    4    5    7    6
    ## assoc.lhs    1    2    3    4    5    7    6

Showing the second associative law, $A ∩ (B ∩ C)=(A ∩ B) ∩ C$

    assoc2.rhs <- set.intersection(a, set.intersection(b, c))
    assoc2.lhs <- set.intersection(set.intersection(a, b), c)
    print(rbind(assoc2.rhs, assoc2.lhs))

    ##            [,1]
    ## assoc2.rhs    3
    ## assoc2.lhs    3

Distributive Laws

$$ \large{A \cap (B \cup C) = (A \cap B) \cup (A \cap C)} $$
$$ \large{A \cup (B \cap C) = (A \cup B) \cap (A \cup C)} $$

starting with the first distributive law,
$A ∩ (B ∪ C)=(A ∩ B) ∪ (A ∩ C)$.

    dist.rhs <- set.intersection(a, set.union(b, c))
    dist.lhs <- set.union(set.intersection(a, b), set.intersection(a, c))
    print(rbind(dist.rhs, dist.lhs))

    ##          [,1] [,2] [,3] [,4] [,5]
    ## dist.rhs    1    2    3    4    5
    ## dist.lhs    1    3    5    2    4

Which are equal sets as member order does not matter when determining
the equality of two sets. The second distributive law,
$A ∪ (B ∩ C)=(A ∪ B)∩(A ∪ C)$ can be demonstrated likewise.

    dist2.rhs <- set.union(a, set.intersection(b, c))
    dist2.lhs <- set.intersection(set.union(a, b), set.union(a, c))
    print(rbind(dist2.rhs, dist2.lhs))

    ##           [,1] [,2] [,3] [,4] [,5]
    ## dist2.rhs    1    2    3    4    5
    ## dist2.lhs    1    2    3    4    5

De Morgan's Laws

$$ \large{C - (A \cup B) = (C - A) \cap (C - B)} $$
$$ \large{C - (A \cap B) = (C - A) \cup (C - B)} $$

We can use the function to find the relative complement of two sets we
wrote earlier to show De Morgan's laws. Starting with the first law,
$C − (A ∪ B)=(C − A) ∩ (C − B)$

    morgan.rhs <- relcomp(c, set.union(a, b))
    morgan.lhs <- set.intersection(relcomp(c, a), relcomp(c, b))
    print(rbind(morgan.rhs, morgan.lhs))

    ##            [,1]
    ## morgan.rhs    6
    ## morgan.lhs    6

The second De Morgan's law, $C − (A ∩ B)=(C − A) ∪ (C − B)$
can be shown similarly.

    morgan2.rhs <- relcomp(c, set.intersection(a, b))
    morgan2.lhs <- set.union(relcomp(c, a), relcomp(c, b))
    print(rbind(morgan2.rhs, morgan2.lhs))

    ##             [,1] [,2] [,3]
    ## morgan2.rhs    2    4    6
    ## morgan2.lhs    6    2    4

De Morgan's laws are often stated without $C$, being understood as a
fixed set. All sets are a subset of some larger set, which can be called
a 'space,' or $S$. If one considers the space to be the set of all real
numbers ℝ, and $A$ and $B$ to be two subsets of $S$ (ℝ), then De
Morgan's laws can be abbreviated as:

$$ \large{-(A \cup B) = - A \cap - B} $$
$$ \large{-(A \cap B) = - A \cup - B} $$

We will close the post by stating some identities with the assumption
$A ⊆ S$

$$ \large{A \cup S = S \qquad A \cap S = A} $$
$$ \large{A \cup - A = S \qquad A \cap - A = \varnothing} $$

Though we cannot directly program the set of all real numbers ℝ as it is
an uncountable set, we can show these identities by using a subset of ℝ
where a set $A$ is a subset of that subset.

Generate the set $A$ as the set of integers from one to ten and $S$, our
simulated set of all real numbers, as the set of integers from one to
100.

    a <- seq.int(10)
    s <- seq.int(100)

Show the first identity: $A ∪ S = S$

    isequalset(set.union(a, s), s)

    ## [1] TRUE

Second identity: $A ∩ S = A$

    isequalset(set.intersection(a, s), a)

    ## [1] TRUE

Third identity: $A ∪ −A = S$

    isequalset(set.union(a, relcomp(s, a)), s)

    ## [1] TRUE

Fourth identity: $A ∩ −A = ⌀$

    set.intersection(a, relcomp(s, a))

    ## logical(0)

References
----------

[Enderton, H. (1977). Elements of set theory (1st ed.). New York:
Academic Press.](https://amzn.to/2SsiA5g)
