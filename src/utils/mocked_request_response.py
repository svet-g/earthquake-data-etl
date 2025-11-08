import json
from unittest.mock import patch

# Mock response that mimics real USGS earthquake API
class MockEarthquakeResponse:
    def __init__(self):
        self.status_code = 200
        self._data = {
            "type": "FeatureCollection",
            "metadata": {
                "generated": 1699459200000,
                "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
                "title": "USGS All Earthquakes, Past Hour - FAKE",
                "count": 3
            },
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "mag": 4.5,
                        "place": "10km NE of San Francisco, CA",
                        "time": 1699459123000,
                        "updated": 1699459200000,
                        "tz": -480,
                        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd",
                        "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us7000abcd.geojson",
                        "felt": 25,
                        "cdi": 3.4,
                        "mmi": 4.5,
                        "alert": "green",
                        "status": "reviewed",
                        "tsunami": 0,
                        "sig": 312,
                        "net": "us",
                        "code": "7000abcd",
                        "ids": ",us7000abcd,",
                        "sources": ",us,",
                        "types": ",origin,phase-data,",
                        "nst": 45,
                        "dmin": 0.234,
                        "rms": 0.15,
                        "gap": 35,
                        "magType": "mb",
                        "type": "earthquake",
                        "title": "M 4.5 - 10km NE of San Francisco, CA"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-122.4194, 37.7749, 10.0]
                    },
                    "id": "us7000abcd"
                },
                {
                    "type": "Feature",
                    "properties": {
                        "mag": 2.3,
                        "place": "5km S of Mammoth Lakes, CA",
                        "time": 1699458900000,
                        "updated": 1699459100000,
                        "tz": -480,
                        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/nc73456789",
                        "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nc73456789.geojson",
                        "felt": None,
                        "cdi": None,
                        "mmi": None,
                        "alert": None,
                        "status": "automatic",
                        "tsunami": 0,
                        "sig": 81,
                        "net": "nc",
                        "code": "73456789",
                        "ids": ",nc73456789,",
                        "sources": ",nc,",
                        "types": ",origin,phase-data,",
                        "nst": 18,
                        "dmin": 0.045,
                        "rms": 0.08,
                        "gap": 82,
                        "magType": "md",
                        "type": "earthquake",
                        "title": "M 2.3 - 5km S of Mammoth Lakes, CA"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-118.9720, 37.6489, 8.5]
                    },
                    "id": "nc73456789"
                },
                {
                    "type": "Feature",
                    "properties": {
                        "mag": 5.2,
                        "place": "Pacific-Antarctic Ridge",
                        "time": 1699457800000,
                        "updated": 1699458900000,
                        "tz": None,
                        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000xyz1",
                        "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us6000xyz1.geojson",
                        "felt": None,
                        "cdi": None,
                        "mmi": None,
                        "alert": None,
                        "status": "reviewed",
                        "tsunami": 0,
                        "sig": 416,
                        "net": "us",
                        "code": "6000xyz1",
                        "ids": ",us6000xyz1,",
                        "sources": ",us,",
                        "types": ",origin,phase-data,",
                        "nst": None,
                        "dmin": 5.678,
                        "rms": 0.92,
                        "gap": 45,
                        "magType": "mb",
                        "type": "earthquake",
                        "title": "M 5.2 - Pacific-Antarctic Ridge"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-129.5, -55.2, 10.0]
                    },
                    "id": "us6000xyz1"
                }
            ]
        }
    
    def json(self):
        return self._data
    
    @property
    def text(self):
        return json.dumps(self._data)
    
    def raise_for_status(self):
        """Mimic requests.Response.raise_for_status()"""
        if self.status_code >= 400:
            raise Exception(f"{self.status_code} Error")
        # If status_code is 200, do nothing (success)


def mock_requests_get(url, *args, **kwargs):
    """Returns mock earthquake data for any USGS URL"""
    return MockEarthquakeResponse()