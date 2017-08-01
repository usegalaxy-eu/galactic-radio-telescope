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
└── archives
    ├── 0.tar.gz
    ├── 0.json
    ├── 1.tar.gz
    ├── 1.json
    ├── 2.tar.gz
    └── 2.json
```

The `archives/####.tar.gz` files will be structured as:

```
<report_id>.jobs.tsv
<report_id>.params.tsv
<report_id>.metric_txt.tsv
<report_id>.metric_num.tsv
```

The `archives/####.json` files will be used to store metadata about the specific upload, or anything else that we deem
relevant. The structure is liable to change whenever we deem necessary.

```json
{
  "version": 1,
  "galaxy_version": "17.09",
  "generated": "1501592951.19",
  "jobs": {
    "error": 22,
    "ok": 76
  },
  "metrics": {
    "_times": [
      [
        "init_start",
        0.00010895729064941406
      ],
      "..."
    ]
  },
  "report_hash": "sha256:1aa8b24e75077a173aeb2f1385bf38cc780260340d13303427b5c58e268784fb",
  "tools": [
    [
      "CONVERTER_maf_to_interval_0",
      "Convert MAF to Genomic Intervals",
      "1.0.2",
      null,
      null,
      null
    ],
    "..."
  ],
  "users": {
    "active": 10,
    "total": 2131
  }
}
```
