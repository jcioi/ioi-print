# IOI Printing System

The IOI Printing System handles all print requests in the International
Olympiad in Informatics, during the contests and the translation meetings.
The system has been developed for and was first used in the
[IOI 2017](http://ioi2017.org/) in Tehran, Iran.

The system supports the following tasks and requests:
  * Print requests from contestants during the contest
    (via a custom printer installed on all contestants machines) [`contestant`]
  * Call staff requests from the IOI Contest Management System [`cms_request`]
  * Print requests from the IOI Translation System during the translation meetings
    [`translation`]
  * Custom mass print requests [`mass`]

## Deployment

Deploy `ioiprint.api:app` on a WSGI-HTTP server of your choice.

ioiprint depends on the following services:

- CUPS server that spools print jobs for real printers.
- NetAdmin service that returns contestats' IDs, names, and desk IDs for a give workstation's IP address.
- Reverse proxies (if any) must correctly set `X-Real-IP` header to specify contestant workstation's IP address

## Configuration

ioiprint reads a JSON configuration from the file specified by `IOIPRINT_CONFIG` environment variable. Alternatively, `IOIPRINT_CONFIG` can be itself a JSON string.

```
{
  "contestant_max_pages": 10,        # max number of pages a contestant can print at a time
  "contastant_printer_map": {        # mapping of desk zones to names of printers used for contestant and cms_request jobs
    "A": "PRINTER",
    "B": "PRINTER",
  },
  "contestant_printer": "PRINTER",   # name of printer used for contestant and cms_request jobs (effective when contastant_printer_map is not specified)
  "translation_printer": "PRINTER",  # name of printer used for translation jobs
  "default_printer": "PRINTER",      # name of printer used for mass jobs when printer is not specified
  "cups_server": "hostname:port",    # address of CUPS server where the real printers are registered
  "netadmin_url": "https://netadmin" # URL to the netadmin service
}
```

## Configure printers

### For contestants print requests

All the contestant workstations must installed with a virtual printer that send print requests to ioiprint.
The contestants can print using this printer during contest and it will be printed on the printer configured for that zone.

For testing you can use `scripts/contestant.sh` (You should change `PRINT_SERVER_ADDRESS`).

You can also change the templates used for rendering the first page and the last page of the prints by changing the `first.html.jinja2` and `last.html.jinja2` in `ioiprint/template` directory (They are in [Jinja2](http://jinja.pocoo.org/) format).

### For call staff requests from CMS

You should add print server address in [CMS](https://github.com/akmohtashami/cms) and it should work.

For testing you can use `scripts/cms_request.sh` (You should change `PRINT_SERVER_ADDRESS`).

You can also change the template used for rendering the prints by changing the `request.html.jinja2` in `ioiprint/template` directory (They are in [Jinja2](http://jinja.pocoo.org/) format).

### For custom translation requests from Translation System

You should add print server address in [Translation System](https://github.com/noidsirius/IOI-Translation) and it should work.

For testing you can use `scripts/translation.sh` (You should change `PRINT_SERVER_ADDRESS`).

(Translation System also uses the `mass` request for non-custom prints.)

You can also change the template used for rendering the prints by changing the `translation.html.jinja2` in `ioiprint/template` directory (They are in [Jinja2](http://jinja.pocoo.org/) format).

### For custom printing

You can use `scripts/mass.sh` (You should change `PRINT_SERVER_ADDRESS`).

## API

### mass

```
endpoint: /mass
method: POST
parameters: pdf -> PDF document to print
            printer -> printer or class name that is configured in CUPS server
                       (If not given default printer is used)
            count -> number of times the system should print the file
```

This will print the file previously uploaded `count` times on the printer specified.

### translation

```
endpoint: /translation
method: POST
parameters: pdf -> PDF document to print
            country_code -> country code of the translating country (e.g. IR)
            country_name -> country name of the translating country (e.g. Iran)
            cover_page -> 0|1 to indicate whether to put a cover page in front of the PDF
            count -> number of times the system should print the file
```

This will add a first page and print the file previously uploaded `count` times on default printer.

### cms_request

```
endpoint: /cms_request
method: POST
parameters: request_message -> The request message (e.g. Restroom)
            ip -> IP of the contestant computer
```

This will print a page with contestant info and request message on the printer configured for the contestant zone.

### contestant

```
endpoint: /contestant
method: POST
parameters: pdf -> PDF docment to print
```

This will add a first and last page to the file and print it on the printer configured for the contestant zone.


## Development

Run `docker-compose up` to spawn ioiprint, CUPS server (connected to a CUPS-PDF virtual printer instead of real one), and NetAdmin stub service. ioiprint listens to 5000/tcp and you can access to the CUPS web interface at <https://localhost:6631/>.

Use the scripts under `./scripts` to generate API calls and check the generated PDF files in `./output`.

## Changing Contestant Data Source

By default the system will get contestant data from the IOI Network Administration System,
and the address is configurable in `docker-compose.yml`.

If you want to change the source of contestant data (e.g. to read it from a file)
you should change the `get_contestant_data` function in `ioiprint/contestant_data.py` file.
The input of the function is the ip of the contestant's computer.
The output should be a python dictionary consisting of the following keys:
- `contestant_id`: ID of the contestant
- `contestant_name`: Name of the contestant
- `contestant_country`: Country name of the contestant
- `zone`: Zone that contestant sits in (It is used for determining which printer should we use for this contestant)
- `desk_id`: ID of the contestant's desk
- `desk_image_url`: The SVG image of the map showing where the contestant is sitting.

## License

This software is distributed under the MIT license (see LICENSE.txt),
and uses third party libraries that are distributed under their own terms
(see LICENSE-3RD-PARTY.txt).

## Copyright
Copyright (c) 2017, IOI 2017 Host Technical Committee
