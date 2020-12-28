"""JSON parser tests"""
import json
import urllib.request
from typing import Dict

import pytest

import json_parser


@pytest.mark.parametrize(
    ('json_string', 'expected'),
    (
        ('{}', {}),
        ('[]', []),
        ('{"abc": "def"}', {"abc": "def"}),
        ('{"value": 42}', {"value": 42}),
        ('{"value": -12.3}', {"value": -12.3}),
        ('{"value": "\\\"Hello\\\" \\n\\b\\f\\r\\t\\u0123"}',
         {"value": '"Hello" \n\b\f\r\t\u0123'}),
        ('["foo", "bar"]', ["foo", "bar"]),
        ('[1, 2, 3]', [1, 2, 3]),
        ('{"value1": true, "value2": false, "value3": null}',
         {"value1": True, "value2": False, "value3": None}),
        ('{"foo": [1, 2, {"bar": 3}]}', {"foo": [1, 2, {"bar": 3}]}),
        ('{"results":[{"gender":"male","name":{"title":"Mr","first":"سینا","last":"موسوی"},"location":{"street":{"number":8134,"name":"میدان امام حسین"},"city":"ارومیه","state":"خوزستان","country":"Iran","postcode":24340,"coordinates":{"latitude":"27.3083","longitude":"-104.2564"},"timezone":{"offset":"0:00","description":"Western Europe Time, London, Lisbon, Casablanca"}},"email":"syn.mwswy@example.com","login":{"uuid":"8a6da152-019a-40b4-80b0-bfafd5281fd7","username":"sadbear764","password":"1947","salt":"ddKNbUrc","md5":"7ff0c750f9b8d7690d50385754a7fe25","sha1":"e140544e222f27a2d0aa809ccb00a1d1ca1fda60","sha256":"fd5dbd61da24a82f48971a6d027400a2fd5b0808fd108764f17d87aaa61774d9"},"dob":{"date":"1996-12-06T21:55:10.574Z","age":24},"registered":{"date":"2013-04-07T05:56:17.049Z","age":7},"phone":"083-15098477","cell":"0998-569-1505","id":{"name":"","value":null},"picture":{"large":"https://randomuser.me/api/portraits/men/94.jpg","medium":"https://randomuser.me/api/portraits/med/men/94.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/94.jpg"},"nat":"IR"}],"info":{"seed":"db5d8d673b395e5a","results":1,"page":1,"version":"1.3"}}',
         {'results': [{'gender': 'male', 'name': {'title': 'Mr', 'first': 'سینا', 'last': 'موسوی'}, 'location': {'street': {'number': 8134, 'name': 'میدان امام حسین'}, 'city': 'ارومیه', 'state': 'خوزستان', 'country': 'Iran', 'postcode': 24340, 'coordinates': {'latitude': '27.3083', 'longitude': '-104.2564'}, 'timezone': {'offset': '0:00', 'description': 'Western Europe Time, London, Lisbon, Casablanca'}}, 'email': 'syn.mwswy@example.com', 'login': {'uuid': '8a6da152-019a-40b4-80b0-bfafd5281fd7', 'username': 'sadbear764', 'password': '1947', 'salt': 'ddKNbUrc', 'md5': '7ff0c750f9b8d7690d50385754a7fe25', 'sha1': 'e140544e222f27a2d0aa809ccb00a1d1ca1fda60', 'sha256': 'fd5dbd61da24a82f48971a6d027400a2fd5b0808fd108764f17d87aaa61774d9'}, 'dob': {'date': '1996-12-06T21:55:10.574Z', 'age': 24}, 'registered': {'date': '2013-04-07T05:56:17.049Z', 'age': 7}, 'phone': '083-15098477', 'cell': '0998-569-1505', 'id': {'name': '', 'value': None}, 'picture': {'large': 'https://randomuser.me/api/portraits/men/94.jpg', 'medium': 'https://randomuser.me/api/portraits/med/men/94.jpg', 'thumbnail': 'https://randomuser.me/api/portraits/thumb/men/94.jpg'}, 'nat': 'IR'}], 'info': {'seed': 'db5d8d673b395e5a', 'results': 1, 'page': 1, 'version': '1.3'}}),
        ("""
        {
            "_id": "5fe977c6eae5f05b1903ee48",
            "index": 0,
            "guid": "f542c7d5-35f5-432d-9ba4-581979a77765",
            "isActive": true,
            "balance": "$2,018.45",
            "picture": "http://placehold.it/32x32",
            "age": 34,
            "eyeColor": "blue",
            "name": "King Hampton",
            "gender": "male",
            "company": "BOILICON",
            "email": "kinghampton@boilicon.com",
            "phone": "+1 (873) 467-3013",
            "address": "971 Calyer Street, Wollochet, New Jersey, 3753",
            "about": "Aute velit consequat tempor exercitation id occaecat sit pariatur irure laboris pariatur veniam fugiat aute. Laborum ea do occaecat culpa labore. Laboris anim commodo ipsum duis eu nulla incididunt in Lorem consectetur cillum in est. Velit amet eiusmod ullamco ut amet. Consectetur elit labore aliqua excepteur. Elit est eu voluptate reprehenderit qui aliqua exercitation ad esse consectetur. Proident quis ex quis proident ad dolor ex sint elit consectetur eu Lorem do proident.\r\n",
            "registered": "2017-01-04T11:20:50 -06:-30",
            "latitude": -66.260402,
            "longitude": 52.599917,
            "tags": [
                "ea",
                "anim",
                "Lorem",
                "veniam",
                "veniam",
                "enim",
                "officia"
            ],
            "friends": [
            {
                "id": 0,
                "name": "Leola Callahan"
            },
            {
                "id": 1,
                "name": "Doyle Ashley"
            },
            {
                "id": 2,
                "name": "Tamara Singleton"
            }
            ],
            "greeting": "Hello, King Hampton! You have 5 unread messages.",
            "favoriteFruit": "strawberry"
        }
  """, {
            "_id": "5fe977c6eae5f05b1903ee48",
            "index": 0,
            "guid": "f542c7d5-35f5-432d-9ba4-581979a77765",
            "isActive": True,
            "balance": "$2,018.45",
            "picture": "http://placehold.it/32x32",
            "age": 34,
            "eyeColor": "blue",
            "name": "King Hampton",
            "gender": "male",
            "company": "BOILICON",
            "email": "kinghampton@boilicon.com",
            "phone": "+1 (873) 467-3013",
            "address": "971 Calyer Street, Wollochet, New Jersey, 3753",
            "about": "Aute velit consequat tempor exercitation id occaecat sit pariatur irure laboris pariatur veniam fugiat aute. Laborum ea do occaecat culpa labore. Laboris anim commodo ipsum duis eu nulla incididunt in Lorem consectetur cillum in est. Velit amet eiusmod ullamco ut amet. Consectetur elit labore aliqua excepteur. Elit est eu voluptate reprehenderit qui aliqua exercitation ad esse consectetur. Proident quis ex quis proident ad dolor ex sint elit consectetur eu Lorem do proident.\r\n",
            "registered": "2017-01-04T11:20:50 -06:-30",
            "latitude": -66.260402,
            "longitude": 52.599917,
            "tags": [
                "ea",
                "anim",
                "Lorem",
                "veniam",
                "veniam",
                "enim",
                "officia"
            ],
            "friends": [
                {
                    "id": 0,
                    "name": "Leola Callahan"
                },
                {
                    "id": 1,
                    "name": "Doyle Ashley"
                },
                {
                    "id": 2,
                    "name": "Tamara Singleton"
                }
            ],
            "greeting": "Hello, King Hampton! You have 5 unread messages.",
            "favoriteFruit": "strawberry"
        })
    )
)
def test_parser(json_string: str, expected: Dict[str, object]) -> None:
    """JSON parser tests"""
    assert json_parser.parse(json_string) == expected


def test_parse_large_file() -> None:
    """Download and parse a 25MB JSON file from the internet"""
    url = "https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json"
    with urllib.request.urlopen(url) as json_file:
        json_string = json_file.read().decode()

    assert json_parser.parse(json_string) == json.loads(json_string)
