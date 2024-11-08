# VSYS Capacity Management Dashboard

## Notes on Build

The Dockerfile installs the files necessary to run the image. The primary framework in use is the Streamlit dashboard tool set. The dashboard relies on a CDW-provided SDK to interact with the Palo Alto Panorama. This SDK exists as a git submodule, pulled from another repository. That SDK resides in the `paloaltosdk` directory. The build process initializes and pulls this git repo into the parent repo.

## Code Layout

Palo Alto and other code specific to this implementation resides in the `rackspace_functions.py` file. The `streamlit_app.py` imports these functions, the `paloaltosdk`, and some utility functions for logging, etc. (also provided by CDW).

Streamlit reruns all the code that generates the page every time an action is chosen. Data that needs to be persisted is intentionally cached between runs.

Calls to the API that provides zone data come from the `facts_query.py` file. This file is run nightly and populates the zone aggr fields.

The `scheduled_tasks.py` file creates the cron jobs that run automatically. These can be adjusted in the running container.

The `./scripts` directory contains a set of example scripts that use the CDW `paloaltosdk`.

## Settings and Secrets

Runtime settings are loaded from the `settings.toml` file. These may be adjusted without rebuilding the image. The following are descriptions of those settings.

### General

- `DB_PATH = "db/zone_data.json"`: This setting specifies the destination of the Facts API query results.
