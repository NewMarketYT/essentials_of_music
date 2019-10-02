from manim.constants import *
from manim.mobject.svg.svg_mobject import SVGMobject
from manim.mobject.types.vectorized_mobject import VGroup


class Creature(SVGMobject):
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        width = 3
        height = 2

