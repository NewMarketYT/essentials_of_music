import os
import sys
import warnings
import numpy as np

from manim import *
from sound.assets.creatures.creature import Creature
from .bubbles import ThoughtBubble
from .bubbles import SpeechBubble
from sound.constants import CREATURE_DIR


class RestCreature(Creature):
    LEFT_EYE_INDEX = 0
    LEFT_PUPIL_INDEX = 1
    BODY_INDEX = 2
    RIGHT_EYE_INDEX = 3
    RIGHT_PUPIL_INDEX = 4
    MOUTH_INDEX = 5
    BOUNDINGBOX = 6
    PREFIX = "RestCreature"

    def __init__(self, mode="plain", color=GREY_BROWN, **kwargs):
        self.mode = mode
        self.color = color
        self.stroke_width = 0
        self.stroke_color = BLACK
        self.fill_opacity = 1.0
        self.corner_scale_factor = 0.75
        self.flip_at_start = False
        self.is_looking_direction_purposeful = False
        self.start_corner = None
        self.pupil_to_eye_width_ratio = 0.4
        self.pupil_dot_to_pupil_width_ratio = 0.3
        self.parts_named = False

        super().__init__(RestCreature.PREFIX, self.mode, color=self.color, **kwargs)
        self.set(height=3)
        if self.flip_at_start:
            self.flip()
        if self.start_corner is not None:
            self.to_corner(self.start_corner)

    def name_parts(self):
        self.boundingbox = self.submobjects[RestCreature.BOUNDINGBOX]
        self.mouth = self.submobjects[RestCreature.MOUTH_INDEX]
        self.body = self.submobjects[RestCreature.BODY_INDEX]
        self.pupils = VGroup(
            *[
                self.submobjects[RestCreature.LEFT_PUPIL_INDEX],
                self.submobjects[RestCreature.RIGHT_PUPIL_INDEX],
            ]
        )
        self.eyes = VGroup(
            *[
                self.submobjects[RestCreature.LEFT_EYE_INDEX],
                self.submobjects[RestCreature.RIGHT_EYE_INDEX],
            ]
        )
        self.eye_parts = VGroup(self.eyes, self.pupils)
        self.parts_named = True


class Rest(RestCreature):
    pass
