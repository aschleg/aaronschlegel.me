Title: PetfindeR, R Wrapper for the Petfinder API, Introduction Part Two
Date: 2018-05-17
Tags: R, PetfindeR, APIs
Category: R
Slug: petfinder-r-wrapper-petfinder-api-introduction-part-two
Author: Aaron Schlegel
Summary: The first post introduced and explored the basic usage of the PetfindeR library. In this post, we take a quick look at some of the additional uses of the library and its methods to extract data from the Petfinder database.

## Getting Started

The [first post introduced and explored the basic usage of the
`PetfindeR` library](petfinder-r-wrapper-petfinder-api-introduction-part-one.html). 
In this post, we take a quick look at some of the additional uses of the library 
and its methods to extract data from the Petfinder database. Before getting started, 
it is worthwhile to recall the limits imposed by Petfinder when interacting with its API.
The following restrictions are copied from [Petfinder's API
documentation](https://www.petfinder.com/developers/api-docs#restrictions):

-   Total requests per day: 10,000
-   Records per request: 1,000
-   Maximum records per search: 2,000

Therefore, a single call cannot exceed 2,000 records, and there is a
maximum of 1,000 records per request. Knowing this information, we can
construct our calls to the API to extract the maximum amount of
information without exceeding the limitations imposed by Petfinder.

After `PetfindeR` is installed, it can be loaded using the `library()`
function. We initialize the `Petfinder` R6 class object using a key
received from Petfinder. You can easily obtain a key by creating an
account on Petfinder on the [site's developers
page](https://www.petfinder.com/developers/api-key). Once the key is
obtained, we use that as an argument when initializing the class. We can
now begin to extract data from the Petfinder API!

    library(PetfindeR)
    key <- Sys.getenv('PETFINDER_KEY')
    pf <- Petfinder(key)

## Paging Results

The Petfinder API pages results to reduce the stress on the API when
extracting a large number of records. Paging is the only way to exceed
the API's limitation of 1,000 records per request. For example, to get
2,000 animal records located in Washington State (and beyond), we could
set the `count` parameter in the `pet.find` method to 500 and the
`pages` parameter to 4. We could also change the `count` and `pages`
parameters to 1, 000 and 2, respectively, which would achieve the same
result.

    paged <- pf$pet.find(location = 'WA', count = 500, pages = 4, return_df = TRUE)
    paged2 <- pf$pet.find(location = 'WA', count = 1000, pages = 2, return_df = TRUE) # Returns the same as above

The `PetfindeR` library will check to make sure the `count` parameter
doesn't exceed 1,000 to avoid wasting an API call.

    count.too.high <- pf$pet.find(location = 'WA', count = 1001, return_df = TRUE)

    ## Error in check_inputs(animal = animal, size = size, sex = sex, age = age, : a single request cannot exceed 1,000 records

The library will also check to make sure that the input `pages`
parameter and `count` will not exceed 2,000.

    max.record.exceeded <- pf$pet.find(location = 'WA', count = 500, pages = 5, return_df = TRUE)

    ## Error in check_inputs(animal = animal, size = size, sex = sex, age = age, : searches cannot exceed 2,000 records.

## Offsetting Results

Four of the available methods (`pet.find`, `shelter.find`,
`shelter.getPets`, and `shelter.listByBreed`) in the Petfinder API offer
an `offset` parameter which can be used to skip the first *n* results
from the API. Behind the scenes, the `offset` parameter is used to page
results if the `pages` parameter is specified, but it can also be used
to avoid returning the same data when iterating calls. For example, the
below two calls using the `pet.find` method would, in essence, return
the first 100 results should the two results be appended.

    no.offset <- pf$pet.find(location = 'WA', count = 50, return_df = TRUE) # Get the first 50 results
    offsetted <- pf$pet.find(location = 'WA', offset = 50, count = 50, return_df = TRUE) # Skip the first 25 results and get the next 50

The above two calls could also be written as the below.

    paged <- pf$pet.find(location = 'WA', pages = 2, count = 50, return_df = TRUE)
    raw_count <- pf$pet.find(location = 'WA', count = 100, return_df = TRUE)

## Conclusion

This short vignette explored some of the additional functionality of
several of the methods available in the Petfinder API and `PetfindeR`
library for further customizing the number of records and their location
in the database using the `offset` parameter. Future vignettes will also
explore some possible use cases of extracting and analyzing the data
available in the Petfinder database.
