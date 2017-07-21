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

### Data Upload

Data will be uploaded to per-instance folders. The structure will be as follows:

```
<instance_id (uuid)>
├── archives
│   ├── 0.tar.gz
│   ├── 0.json
│   ├── 1.tar.gz
│   ├── 1.json
│   ├── 2.tar.gz
│   └── 2.json
└── metadata.json
```

The metadata.json will look approximately like:

```json
{
  "url": "https://example.com/galaxy/",
  "title": "NLP Galaxy",
  "description": "Some\ndescription",
  "public": true,
  "latitude": 0.000,
  "longitude": 0.000
  ],
  "owners": [
     "jane.doe"
  ]
}
```

The `archives/####.tar.gz` files will be structured as:


The `archives/####.json` files will be used to store metadata about the specific upload, or anything else that we deem
relevant. The structure is liable to change whenever we deem necessary.

```json
{
    "version": 1,
    "generated": 1500541683,
    "metrics": {
        "query_time": 0.000,
        "tarball_time": 0.000
    },
    "users": {
        "active": 30,
        "total": 1000,
    },
    "jobs": {
        "ok": 10000000
    },
    "tools": [
        {
            "id": "toolshed.g2....",
            "version": "1.0.0",
            "tool_shed_repository": {
                "changeset_revision": "abcdef",
                "name": "tool_repo",
                "toolshed": "toolshed.g2.bx.psu.edu"
            }
        }
    ]
}
```
