# Restructuring of GRT

The original GRT was a proof-of-concept, and we now need something more permanent. It should be functional in the long
term, and not need to be rewritten every N years, but should support that if neccessary. This mostly means that we just
need to have a stable interface to accept job logs.

## New Constraints

- we will be accepting huge amounts of data
- this data does not need to be immediately visible in the frontend
- if we decide after the fact that data must be re-calculated, then we should be able to do this from raw logs that were
  submitted.

This is more of an "analytics" database than a transactional, we might decide that we need to denormalize for
performance, these sort of things. Maybe we want to make it available on a Hadoop cluster if the datasets are big
enough.

## New Structure

So! Given the new constraints, rather than a single giant django app that handles everything, we plan to decouple things
ever so slightly to allow us some more freedom in how and when we process the data.

- Data is uploaded to us (HTTP? FTP?)
- Cron job to ingest data into a postgres database (eventually we can add additional cron jobs to ingest into a document
  store, etc.)
- The web frontend has access to the postgres DB.
