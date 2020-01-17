Title: N-Union and Intersection Set Operations
Date: 2018-01-22
Tags: R, set theory
Category: R
Slug: n-set-union-intersection-r
Author: Aaron Schlegel
Summary: Set unions and intersections can be extended to any number of sets. This post introduces notation to simplify the expression of n-sets and the set union and intersection operations themselves with R.

The union and intersection set operations were introduced in a previous
post using two sets, $a$ and $b$. These set operations can be
generalized to accept any number of sets.

Arbitrary Set Unions Operation
------------------------------

Consider a set of infinitely many sets:

$$ A = \large{\{b_0, b_1, b_2, \cdots \} \large} $$

It would be very tedious and unnecessary to repeat the union statement
repeatedly for any non-trivial amount of sets, for example, the first
few unions would be written as:

$$ \large{b_0 \cup b_1 \cup b_2 \cup b_3 \cup b_4 \cup b_5\large} $$

Thus a more general operation for performing unions is needed. This
operation is denoted by the ⋃ symbol. For example, the set $A$ above and
the desired unions of the member sets can be generalized to the
following using the new notation:

$$ \large{\bigcup A = \bigcup_i b_i} $$

We can then state the following definition: For a set $A$, the union
⋃$A$ of $A$ is defined by:

$$ \large{\bigcup A = \{x \space | \space (\exists b \in A) \space x \in b \} \large} $$

For example, consider the three sets:

$$ \large{a = \{2, 4, 6 \} \qquad b = \{3, 5, 7\} \qquad c = \{2, 3, 8 \} \large}$$
The union of the three sets is written as:

$$ \large{\bigcup \Big\{\{2,4,6\}, \{3,5,7\}, \{2,3,8\} \Big\} = \{2,3,4,5,6,7,8\}} $$

Recalling our union axiom from a previous post, the union axiom states
for two sets $A$ and $B$, there is a set whose members consist entirely
of those belonging to sets $A$ or $B$, or both. More formally, the union
axiom is stated as:

$$ \large{\forall a \space \forall b \space \exists B \space \forall x (x \in B \Leftrightarrow x \in a \space \vee \space x \in b)} $$

As we are now dealing with an arbitrary amount of sets, we need an
updated version of the union axiom to account for the change.

Restating the union axiom:

For any set $A$, there exists a set $B$ whose members are the same
elements of the elements of $A$. Stated more formally:

$$ \large{\forall x \bigg[ x \in B \space \Leftrightarrow \space (\exists b \in A) \space x \in b \bigg] }$$

The definition of ⋃$A$ can be stated as:

$$ \large{x \in \bigcup A \Leftrightarrow (\exists b \in A) \space x \in b} $$

For example, we can demonstrate the updated axiom with the union of four
sets ${a, b, c, d}$:

$$ \large{\bigcup \{a, b, c, d \} = \big\{(\exists B \in A) \space x \in \{a, b, c, d\}\big\} \large}$$

$$ \large{ \bigcup \{a, b, c, d \} = a \cup b \cup c \cup d \large}$$

We can implement the set operation for an arbitrary amount of sets by
expanding upon the function we wrote previously.

    set.unions <- function(a, b, ...) {
      u <- a
      for (i in 1:length(b)) {
        if (!(b[i] %in% u)) {
          u <- append(u, b[i])
        }
      }
      
      s <- list(...)
      
      for (i in s) {
        for (j in i) {
          if (!(j %in% u)) {
            u <- append(u, j)
          }
        }
      }
      return(u)
    }

Perform the set union operation of four sets:

$$ \large{a = \{1,2,3\} \qquad b = \{3,4,5\} \qquad c = \{1,4,6\} \qquad d =\{2,5,7\} \large}$$

    a <- c(1,2,3)
    b <- c(3,4,5)
    c <- c(1,4,6)
    d <- c(2,5,7)

    set.unions(a, b, c, d)

    ## [1] 1 2 3 4 5 6 7

Intersections of an Arbitrary Number of Sets
--------------------------------------------

The intersection set operation can also be generalized to any number of
sets. Consider the previous set containing an infinite number of sets.

$$ \large{A = \{b_0, b_1, b_2, \cdots \}} $$

As before, writing out all the intersections would be tedious and not
elegant. The intersection can instead be written as:

$$ \large{\bigcap A = \bigcap_i b_i} $$

As before in our previous example of set intersections, there is no need
for a separate axiom for intersections, unlike unions. Instead, we can
state the following theorem, for a nonempty set $A$, a set $B$ exists
that such for any element $x$:

$$ \large{x \in B \Leftrightarrow x \in \forall A} $$

Consider the following four sets:

$$ \large{a = \{1,2,3\} \qquad b = \{1,3,5\} \qquad c = \{1,4,5,3\} \qquad d = \{2,6,1,3\}} $$

The intersection of the sets is written as:

$$ \large{\bigcap \big\{\{1,2,3,5\}, \{1,3,5\}, \{1,4,5,3\}, \{2,5,1,3\}\big\}} $$
$$ = \large{\{1,2,3,5\} \cap \{1,3,5\} \cap \{1,4,5,3\} \cap \{2,5,1,3\} = \{1,3,5\}} $$

We can write another function to implement the set intersection
operation given any number of sets.

    set.intersections <- function(a, b, ...) {

      intersect <- vector()
      for (i in a) {
        if (i %in% b) {
          intersect <- append(intersect, i)
        }
      }
      
      s <- list(...)
      
      for (i in s) {
        for (j in i) {
          if (j %in% intersect) {
            intersect <- append(intersect, j)
          }
        }
      }
      intersect <- unique(intersect)
      
      return(intersect)
    }

Perform set intersections of the four sets specified earlier.

    a <- c(1,2,3,5)
    b <- c(1,3,5)
    c <- c(1,4,5,3)
    d <- c(2,5,1,3)

    set.intersections(a, b, c, d)

    ## [1] 1 3 5

References
----------

Enderton, H. (1977). Elements of set theory (1st ed.). New York:
Academic Press.
