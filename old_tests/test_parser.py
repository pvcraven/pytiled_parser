"""Unit tests for pytiled_parser"""

import xml.etree.ElementTree as etree
from contextlib import ExitStack as does_not_raise

import pytest

from pytiled_parser import objects, utilities, xml_parser

LAYER_DATA = [
    (
        '<layer id="1" name="Tile Layer 1" width="10" height="10">' + "</layer>",
        (int(1), "Tile Layer 1", None, None, None),
    ),
    (
        '<layer id="2" name="Tile Layer 2" width="10" height="10" opacity="0.5">'
        + "</layer>",
        (int(2), "Tile Layer 2", None, float(0.5), None),
    ),
    (
        '<layer id="5" name="Tile Layer 4" width="10" height="10" offsetx="49" offsety="-50">'
        + "<properties>"
        + "</properties>"
        + "</layer>",
        (int(5), "Tile Layer 4", objects.OrderedPair(49, -50), None, "properties",),
    ),
]


@pytest.mark.parametrize("xml,expected", LAYER_DATA)
def test_parse_layer(xml, expected, monkeypatch):
    def mockreturn(*args):
        return "properties"

    monkeypatch.setattr(xml_parser, "_parse_properties_element", mockreturn)

    result = xml_parser._parse_layer(etree.fromstring(xml))

    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("#001122", (0x00, 0x11, 0x22, 0xFF)),
        ("001122", (0x00, 0x11, 0x22, 0xFF)),
        ("#FF001122", (0x00, 0x11, 0x22, 0xFF)),
        ("FF001122", (0x00, 0x11, 0x22, 0xFF)),
        ("FF001122", (0x00, 0x11, 0x22, 0xFF)),
    ],
)
def test_color_parsing(test_input, expected):
    assert utilities.parse_color(test_input) == expected


layer_data = [
    (
        etree.fromstring(
            "<data>\n1,2,3,4,5,6,7,8,\n"
            "9,10,11,12,13,14,15,16,\n"
            "17,18,19,20,21,22,23,24,\n"
            "25,26,27,28,29,30,31,32,\n"
            "33,34,35,36,37,38,39,40,\n"
            "41,42,43,44,45,46,47,48\n</data>"
        ),
        8,
        "csv",
        None,
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        does_not_raise(),
    ),
    (
        etree.fromstring("<data>\n0,0,0,0,0\n</data>"),
        5,
        "csv",
        None,
        [[0, 0, 0, 0, 0]],
        does_not_raise(),
    ),
    (
        etree.fromstring(
            "<data>AQAAAAIAAAADAAAABAAAAAUAAAAGAAAABwAAAAgAAAAJAAAACgAAAAsAAAAMAAAADQAAAA4AAAAPAAAAEAAAABEAAAASAAAAEwAAABQAAAAVAAAAFgAAABcAAAAYAAAAGQAAABoAAAAbAAAAHAAAAB0AAAAeAAAAHwAAACAAAAAhAAAAIgAAACMAAAAkAAAAJQAAACYAAAAnAAAAKAAAACkAAAAqAAAAKwAAACwAAAAtAAAALgAAAC8AAAAwAAAA</data>"
        ),
        8,
        "base64",
        None,
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        does_not_raise(),
    ),
    (
        etree.fromstring(
            "<data>eJwNwwUSgkAAAMAzEQOwUCzExPb/r2N3ZlshhLYdu/bsGzkwdujIsRMTUzOnzpy7cGnuyrWFG7fu3Huw9GjlybMXr968W/vw6cu3H7/+/NsAMw8EmQ==</data>"
        ),
        8,
        "base64",
        "zlib",
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        does_not_raise(),
    ),
    (
        etree.fromstring(
            "<data>H4sIAAAAAAAAAw3DBRKCQAAAwDMRA7BQLMTE9v+vY3dmWyGEth279uwbOTB26MixExNTM6fOnLtwae7KtYUbt+7ce7D0aOXJsxev3rxb+/Dpy7cfv/782wAcvDirwAAAAA==</data>"
        ),
        8,
        "base64",
        "gzip",
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        does_not_raise(),
    ),
    (
        etree.fromstring("<data>SGVsbG8gV29ybGQh</data>"),
        8,
        "base64",
        "lzma",
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        pytest.raises(ValueError),
    ),
    (
        etree.fromstring(
            "<data>/ .---- --..-- ..--- --..-- ...-- --..-- ....- --..-- ..... --..-- -.... --..-- --... --..-- ---.. --..-- / ----. --..-- .---- ----- --..-- .---- .---- --..-- .---- ..--- --..-- .---- ...-- --..-- .---- ....- --..-- .---- ..... --..-- .---- -.... --..-- / .---- --... --..-- .---- ---.. --..-- .---- ----. --..-- ..--- ----- --..-- ..--- .---- --..-- ..--- ..--- --..-- ..--- ...-- --..-- ..--- ....- --..-- / ..--- ..... --..-- ..--- -.... --..-- ..--- --... --..-- ..--- ---.. --..-- ..--- ----. --..-- ...-- ----- --..-- ...-- .---- --..-- ...-- ..--- --..-- / ...-- ...-- --..-- ...-- ....- --..-- ...-- ..... --..-- ...-- -.... --..-- ...-- --... --..-- ...-- ---.. --..-- ...-- ----. --..-- ....- ----- --..-- / ....- .---- --..-- ....- ..--- --..-- ....- ...-- --..-- ....- ....- --..-- ....- ..... --..-- ....- -.... --..-- ....- --... --..-- ....- ---..</data>"
        ),
        8,
        "morse",
        None,
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
        ],
        pytest.raises(ValueError),
    ),
]


@pytest.mark.parametrize(
    "layer_data,width,encoding,compression,expected,raises", layer_data
)
def test_decode_layer_data(layer_data, width, encoding, compression, expected, raises):
    with raises:
        assert (
            xml_parser._decode_tile_layer_data(layer_data, width, encoding, compression)
            == expected
        )


# FIXME: use hypothesis for this
def create_tile_set(qty_of_tiles):
    """ Create tile set of specific size.
    """
    tile_set = objects.TileSet(None, None)

    if qty_of_tiles == 0:
        return tile_set

    tiles = {}

    for tile_id in range(qty_of_tiles):
        tiles[tile_id] = objects.Tile(id_=tile_id)

    tile_set.tiles = tiles

    return tile_set


tile_by_gid = [
    (1, {1: create_tile_set(0)}, None),
    (1, {1: create_tile_set(1)}, objects.Tile(id_=0)),
    (1, {1: create_tile_set(2)}, objects.Tile(id_=0)),
    (2, {1: create_tile_set(1)}, None),
    (10, {1: create_tile_set(10)}, objects.Tile(id_=9)),
    (1, {1: create_tile_set(1), 2: create_tile_set(1)}, objects.Tile(id_=0)),
    (2, {1: create_tile_set(1), 2: create_tile_set(1)}, objects.Tile(id_=0)),
    (3, {1: create_tile_set(1), 2: create_tile_set(1)}, None),
    (15, {1: create_tile_set(5), 6: create_tile_set(10)}, objects.Tile(id_=9)),
    (
        20,
        {1: create_tile_set(5), 6: create_tile_set(10), 16: create_tile_set(10),},
        objects.Tile(id_=4),
    ),
]


@pytest.mark.parametrize("gid,tile_sets,expected", tile_by_gid)
def test_get_tile_by_gid(gid, tile_sets, expected):
    assert utilities.get_tile_by_gid(gid, tile_sets) == expected
