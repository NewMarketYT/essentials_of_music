from manim.animation.animation import Animation
from manim.animation.composition import AnimationGroup
from manim.animation.fading import FadeOut
from manim.animation.creation import DrawBorderThenFill, Create
from manim.animation.creation import Write
from manim.animation.transform import ApplyMethod
from manim.animation.transform import MoveToTarget
from manim.constants import *
from manim.utils.color import *
from manim.mobject.mobject import Group
from manim.utils.rate_functions import squish_rate_func
from manim.utils.rate_functions import there_and_back
from .bubbles import SpeechBubble
from .creature import *


class Blink(ApplyMethod):
    def __init__(self, creature, **kwargs):
        self.rate_func = squish_rate_func(there_and_back)
        ApplyMethod.__init__(self, creature.blink, **kwargs)


class CreatureBubbleIntroduction(AnimationGroup):
    def __init__(self, creature, *content, **kwargs):
        self.target_mode = kwargs["target_mode"]
        self.bubble_class = SpeechBubble
        self.change_mode_kwargs = {}
        self.bubble_creation_class = Create
        self.bubble_creation_kwargs = {}
        self.bubble_kwargs = {}
        self.content_introduction_class = DrawBorderThenFill
        self.content_introduction_kwargs = {}
        self.look_at_arg = None
        bubble = creature.get_bubble(
            *content, bubble_class=self.bubble_class, **self.bubble_kwargs
        )
        Group(bubble, bubble.content).shift_onto_screen()

        creature.generate_target()
        creature.target.change_mode(self.target_mode)
        if self.look_at_arg is not None:
            creature.target.look_at(self.look_at_arg)

        change_mode = MoveToTarget(creature, **self.change_mode_kwargs)
        bubble_creation = self.bubble_creation_class(
            bubble, **self.bubble_creation_kwargs
        )
        content_introduction = self.content_introduction_class(
            bubble.content, **self.content_introduction_kwargs
        )
        AnimationGroup.__init__(
            self, change_mode, bubble_creation, content_introduction, **kwargs
        )


class CreatureSays(CreatureBubbleIntroduction):
    def __init__(self):
        super().__init__()


class RemoveCreatureBubble(AnimationGroup):
    def __init__(self, creature, **kwargs):
        self.target_mode = "plain"
        self.look_at_arg = None
        self.remover = True
        assert hasattr(creature, "bubble")

        creature.generate_target()
        creature.target.change_mode(self.target_mode)
        if self.look_at_arg is not None:
            creature.target.look_at(self.look_at_arg)

        AnimationGroup.__init__(
            self,
            MoveToTarget(creature),
            FadeOut(creature.bubble),
            FadeOut(creature.bubble.content),
        )

    def clean_up_from_scene(self, scene=None):
        AnimationGroup.clean_up_from_scene(self, scene)
        self.creature.bubble = None
        if scene is not None:
            scene.add(self.creature)


class FlashThroughClass(Animation):
    def __init__(self, mobject, mode="linear", **kwargs):
        self.highlight_color = GREEN
        if not isinstance(mobject, Creature):
            raise Exception("FlashThroughClass mobject must be a PiCreatureClass")
        self.indices = list(range(mobject.height * mobject.width))
        if mode == "random":
            np.random.shuffle(self.indices)
        Animation.__init__(self, mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        index = int(np.floor(alpha * self.mobject.height * self.mobject.width))
        for pi in self.mobject:
            pi.set_color(BLUE_E)
        if index < self.mobject.height * self.mobject.width:
            self.mobject[self.indices[index]].set_color(self.highlight_color)
