
starting with code pulled over from ts_config_scheduler and ts_fbs_utils

from ts_fbs_utils/python/lsst/ts/fbs/utils/maintel:
lsst_ddf_presched.py
lsst_footprints.py
lsst_surveys.py
make_scheduler.py
roman_surveys.py
too_surveys.py

from ts_config_scheduler/Scheduler/feature_scheduler/maintel
fbs_config_lsst_survey.py

from ts_config_scheduler/Scheduler/ddf_gen:
not bothering to copy

----

Main changed from 5.4:

* changes to template gathering. Switched to gathering over multiple years
* change survey start date to Time("2026-10-15T12:00:00").mjd (from "2026-06-15T12:00:00")

