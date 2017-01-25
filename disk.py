# Each piece played is a Disk object

class Disk:
    def __init__(self, center: tuple, radius: tuple, color: str):
        self._center = center
        self._radius = radius
        self._color = color

    def center(self) -> tuple:
        return self._center

    '''def center_to_f(width: int, height: int) -> tuple:
        return (_center[0]*width, _center[1]*height)'''

    def radius(self) -> tuple:
        return self._radius

    def color(self) -> str:
        if self._color == 'W':
            return 'white'
        else:
            return 'black'

    def opposite_color(self) -> str:
        if self._color == 'W':
            return 'black'
        else:
            return 'white'
