# polar-flow-export
Command line tool for bulk exporting TCX files from [Polar Flow](https://flow.polar.com/)

Requires [Python](https://www.python.org) 3.11 and dependencies are defined in pyproject.toml.

Usage is as follows:

    python polarflowexport.py <username> <password> <start_date> <end_date> <output_dir>

The start_date and end_date parameters are ISO-8601 date strings (i.e.
year-month-day). An example invocation is as follows:

    python polarflowexport.py me@me.com mypassword 2015-08-01 2015-08-30 /tmp/tcxfiles

Licensed under the Apache Software License v2, see: http://www.apache.org/licenses/LICENSE-2.0

This project is not in any way affiliated with Polar or Polar Flow. It is purely a
hobby project created out of a need to export a large quantity of TCX files from 
Polar Flow.
"""

## Why fork

The [original repo](https://github.com/gabrielreid/polar-flow-export) was no longer alive (long standing pull requests that got stale).
The heavyy lifting was done one the original repo but I need a working version with some additional 
features.
