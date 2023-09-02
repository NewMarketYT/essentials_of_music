import os
import sys
import warnings
import numpy as np

from manim import *
from .creature import Creature
from sound.constants import CREATURE_DIR


class TrebleCreature(Creature):
    BODY_INDEX = 0
    TAIL_INDEX = 1
    LEFT_EYE_INDEX = 2
    RIGHT_EYE_INDEX = 3
    LEFT_PUPIL_INDEX = 4
    RIGHT_PUPIL_INDEX = 5
    MOUTH_INDEX = 6
    BOUNDING_BOX = 7
    PREFIX = "TrebleCreature"

    def __init__(self, mode="plain", color=GREY_BROWN, **kwargs):
        self.mode = mode
        self.stroke_width = 1
        self.fill_opacity = 1.0
        self.corner_scale_factor = 0.75
        self.flip_at_start = False
        self.is_looking_direction_purposeful = False
        self.start_corner = None
        self.pupil_to_eye_width_ratio = 0.4
        self.pupil_dot_to_pupil_width_ratio = 0.3
        self.parts_named = False

        super().__init__(TrebleCreature.PREFIX, mode=self.mode, color=color, **kwargs)
        self.set(height=6)
        if self.flip_at_start:
            self.flip()
        if self.start_corner is not None:
            self.to_corner(self.start_corner)

    def name_parts(self):
        self.boundingbox = self.submobjects[TrebleCreature.BOUNDING_BOX]
        self.mouth = self.submobjects[TrebleCreature.MOUTH_INDEX]
        self.body = VGroup(
            *[
                self.submobjects[TrebleCreature.BODY_INDEX],
                self.submobjects[TrebleCreature.TAIL_INDEX],
            ]
        )
        self.pupils = VGroup(
            *[
                self.submobjects[TrebleCreature.LEFT_PUPIL_INDEX],
                self.submobjects[TrebleCreature.RIGHT_PUPIL_INDEX],
            ]
        )
        self.eyes = VGroup(
            *[
                self.submobjects[TrebleCreature.LEFT_EYE_INDEX],
                self.submobjects[TrebleCreature.RIGHT_EYE_INDEX],
            ]
        )
        self.eye_parts = VGroup(self.eyes, self.pupils)
        self.parts_named = True


class Json(TrebleCreature):
    pass


class Nsoj(TrebleCreature):
    def __init__(self):
        super().__init__(color=GREY_BROWN, flip_at_start=True)
