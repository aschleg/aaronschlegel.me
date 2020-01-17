Title: PetfindeR, R Wrapper for the Petfinder API, Introduction Part One
Date: 2018-05-15
Tags: R, PetfindeR, APIs
Category: R
Slug: petfinder-r-wrapper-petfinder-api-introduction-part-one
Author: Aaron Schlegel
Summary: The goal of the PetfindeR package is to provide a simple and straightforward interface for interacting with the Petfinder API through R. The Petfinder database contains approximately 300,000 adoptable pet records and 11,000 animal welfare organization records, which makes it a handy and valuable source of data for those in the animal welfare community. However, the outputs from the Petfinder API are in messy JSON format and thus it makes it more time-consuming and often frustrating to coerce the output data into a form that is workable with R.

## About PetfindeR

The goal of the `PetfindeR` package is to provide a simple and
straightforward interface for interacting with the [Petfinder
API](https://www.petfinder.com/developers/api-docs) through R. The
Petfinder database contains approximately 300,000 adoptable pet records
and 11,000 animal welfare organization records, which makes it a handy
and valuable source of data for those in the animal welfare community.
However, the outputs from the Petfinder API are in messy JSON format and
thus it makes it more time-consuming and often frustrating to coerce the
output data into a form that is workable with R. The `PetfindeR` package
was developed to alleviate this difficulty and provide users with a
streamlined interface for getting the data they want and using it for
their specific purpose.

## Introduction

This post introduces and walks through the methods available in
`PetfindeR` and the Petfinder API for authenticating and extracting data
from the database.

## Obtaining an API Key from Petfinder

Before we can use the `PetfindeR` package, we need to obtain an API key
from the Petfinder website to authenticate our requests. To acquire an
API key, create an account on [Petfinder's developer
page](https://www.petfinder.com/developers/api-key). A 'secret' key is
also given from Petfinder for requests that require an additional layer
of authentication; however, the current methods available do not need a
secret key to be provided (this could potentially change in the future).

## Getting Started with PetfindeR

At the time of this writing, `PetfindeR` has been submitted to CRAN but 
and is currently in the review process. In the meantime, the package can 
be easily installed through the `devtools` package function `install_github()`.

	devtools::install_github('aschleg/PetfindeR')

After installing and loading the package, The first step in using the
PetfindeR package is to initialize the API connection to Petfinder. To
do this, we pass the API key received from Petfinder into the
`Petfinder` function which calls a wrapped [R6
class](https://cran.r-project.org/package=R6) and creates the connection
to the API.

It is best practice to obfuscate sensitive data such as API keys to
avoid any potential malicious activity. To this effect, I load my API
key by using the `Sys.getenv()` function to access an environment
variable containing the key.

    key <- Sys.getenv('PETFINDER_KEY')

The API key is securely loaded so that we can initialize the PetfindeR
API!

    pf <- Petfinder(key)

That's all there is to it! The [Petfinder API
methods](https://www.petfinder.com/developers/api-docs#methods) are now
accessible through R.

## Examples

The following section introduces the `PetfindeR` package and how to
interact with the Petfinder API with some simple examples of extracting
data from the database. The examples are split into pet and shelter
methods, not due to any significant demarcation, but rather for
organization.

### Pet Methods

<table>
<colgroup>
<col width="16%" />
<col width="15%" />
<col width="68%" />
</colgroup>
<thead>
<tr class="header">
<th>Method</th>
<th>Petfinder API Method</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>breed.list()</td>
<td>breed.list</td>
<td>Returns the available breeds for the selected animal.</td>
</tr>
<tr class="even">
<td>pet.find()</td>
<td>pet.find</td>
<td>Returns a collection of pet records matching input parameters.</td>
</tr>
<tr class="odd">
<td>pet.get()</td>
<td>pet.get</td>
<td>Returns a single record for a pet.</td>
</tr>
<tr class="even">
<td>pet.getRandom()</td>
<td>pet.getRandom</td>
<td>Returns a randomly selected pet record. The possible result can be filtered with input parameters.</td>
</tr>
</tbody>
</table>

### Finding the available breeds of an animal

The `breed.list()` method allows the user to pull a list of breeds
associated with a particular type of animal. The currently available
animals to search for are `'barnyard'`, `'bird'`, `'cat'`, `'dog'`,
`'horse'`, `'reptile'` and `'smallfurry'`. Let's say we are interested
in finding the breeds of cats in the Petfinder database.

    cats <- pf$breed.list('cat')
    cats

    ## $`@encoding`
    ## [1] "iso-8859-1"
    ## 
    ## $`@version`
    ## [1] "1.0"
    ## 
    ## $petfinder
    ## $petfinder$`@xmlns:xsi`
    ## [1] "http://www.w3.org/2001/XMLSchema-instance"
    ## 
    ## $petfinder$breeds
    ## $petfinder$breeds$breed
    ##                                       $t
    ## 1                             Abyssinian
    ## 2                          American Curl
    ## 3                     American Shorthair
    ## 4                      American Wirehair
    ## 5                      Applehead Siamese
    ## 6                               Balinese
    ## 7                                 Bengal
    ## 8                                 Birman
    ## 9                                Bobtail
    ## 10                                Bombay
    ## 11                     British Shorthair
    ## 12                               Burmese
    ## 13                              Burmilla
    ## 14                                Calico
    ## 15                     Canadian Hairless
    ## 16                             Chartreux
    ## 17                               Chausie
    ## 18                            Chinchilla
    ## 19                           Cornish Rex
    ## 20                                Cymric
    ## 21                             Devon Rex
    ## 22                         Dilute Calico
    ## 23                  Dilute Tortoiseshell
    ## 24                    Domestic Long Hair
    ## 25                  Domestic Medium Hair
    ## 26                   Domestic Short Hair
    ## 27                          Egyptian Mau
    ## 28                      Exotic Shorthair
    ## 29 Extra-Toes Cat / Hemingway Polydactyl
    ## 30                                Havana
    ## 31                             Himalayan
    ## 32                      Japanese Bobtail
    ## 33                              Javanese
    ## 34                                 Korat
    ## 35                                LaPerm
    ## 36                            Maine Coon
    ## 37                                  Manx
    ## 38                              Munchkin
    ## 39                              Nebelung
    ## 40                  Norwegian Forest Cat
    ## 41                                Ocicat
    ## 42                    Oriental Long Hair
    ## 43                   Oriental Short Hair
    ## 44                        Oriental Tabby
    ## 45                               Persian
    ## 46                             Pixie-Bob
    ## 47                            Ragamuffin
    ## 48                               Ragdoll
    ## 49                          Russian Blue
    ## 50                         Scottish Fold
    ## 51                           Selkirk Rex
    ## 52                               Siamese
    ## 53                              Siberian
    ## 54                                Silver
    ## 55                             Singapura
    ## 56                              Snowshoe
    ## 57                                Somali
    ## 58                 Sphynx / Hairless Cat
    ## 59                                 Tabby
    ## 60                                 Tiger
    ## 61                             Tonkinese
    ## 62                                Torbie
    ## 63                         Tortoiseshell
    ## 64                        Turkish Angora
    ## 65                           Turkish Van
    ## 66                                Tuxedo
    ## 
    ## $petfinder$breeds$`@animal`
    ## [1] "cat"
    ## 
    ## 
    ## $petfinder$header
    ## $petfinder$header$timestamp
    ## $petfinder$header$timestamp$`$t`
    ## [1] "2018-05-13T21:53:18Z"
    ## 
    ## 
    ## $petfinder$header$status
    ## $petfinder$header$status$message
    ## named list()
    ## 
    ## $petfinder$header$status$code
    ## $petfinder$header$status$code$`$t`
    ## [1] "100"
    ## 
    ## 
    ## 
    ## $petfinder$header$version
    ## $petfinder$header$version$`$t`
    ## [1] "0.1"
    ## 
    ## 
    ## 
    ## $petfinder$`@xsi:noNamespaceSchemaLocation`
    ## [1] "http://api.petfinder.com/schemas/0.9/petfinder.xsd"

`breed.list()` can also be set to return a `data.frame` object by
setting the `return_df` parameter to `TRUE`.

    cats <- pf$breed.list('cat', return_df = TRUE)
    head(cats)

    ##           cat.breeds
    ## 1         Abyssinian
    ## 2      American Curl
    ## 3 American Shorthair
    ## 4  American Wirehair
    ## 5  Applehead Siamese
    ## 6           Balinese

### Finding pet records matching criteria

The `pet.find()` method enables one to return a `data.frame` of pet
records that match the input parameters. The available parameters can be
found using `?pet.find()` or checking out the [Petfinder API
documentation](https://www.petfinder.com/developers/api-docs#methods)
directly.

Let's say we want to find female cats in Washington. The default amount
of records is 25 (assuming there are 25 to return), which can be
overridden with the `count` parameter.

    wa_cats <- pf$pet.find('WA', 'cat', sex='F')

The returned data can also be automatically parsed into a `data.frame`
by setting the method parameter `return_df` to TRUE. Here, we make the
same call to the Petfinder API but with `return_df = TRUE` and print the
first six rows of the first ten columns to demonstrate the returned
`data.frame`.

    wa_cats <- pf$pet.find('WA', 'cat', sex='F', return_df = TRUE)
    head(wa_cats[,1:10])

    ##   status  contact.phone contact.state                   contact.email
    ## 1      A   206-296-7387            WA        adoptapet@kingcounty.gov
    ## 2      A   206-296-7387            WA        adoptapet@kingcounty.gov
    ## 3      A   425-576-5548            WA           info@thewhole-cat.com
    ## 4      A   425-576-5548            WA           info@thewhole-cat.com
    ## 5      A           <NA>            WA       rescuinganimals@gmail.com
    ## 6      A (253) 856-1771            WA anotherchancecats2007@gmail.com
    ##   contact.city contact.zip  contact.address1    age size       id
    ## 1         Kent       98032  21615 64th Ave S Senior    M 39921493
    ## 2         Kent       98032  21615 64th Ave S  Adult    L 37949653
    ## 3      Redmond       98052 8103 161st Ave NE Senior    L 40688475
    ## 4      Redmond       98052 8103 161st Ave NE Senior    M 41470264
    ## 5  Federal Way       98023              <NA>  Adult    M 41589923
    ## 6   Des Moines       98198      PO Box 13244  Young    M 39650811

### Returning random pet records

The `pet.getRandom()` method returns a random pet ID by default, but can
return a full pet record with a description by setting
`output = 'full'`.

    pf$pet.getRandom(output = 'full')

    ## $`@encoding`
    ## [1] "iso-8859-1"
    ## 
    ## $`@version`
    ## [1] "1.0"
    ## 
    ## $petfinder
    ## $petfinder$pet
    ## $petfinder$pet$options
    ## $petfinder$pet$options$option
    ##             $t
    ## 1      altered
    ## 2     hasShots
    ## 3 housetrained
    ## 4       noDogs
    ## 5       noCats
    ## 6       noKids
    ## 
    ## 
    ## $petfinder$pet$status
    ## $petfinder$pet$status$`$t`
    ## [1] "A"
    ## 
    ## 
    ## $petfinder$pet$contact
    ## $petfinder$pet$contact$phone
    ## $petfinder$pet$contact$phone$`$t`
    ## [1] "717-831-5010"
    ## 
    ## 
    ## $petfinder$pet$contact$state
    ## $petfinder$pet$contact$state$`$t`
    ## [1] "PA"
    ## 
    ## 
    ## $petfinder$pet$contact$address2
    ## named list()
    ## 
    ## $petfinder$pet$contact$email
    ## $petfinder$pet$contact$email$`$t`
    ## [1] "info@castawaycritters.org"
    ## 
    ## 
    ## $petfinder$pet$contact$city
    ## $petfinder$pet$contact$city$`$t`
    ## [1] "Harrisburg"
    ## 
    ## 
    ## $petfinder$pet$contact$zip
    ## $petfinder$pet$contact$zip$`$t`
    ## [1] "17105"
    ## 
    ## 
    ## $petfinder$pet$contact$fax
    ## named list()
    ## 
    ## $petfinder$pet$contact$address1
    ## $petfinder$pet$contact$address1$`$t`
    ## [1] "P.O. Box 1421"
    ## 
    ## 
    ## 
    ## $petfinder$pet$age
    ## $petfinder$pet$age$`$t`
    ## [1] "Adult"
    ## 
    ## 
    ## $petfinder$pet$size
    ## $petfinder$pet$size$`$t`
    ## [1] "M"
    ## 
    ## 
    ## $petfinder$pet$media
    ## $petfinder$pet$media$photos
    ## $petfinder$pet$media$photos$photo
    ##    @size
    ## 1    pnt
    ## 2    fpm
    ## 3      x
    ## 4     pn
    ## 5      t
    ## 6    pnt
    ## 7    fpm
    ## 8      x
    ## 9     pn
    ## 10     t
    ## 11   pnt
    ## 12   fpm
    ## 13     x
    ## 14    pn
    ## 15     t
    ##                                                                                       $t
    ## 1  http://photos.petfinder.com/photos/pets/35679386/1/?bust=1488734507&width=60&-pnt.jpg
    ## 2  http://photos.petfinder.com/photos/pets/35679386/1/?bust=1488734507&width=95&-fpm.jpg
    ## 3   http://photos.petfinder.com/photos/pets/35679386/1/?bust=1488734507&width=500&-x.jpg
    ## 4  http://photos.petfinder.com/photos/pets/35679386/1/?bust=1488734507&width=300&-pn.jpg
    ## 5    http://photos.petfinder.com/photos/pets/35679386/1/?bust=1488734507&width=50&-t.jpg
    ## 6  http://photos.petfinder.com/photos/pets/35679386/2/?bust=1488734507&width=60&-pnt.jpg
    ## 7  http://photos.petfinder.com/photos/pets/35679386/2/?bust=1488734507&width=95&-fpm.jpg
    ## 8   http://photos.petfinder.com/photos/pets/35679386/2/?bust=1488734507&width=500&-x.jpg
    ## 9  http://photos.petfinder.com/photos/pets/35679386/2/?bust=1488734507&width=300&-pn.jpg
    ## 10   http://photos.petfinder.com/photos/pets/35679386/2/?bust=1488734507&width=50&-t.jpg
    ## 11 http://photos.petfinder.com/photos/pets/35679386/3/?bust=1477877892&width=60&-pnt.jpg
    ## 12 http://photos.petfinder.com/photos/pets/35679386/3/?bust=1477877892&width=95&-fpm.jpg
    ## 13  http://photos.petfinder.com/photos/pets/35679386/3/?bust=1477877892&width=500&-x.jpg
    ## 14 http://photos.petfinder.com/photos/pets/35679386/3/?bust=1477877892&width=300&-pn.jpg
    ## 15   http://photos.petfinder.com/photos/pets/35679386/3/?bust=1477877892&width=50&-t.jpg
    ##    @id
    ## 1    1
    ## 2    1
    ## 3    1
    ## 4    1
    ## 5    1
    ## 6    2
    ## 7    2
    ## 8    2
    ## 9    2
    ## 10   2
    ## 11   3
    ## 12   3
    ## 13   3
    ## 14   3
    ## 15   3
    ## 
    ## 
    ## 
    ## $petfinder$pet$id
    ## $petfinder$pet$id$`$t`
    ## [1] "35679386"
    ## 
    ## 
    ## $petfinder$pet$shelterPetId
    ## $petfinder$pet$shelterPetId$`$t`
    ## [1] "1732589-CC-11179"
    ## 
    ## 
    ## $petfinder$pet$breeds
    ## $petfinder$pet$breeds$breed
    ##                     $t
    ## 1               Beagle
    ## 2 Jack Russell Terrier
    ## 
    ## 
    ## $petfinder$pet$name
    ## $petfinder$pet$name$`$t`
    ## [1] "Duke- *ADOPTION SPECIAL*"
    ## 
    ## 
    ## $petfinder$pet$sex
    ## $petfinder$pet$sex$`$t`
    ## [1] "M"
    ## 
    ## 
    ## $petfinder$pet$description
    ## $petfinder$pet$description$`$t`
    ## [1] "You can fill out an adoption application online on our official website.Please contact Jamie (ccjamieballa@gmail.com) for more information about this pet.Hello my name is Duke! I really would love a forever home. I love to run and play so a fenced yard would be so fun! I do well on walks and don't pull on my leash.I really love being the center of attention so I prefer to live without other animals. We are still trying out how well I do with children.I am potty trained, well mannered, crate trained. A super loving pup who is quiet, timid with loud noises and knows sit and stay. I travel great in the car.I would make a great running companion or might even do pretty well in Agility training. I would love to be a part of my very own family. Could that be you??Duke is in foster care so please complete an application before meeting him. Completing an application does not obligate you to adopt; however, it is required. Applications are processed in the order received in an effort to find the best match possible for both the dog and the adopter.*Duke has an adoption special right now. His adoption fee is only $150. If you feel you are the right home for Duke please fill out an app! 5/12/18 5:11 PM"
    ## 
    ## 
    ## $petfinder$pet$mix
    ## $petfinder$pet$mix$`$t`
    ## [1] "yes"
    ## 
    ## 
    ## $petfinder$pet$shelterId
    ## $petfinder$pet$shelterId$`$t`
    ## [1] "PA224"
    ## 
    ## 
    ## $petfinder$pet$lastUpdate
    ## $petfinder$pet$lastUpdate$`$t`
    ## [1] "2016-07-15T21:28:15Z"
    ## 
    ## 
    ## $petfinder$pet$animal
    ## $petfinder$pet$animal$`$t`
    ## [1] "Dog"
    ## 
    ## 
    ## 
    ## $petfinder$`@xmlns:xsi`
    ## [1] "http://www.w3.org/2001/XMLSchema-instance"
    ## 
    ## $petfinder$header
    ## $petfinder$header$timestamp
    ## $petfinder$header$timestamp$`$t`
    ## [1] "2018-05-13T21:53:20Z"
    ## 
    ## 
    ## $petfinder$header$status
    ## $petfinder$header$status$message
    ## named list()
    ## 
    ## $petfinder$header$status$code
    ## $petfinder$header$status$code$`$t`
    ## [1] "100"
    ## 
    ## 
    ## 
    ## $petfinder$header$version
    ## $petfinder$header$version$`$t`
    ## [1] "0.1"
    ## 
    ## 
    ## 
    ## $petfinder$`@xsi:noNamespaceSchemaLocation`
    ## [1] "http://api.petfinder.com/schemas/0.9/petfinder.xsd"

We can also get a set of random results by setting the `records`
parameter to the number of desired results to return. Note that each
record counts as one call to the Petfinder API.

    random_records <- pf$pet.getRandom(records = 3, output = 'full')

Similar to other methods available in the PetfindeR package, the
`pet.getRandom` method can also be set to return a `data.frame` by
setting the parameter `return_df = TRUE`. As an example, we get three
random pet records again and output the result as a `data.frame` (note
the returned records will likely not be the same as the earlier returned
records due to the random nature of the output).

    random_records_df <- pf$pet.getRandom(records = 3, output = 'full', return_df = TRUE)
    random_records_df[,1:10]

    ##   status.1 status.2     status.3 status address1.state
    ## 1  altered hasShots housetrained      A             MA
    ## 2     <NA>     <NA>         <NA>      A             TX
    ## 3  altered hasShots housetrained      A             MI
    ##                           address1.email address1.city address1.zip   age
    ## 1                   Info@AhimsaHaven.org     Templeton        01468 Adult
    ## 2 animal.customerservice@austintexas.gov        Austin        78702 Adult
    ## 3                     kelcruiser@aol.com        Macomb        48042 Adult
    ##   size
    ## 1    L
    ## 2   XL
    ## 3    M

### Getting pet records associated with a petId

Given a petId, an ID associated with information on a pet in the
Petfinder database, the `pet.get()` method will return the pet record as
a JSON object represented as an R list. The method also accepts a vector
or list of IDs for returning multiple records. For example, we can take
the petIds given in our previous call to `pet.getRandom()` and pass
those to `pet.get()`. Note since we are using the same petIds from
before, the returned records will be the same. We also set the
`return_df` parameter to `TRUE` to demonstrate the functionality to
convert the returned JSON result into a `data.frame` as in other methods
seen previously.

    pet_get_df <- pf$pet.get(petId = random_records_df$id, return_df = TRUE)
    pet_get_df[,1:10]

    ##   status.1 status.2     status.3 status address1.state
    ## 1  altered hasShots housetrained      A             MA
    ## 2     <NA>     <NA>         <NA>      A             TX
    ## 3  altered hasShots housetrained      A             MI
    ##                           address1.email address1.city address1.zip   age
    ## 1                   Info@AhimsaHaven.org     Templeton        01468 Adult
    ## 2 animal.customerservice@austintexas.gov        Austin        78702 Adult
    ## 3                     kelcruiser@aol.com        Macomb        48042 Adult
    ##   size
    ## 1    L
    ## 2   XL
    ## 3    M

## Shelter Methods

<table>
<colgroup>
<col width="16%" />
<col width="15%" />
<col width="68%" />
</colgroup>
<thead>
<tr class="header">
<th>Method</th>
<th>Petfinder API Method</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>shelter.find()</td>
<td>shelter.find</td>
<td>Returns a collection of shelter records matching input parameters.</td>
</tr>
<tr class="even">
<td>shelter.get()</td>
<td>shelter.get</td>
<td>Returns a single shelter record.</td>
</tr>
<tr class="odd">
<td>shelter.getPets()</td>
<td>shelter.getPets</td>
<td>Returns a collection of pet records for an individual shelter.</td>
</tr>
<tr class="even">
<td>shelter.listByBreed()</td>
<td>shelter.listByBreed</td>
<td>Returns a list of shelter IDs listing animals matching the input animal breed.</td>
</tr>
</tbody>
</table>

Shelter methods are somewhat similar to the Pet methods we explored
previously, but return information on animal shelters and other animal
welfare organizations.

### Finding animal welfare organizations in an area

Using the `shelter.find()` method, one can locate shelters and their
available attributes matching the input parameters. For example, say we
wanted to find shelters in a ZIP code in Seattle (my old zip code).

    wa_shelters <- pf$shelter.find('98115')
    head(wa_shelters$petfinder$shelters$shelter)

    ##   country.$t longitude.$t                                    name.$t
    ## 1         US    -122.2939                      Forgotten Dogs Rescue
    ## 2         US    -122.2939 Fox Terrier Fanciers of Puget Sound Rescue
    ## 3         US    -122.2939                    Little Blessings Rescue
    ## 4         US    -122.3004                           Dog Gone Seattle
    ## 5         US    -122.3005          Friends of the Animals Foundation
    ## 6         US    -122.3005            Pacific Northwest KUVASZ Rescue
    ##           phone.$t state.$t                                  email.$t
    ## 1             <NA>       WA           forgotten.dogs.rescue@gmail.com
    ## 2  360-733-5735          WA                   kmartin44@earthlink.net
    ## 3    206473-1111         WA adoptions@littleblessingsrescue.vpweb.com
    ## 4             <NA>       WA                  adopt@doggoneseattle.org
    ## 5 (206) 719-4864         WA                       info@fafseattle.org
    ## 6             <NA>       WA                    vicki@AnimalsReign.com
    ##   city.$t zip.$t latitude.$t id.$t    address1.$t
    ## 1 Seattle  98115     47.6831 WA368           <NA>
    ## 2 Seattle  98115     47.6831  WA58           <NA>
    ## 3 Seattle  98115     47.6831 WA620           <NA>
    ## 4 Seattle  98165     47.7161 WA650           <NA>
    ## 5 Seattle  98125     47.7165  WA77 P.O. Box 16308
    ## 6 Seattle  98125     47.7165  WA90           <NA>

As with other methods in `PetfindeR`, the `shelter.find` method also has
a `return_df` parameter that coerces and outputs the returned JSON into
a workable `data.frame`.

    wa_shelters_df <- pf$shelter.find('98115', return_df = TRUE)
    head(wa_shelters_df)

    ##   country longitude                                       name
    ## 1      US -122.2939                      Forgotten Dogs Rescue
    ## 2      US -122.2939 Fox Terrier Fanciers of Puget Sound Rescue
    ## 3      US -122.2939                    Little Blessings Rescue
    ## 4      US -122.3004                           Dog Gone Seattle
    ## 5      US -122.3005          Friends of the Animals Foundation
    ## 6      US -122.3005            Pacific Northwest KUVASZ Rescue
    ##              phone shelterate                                     email
    ## 1             <NA>         WA           forgotten.dogs.rescue@gmail.com
    ## 2  360-733-5735            WA                   kmartin44@earthlink.net
    ## 3    206473-1111           WA adoptions@littleblessingsrescue.vpweb.com
    ## 4             <NA>         WA                  adopt@doggoneseattle.org
    ## 5 (206) 719-4864           WA                       info@fafseattle.org
    ## 6             <NA>         WA                    vicki@AnimalsReign.com
    ##      city   zip latitude    id       address1
    ## 1 Seattle 98115  47.6831 WA368           <NA>
    ## 2 Seattle 98115  47.6831  WA58           <NA>
    ## 3 Seattle 98115  47.6831 WA620           <NA>
    ## 4 Seattle 98165  47.7161 WA650           <NA>
    ## 5 Seattle 98125  47.7165  WA77 P.O. Box 16308
    ## 6 Seattle 98125  47.7165  WA90           <NA>

### Returning information on specific animal welfare organizations

Similar to `pet.get()`, the `shelter.get()` method takes a shelterId and
returns the available information on the shelter from the Petfinder
database.

One shelter that's very dear to me is [Seattle Area Feline
Rescue](http://www.seattleareafelinerescue.org/), the shelterId of which
is 'WA40'. Let's return the information available on the rescue.

    safr <- pf$shelter.get('WA40')
    safr

    ## $`@encoding`
    ## [1] "iso-8859-1"
    ## 
    ## $`@version`
    ## [1] "1.0"
    ## 
    ## $petfinder
    ## $petfinder$`@xmlns:xsi`
    ## [1] "http://www.w3.org/2001/XMLSchema-instance"
    ## 
    ## $petfinder$shelter
    ## $petfinder$shelter$country
    ## $petfinder$shelter$country$`$t`
    ## [1] "US"
    ## 
    ## 
    ## $petfinder$shelter$longitude
    ## $petfinder$shelter$longitude$`$t`
    ## [1] "-122.3428"
    ## 
    ## 
    ## $petfinder$shelter$name
    ## $petfinder$shelter$name$`$t`
    ## [1] "Seattle Area Feline Rescue"
    ## 
    ## 
    ## $petfinder$shelter$phone
    ## $petfinder$shelter$phone$`$t`
    ## [1] "206-659-6220 "
    ## 
    ## 
    ## $petfinder$shelter$state
    ## $petfinder$shelter$state$`$t`
    ## [1] "WA"
    ## 
    ## 
    ## $petfinder$shelter$address2
    ## named list()
    ## 
    ## $petfinder$shelter$email
    ## $petfinder$shelter$email$`$t`
    ## [1] "adoptions@seattleareafelinerescue.org"
    ## 
    ## 
    ## $petfinder$shelter$city
    ## $petfinder$shelter$city$`$t`
    ## [1] "Shoreline"
    ## 
    ## 
    ## $petfinder$shelter$zip
    ## $petfinder$shelter$zip$`$t`
    ## [1] "98133"
    ## 
    ## 
    ## $petfinder$shelter$fax
    ## named list()
    ## 
    ## $petfinder$shelter$latitude
    ## $petfinder$shelter$latitude$`$t`
    ## [1] "47.7382"
    ## 
    ## 
    ## $petfinder$shelter$id
    ## $petfinder$shelter$id$`$t`
    ## [1] "WA40"
    ## 
    ## 
    ## $petfinder$shelter$address1
    ## $petfinder$shelter$address1$`$t`
    ## [1] "14717 Aurora Ave N"
    ## 
    ## 
    ## 
    ## $petfinder$header
    ## $petfinder$header$timestamp
    ## $petfinder$header$timestamp$`$t`
    ## [1] "2018-05-13T21:53:24Z"
    ## 
    ## 
    ## $petfinder$header$status
    ## $petfinder$header$status$message
    ## named list()
    ## 
    ## $petfinder$header$status$code
    ## $petfinder$header$status$code$`$t`
    ## [1] "100"
    ## 
    ## 
    ## 
    ## $petfinder$header$version
    ## $petfinder$header$version$`$t`
    ## [1] "0.1"
    ## 
    ## 
    ## 
    ## $petfinder$`@xsi:noNamespaceSchemaLocation`
    ## [1] "http://api.petfinder.com/schemas/0.9/petfinder.xsd"

This data can also be transformed into a one-row `data.frame` by setting
`return_df = TRUE`.

    safr_df <- pf$shelter.get('WA40', return_df = TRUE)
    safr_df

    ##   country longitude                       name         phone state
    ## 1      US -122.3428 Seattle Area Feline Rescue 206-659-6220     WA
    ##   address2                                 email      city   zip fax
    ## 1       NA adoptions@seattleareafelinerescue.org Shoreline 98133  NA
    ##   latitude   id           address1
    ## 1  47.7382 WA40 14717 Aurora Ave N

### Getting pet records from a shelter

Let's say we are interested in finding the available pets at a
particular shelter; we could use the `shelter.getPets()` method to
quickly find this information. Here, we return the pets currently
available at the Seattle Area Feline Rescue and print the first ten
columns of the returned data.

    safr.pets <- pf$shelter.getPets('WA40')
    head(safr.pets$petfinder$pets$pet)[,1:10]

    ##                          options.option status.$t contact.phone.$t
    ## 1       altered, hasShots, housetrained         A    206-659-6220 
    ## 2                                  NULL         A    206-659-6220 
    ## 3                 altered, housetrained         A    206-659-6220 
    ## 4         altered, housetrained, noKids         A    206-659-6220 
    ## 5 altered, housetrained, noCats, noKids         A    206-659-6220 
    ## 6         altered, housetrained, noKids         A    206-659-6220 
    ##   contact.state.$t                      contact.email.$t contact.city.$t
    ## 1               WA adoptions@seattleareafelinerescue.org       Shoreline
    ## 2               WA adoptions@seattleareafelinerescue.org       Shoreline
    ## 3               WA adoptions@seattleareafelinerescue.org       Shoreline
    ## 4               WA adoptions@seattleareafelinerescue.org       Shoreline
    ## 5               WA adoptions@seattleareafelinerescue.org       Shoreline
    ## 6               WA adoptions@seattleareafelinerescue.org       Shoreline
    ##   contact.zip.$t contact.address1.$t age.$t size.$t
    ## 1          98133  14717 Aurora Ave N  Adult       L
    ## 2          98133  14717 Aurora Ave N   Baby       M
    ## 3          98133  14717 Aurora Ave N Senior       L
    ## 4          98133  14717 Aurora Ave N Senior       L
    ## 5          98133  14717 Aurora Ave N  Adult       M
    ## 6          98133  14717 Aurora Ave N  Adult       M

The `shelter.getPets()` method also has a `return_df` parameter that can
be set to TRUE to return a clean, workable `data.frame` for analysis.

    safr.pets_df <- pf$shelter.getPets('WA40', return_df = TRUE)
    head(safr.pets_df)[,1:10]

    ##   status contact.phone contact.state                         contact.email
    ## 1      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ## 2      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ## 3      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ## 4      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ## 5      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ## 6      A 206-659-6220             WA adoptions@seattleareafelinerescue.org
    ##   contact.city contact.zip   contact.address1    age size       id
    ## 1    Shoreline       98133 14717 Aurora Ave N  Adult    L  6481751
    ## 2    Shoreline       98133 14717 Aurora Ave N   Baby    M  6497950
    ## 3    Shoreline       98133 14717 Aurora Ave N Senior    L 38016564
    ## 4    Shoreline       98133 14717 Aurora Ave N Senior    L 40493265
    ## 5    Shoreline       98133 14717 Aurora Ave N  Adult    M 40674254
    ## 6    Shoreline       98133 14717 Aurora Ave N  Adult    M 40977444

### Finding shelters that have a particular animal breed

The `shelter.listByBreed()` method allows one to find shelters that have
a particular breed of animal, which may be useful for users interested
in finding rarer breeds of animal. The `breed` argument must match a
breed listed in the Petfinder database, which can be easily extracted by
using the `breed.list()` method. We already pulled the available cat
breeds earlier in the vignette, so we can use that to select a breed of
cat to search.

The Abyssinian is a beautiful and wonderfully friendly breed of cat, so
let's search for some shelters that have Abyssinians listed on
Petfinder.

    aby_shelters <- pf$shelter.listByBreed('cat', 'Abyssinian')

Note: There currently seems to be an issue (as of 5/9/2018) with the
Petfinder API and the `shelter.listByBreed` method. The API will return
an object successfully, but the data is empty. Hopefully, Petfinder will
be able to fix this issue soon, but in the meantime, I leave this note
here just in case.

## Conclusion

In this vignette, we introduced the core functionality of the
`PetfindeR` library for interacting and extracting data from the
Petfinder API. In future vignettes, we will further explore working with
the `PetfindeR` library as well some potential uses of the package for
data extraction and analysis.
