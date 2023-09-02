import os
import sys
import warnings
import numpy as np

from manim import *
from .bubbles import ThoughtBubble
from .bubbles import SpeechBubble
from .creature import Creature
from sound.constants import CREATURE_DIR


class QuarterCreature(Creature):
    LEFT_EYE_INDEX = 0
    RIGHT_EYE_INDEX = 1
    LEFT_PUPIL_INDEX = 2
    RIGHT_PUPIL_INDEX = 3
    TAIL_INDEX = 4
    BODY_INDEX = 5
    MOUTH_INDEX = 6
    BOUNDING_BOX = 7
    PREFIX = "QuarterCreature"

    def __init__(self, mode="plain", color=GREY_BROWN, **kwargs):
        self.mode = mode
        self.fill_opacity = 1.0
        self.corner_scale_factor = 1
        self.flip_at_start = False
        self.is_looking_direction_purposeful = False
        self.start_corner = None
        self.pupil_to_eye_width_ratio = 0.4
        self.pupil_dot_to_pupil_width_ratio = 0.3
        self.parts_named = False

        super().__init__(QuarterCreature.PREFIX, self.mode, color=color, **kwargs)
        self.init_body()
        self.set(height=4)
        if self.flip_at_start:
            self.flip()
        if self.start_corner is not None:
            self.to_corner(self.start_corner)

    def init_body(self):
        if not self.parts_named:
            self.name_parts()
        self.boundingbox.set_fill(WHITE, opacity=0)
        self.mouth.set_fill(BLACK, opacity=1)
        self.body.set_fill(self.color, opacity=1)
        self.eyes.set_fill(WHITE, opacity=1)
        self.init_pupils()

    def name_parts(self):
        self.boundingbox = self.submobjects[QuarterCreature.BOUNDING_BOX]
        self.mouth = self.submobjects[QuarterCreature.MOUTH_INDEX]
        self.body = VGroup(
            *[
                self.submobjects[QuarterCreature.TAIL_INDEX],
                self.submobjects[QuarterCreature.BODY_INDEX],
            ]
        )
        self.pupils = VGroup(
            *[
                self.submobjects[QuarterCreature.LEFT_PUPIL_INDEX],
                self.submobjects[QuarterCreature.RIGHT_PUPIL_INDEX],
            ]
        )
        self.eyes = VGroup(
            *[
                self.submobjects[QuarterCreature.LEFT_EYE_INDEX],
                self.submobjects[QuarterCreature.RIGHT_EYE_INDEX],
            ]
        )
        self.eye_parts = VGroup(self.eyes, self.pupils)
        self.parts_named = True

    def get_bubble(self, *content, **kwargs):
        bubble_class = kwargs.pop("bubble_class", SpeechBubble)
        bubble = bubble_class(**kwargs)
        bubble.set_fill(BLACK, .75)
        if len(content) > 0:
            if isinstance(content[0], str):
                content_mob = Text(*content, color=YELLOW)
            else:
                content_mob = content[0]
            if "height" not in kwargs and "width" not in kwargs:
                bubble.resize_to_content(content_mob)
            bubble.add_content(content_mob)
        dot = Dot().move_to(self)
        bubble.pin_to(dot)
        self.bubble = bubble
        return bubble


class Quarter(QuarterCreature):
    pass
