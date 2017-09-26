# 2017-00-26

- Added a new query that outputs a histogram of runtimes for tools. Not super
  useful since it has no intelligence from the input size.

# 2017-08-18

- Swapped to bigints after reading a [blog
  post](https://medium.com/@jakswa/the-night-the-postgresql-ids-ran-out-9430a2dbb895)
  and realising we may definitely capture this many jobs if aggregating from
  big galaxies.
