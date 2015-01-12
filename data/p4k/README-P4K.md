
P4K-ALL.JSON
============

  This is a text-format corpus consisting of reviews and accompanying metadata
  crawled from the independent-music journalism site http://pitchfork.com on
  January 10, 2014. This corpus was collected by Jonathan D. Jones and Kathleen
  Kusworo, using the scrapy python library.


DETAILS
=======
  
  Reviews are stored in .json format as a list of dictionaries. See below for a
  description of the items in each dictionary. Each key stores a list of
  strings. Values representing meta-data can have multiple list entries --
  for example,

    title -> ['I'm wide awake, it's morning', 'Digital ash in a digital urn'].

  This is because some writeups review multiple albums. In the example above it
  is because an artist released two albums simultaneously, but more often this
  occurs in box-set reviews.


FIELDS
======

  TITLE: Album title.

  ARTIST: Album artist. Multiple artists are delimited with the characters
    ' / ' between artists. This can occur with split EPs or collaborations,
    for example.

  LABEL: Record label that released the album. Multiple labels are delimited
    with the characters ' / ' between labels. Note that in very few
    occurrences multiple labels are delimited using only '/'. In this case it
    is impossible to distinguish between multiple labels and a single label
    with a slash character in its name.

  YEAR: Release year. Multiple release years are delimited with the character
    '/' between years. This can occur with reissues, for example.

  SCORE: Numeric score assigned by reviewer. This is a number between 0.0 and
    10.0, to one decimal point of precision.

  BNM_LABEL: Best new music label. Can be 'Best New Music', 'Best New
    Reissue' or '' (empty string). Note that this label was not used by
    Pitchfork until several years after it was founded.

  DATE: Date of review, formatted as MONTH DD YYYY. Example: December 19,
    2014.

  AUTHOR: Review author. There is at least one example of a multi-author
    review, which is formatted as [NAME_1] & [NAME_2].

  REVIEW: Essay justifying the score(s) given.
