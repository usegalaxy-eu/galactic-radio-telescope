# 2017-08-02

questions which need answers


Question                                            | Notes
--------                                            | -----
popular Galaxy instances                            | number of jobs in past week / month. Can be pushed to the live data
which instances have the tools I need               | could be pushed online which would enable search
which tools are popular (recently)                  | no reason to have this online
popular configuration / parameters                  | no reason to have this online
runtimes of tools                                   | no reason to have this online
relationships between runtime parameters and inputs | no reason to have this online
instance statistics?                                | no reason to have this online

The offline / online decision basically boils down to:

- do we need to search / sort / filter / query with limits
- or is it the GalaxyInstance object

everything else should be offline.

# 2017-08-04

- Removed public flag. Galaxy directory is someone else's job.
- switched to id from uuid due to size.
- dropped foreign key relationships. This is sub-optimal, but it will be much,
  much faster to load huge amounts of data. And due to the construction, if we
  ever change our mind we can go back and add foreign keys and re-import all
  data. Neat. At least saves me from my own (possible/likely) stupidity.
