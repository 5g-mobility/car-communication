from pygeotile.point import Point
from pygeotile.tile import Tile    


def geoTiles_conveter(position):
    """
        converter geo coordenadas para quadTrees

    """
    lat, lon = position
 

    tile = Tile.for_latitude_longitude(latitude=lat, longitude=lon, zoom=18)

    return tile.quad_tree