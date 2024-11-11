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

### Description of settings

- `DB_PATH = "db/zone_data.json"`: This setting specifies the destination of the Facts API query results.
- `RESERVATION_MAX_HOURS = 0.0083`: The maximum number of hours a VSYS reservation is valid.
- `RESERVATION_MAX_DAYS = 21`: The maximum number of days a reservation is valid.
- `RESERVATION_PREFIX = "RES-"`: The prefix for VSYS reservation names.
- `PANORAMA = "204.232.167.99"`: The IP address of the Panorama instance.
- `AUTHORITY_URL = "https://login.microsoftonline.com/"`: The URL for the OAuth provider.
- `REDIRECT_URI = "http://localhost:8505"`: The redirect URI for OAuth authentication.
- `LOG_LEVEL = "INFO"`: The logging level.
- `LOG_FILE = "vsys_dashboard.log"`: The name of the log file.
- `LOG_DIR = "logs/"`: The directory where log files are stored.
- `DEVICE_GRPS = ["GTS-VSYS-ORD", "GTS-VSYS-DFW", "GTS-VSYS-IAD", "GTS-VSYS-FRA", "GTS-VSYS-HKG", "GTS-VSYS-LON", "GTS-VSYS-SIN", "GTS-VSYS-SJC", "GTS-VSYS-SYD"]`: The list of device groups in that define the inventory of vsys-eligible devices
- `FACTS_TOKEN_URL = "https://identity-internal.api.rackspacecloud.com/v2.0/tokens"`: The URL to obtain a token for the Facts API.
- `FACTS_URL = "https://facts.nsi.rackspace.com/vsys_infra/vsys_infra"`: The URL for the Facts API.
- `PER_PAGE = 50`: The number of results per page for the Facts API.


## UI Description
## API Description
