
# Administering Bluesky

**NOTICE** 2023-04-24:  DO NOT USE.
This material is out of date and will not be updated here.
This repository will be archived by 2023-09-01.
It should not be used for new work.  All content of this repository
(environment files, training documents, reference material) is migrating
to https://bcda-aps.github.io/bluesky_training/


See the [installation guide](/install/README.md).

## `db_activity_report`

The `db_activity_report` explores a list (provided) of workstations, each
possibly running a MongoDB server  hosting Bluesky databroker repositories.  For
each such repository identified, report its associated databases and simple
measures of activity.

<details>
<summary>Example</summary>

```
(bluesky_2021_1) prjemian@zap:~/.../projects/BCDA-APS/use_bluesky$ ./admin/db_activity_report.py 
Bluesky (databroker) Repository Report
==== ============= =========================== =======================
host repository    runs database               file references db     
==== ============= =========================== =======================
poof production-v1 metadatastore-production-v1 filestore-production-v1
poof quokka_intake quokka_intake-run_data      quokka_intake-file_refs
poof wombat        wombat-bluesky              wombat-bluesky         
poof test1         test1-run_data              test1-file_refs        
==== ============= =========================== =======================

Databroker Mongodb Server Activity Report: 2021-02-21
============== ===================== ========== ===================== ========== ==========
Mongodb server Databroker repository total runs runs since 2020-08-23 first run  last run  
============== ===================== ========== ===================== ========== ==========
poof           production-v1         3876       1513                  2017-02-05 2020-12-26
poof           quokka_intake         82         82                    2021-01-22 2021-02-10
poof           test1                 19         0                     2017-10-22 2017-11-03
poof           wombat                3          3                     2021-02-20 2021-02-20
============== ===================== ========== ===================== ========== ==========
```

</details>
