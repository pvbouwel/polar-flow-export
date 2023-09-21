# polar-flow-export
Command line tool for bulk exporting exercise and fitness data from [Polar Flow](https://flow.polar.com/) to your local
filesystem.


Usage is documented by the CLI:

   `polar-flow-export --help`

Simplest invocation exports data for past 31 days in working directory. Example with dummy credentials:
   `polar-flow-export me@me.com mypassword`

Licensed under the Apache Software License v2, see: http://www.apache.org/licenses/LICENSE-2.0

This project is not in any way affiliated with Polar or Polar Flow. It is purely a
hobby project created out of a need to export a large quantity of TCX files from 
Polar Flow.
"""

## Installation instructions

Requires [Python](https://www.python.org) 3.11 and a matching pip.

Easiest install is to clone the repository and in the `polar-flow-export` run `pip3 install .`.

This could give rise to dependency conflicts in that case you can install it in a venv (e.g. via [pipx](https://pypa.github.io/pipx/)).

## Attributions

This project was a fork from [original repo](https://github.com/gabrielreid/polar-flow-export). 

Since [original repo](https://github.com/gabrielreid/polar-flow-export) was no longer alive (long standing pull requests that got stale) forking
seemed the best option.
The heavyy lifting was done on the original repo but I need a working version with some additional 
features.
