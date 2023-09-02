from turtle import position
from manim import *

__all__ = ["SpeechBubble", "ThoughtBubble"]

MEDIA_DIR = "../assets/creatures/svg_images/"


class Bubble(SVGMobject):
    def __init__(
        self,
        file_name,
        direction=LEFT,
        center_point=ORIGIN,
        content_scale_factor=0.75,
        bubble_center_adjustment_factor = 1.0 / 8,
        width=6,
        height=3,
        fill_opacity = 0.8,
        stroke_width = 3,
        **kwargs
    ):
        self.file_name = file_name
        self.direction = direction
        self.center_point = center_point
        self.content_scale_factor = content_scale_factor
        self.bubble_center_adjustment_factor = bubble_center_adjustment_factor
        self.fill_opacity = fill_opacity
        self.stroke_width = stroke_width
        super().__init__(self.file_name, **kwargs)
        self.set(height=height)
        self.set(width=width)
        self.center()
        self.stretch_to_fit_height(self.height)
        self.stretch_to_fit_width(self.width)
        if self.direction[0] > 0:
            self.flip()
        self.direction_was_specified = "direction" in kwargs
        self.content = Mobject()

    def get_tip(self):
        return self.get_corner(DOWN + self.direction)

    def get_bubble_center(self):
        factor = self.bubble_center_adjustment_factor
        return self.get_center() + factor * self.get_height() * UP

    def move_tip_to(self, point, content):
        mover = VGroup(self)
        if content is not None:
            mover.add(content)
        mover.shift(point - self.get_tip())
        return self

    def flip(self, axis=UP):
        Mobject.flip(self, axis=axis)
        if abs(axis[1]) > 0:
            self.direction = -np.array(self.direction)
        return self

    def pin_to(self, mobject):
        mob_center = mobject.get_center()
        want_to_flip = np.sign(mob_center[0]) != np.sign(self.direction[0])
        can_flip = not self.direction_was_specified
        if want_to_flip and can_flip:
            self.flip()
            self.content.flip()
        boundary_point = mobject.get_critical_point(UP - self.direction)
        vector_from_center = 1.0 * (boundary_point - mob_center)
        self.move_tip_to((mob_center + vector_from_center), self.content)
        return self

    def position_mobject_inside(self, mobject):
        scaled_width = self.content_scale_factor * self.get_width()
        if mobject.get_width() > scaled_width:
            mobject.set_width(scaled_width)
        mobject.shift(self.get_bubble_center() - mobject.get_center())
        return mobject

    def add_content(self, mobject):
        self.position_mobject_inside(mobject)
        self.add(mobject)
        self.content = mobject
        return self

    def write(self, *text):
        self.add_content(Text(*text))
        return self

    def resize_to_content(self, content):
        target_width = content.get_width()
        target_width += max(MED_LARGE_BUFF, 2)
        target_height = content.get_height()
        target_height += 2.5 * MED_LARGE_BUFF
        tip_point = self.get_tip()
        self.stretch_to_fit_width(target_width)
        self.stretch_to_fit_height(target_height)
        self.move_tip_to(tip_point, content)
        self.position_mobject_inside(content)

    def clear(self):
        self.add_content(VMobject())
        return self


class SpeechBubble(Bubble):
    def __init__(self, **kwargs):
        super().__init__(MEDIA_DIR + "Bubbles_speech.svg", **kwargs)
        self.color = WHITE


class ThoughtBubble(Bubble):
    def __init__(self, **kwargs):
        super().__init__(MEDIA_DIR + "Bubbles_thought.svg", **kwargs)
