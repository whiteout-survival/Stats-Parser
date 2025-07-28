# Stats Parser

A utility for parsing and formatting stat data in Whiteout Survival.

- Parses raw city bonus data
- Formats output for readability

## Quickstart Guide

### Prerequisites

- [uv](https://pypi.org/project/uv/) (Python package manager) installed, if you want to manage Python dependencies

### Installation

```bash
uv sync
cd src
uv run api.py
```
A server will start on 0.0.0.0:8000 by default. 
## API Endpoint

### POST `/api/v1/read_stats`

Extracts and merges troop statistics from one or more images using OCR.

#### Request Body

Send a JSON object with the following structure:

```json
{
  "images": [
    {
      "image_data": "<base64-encoded-image>"
    },
    ...
  ]
}
```

- `images`: A list of objects, each containing a `image_data` field with a base64-encoded image (PNG, JPG, etc.).

#### Response

Returns a JSON object containing merged troop statistics extracted from all provided images.

```json
{
  "merged_stats": {
    "infantry": [attack, defense, lethality, health],
    "lancers": [attack, defense, lethality, health],
    "marksmen": [attack, defense, lethality, health]
  }
}
```

- Each troop type contains a list of four float values representing their respective stats.


### Example Usage

Refer to the [`demo_usage.py`](demo_usage.py) file for example usage and demonstration of the Stats Parser.

