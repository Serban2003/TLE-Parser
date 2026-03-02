# SpaceTrack TLE Client

A lightweight Python client for fetching **Two-Line Element (TLE)** data from [Space-Track.org](https://www.space-track.org), parsing it into a structured `TLE` dataclass, and exporting results to Excel.

---

## Features

- Authenticates with Space-Track
- Fetches latest TLE by NORAD ID
- Parses TLE into a structured `TLE` dataclass
- Exports data to Excel (`.xlsx`)

---

### Install dependencies

```bash
pip install requests openpyxl
```

## Configuration

Create a file named:

```text
SLTrack.ini
```

Add your Space-Track credentials:

```ini
[configuration]
username = your_space_track_username
password = your_space_track_password
output = ./out/tle_data.xlsx
```
---

## Excel Output

Each execution appends a row containing:

- Timestamp
- Satellite name
- NORAD ID
- Epoch (UTC)
- Orbital parameters
- Optional raw TLE lines
- Query URL
---

## Dependencies

- Python 3.9+
- `requests`
- `openpyxl`

