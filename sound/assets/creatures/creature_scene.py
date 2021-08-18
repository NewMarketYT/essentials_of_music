import itertools as it
import random

from manim import *
from .quarter_creature import Quarter
from .rest_creature import Rest
from .treble_creature import Json
from .treble_creature import Nsoj
from .treble_creature import TrebleCreature
from .creature_animations import Blink
from .creature_animations import CreatureBubbleIntroduction
from .creature_animations import RemoveCreatureBubble
from .bubbles import SpeechBubble
from .bubbles import ThoughtBubble


class CreatureScene(Scene):
    def __init__(
        self,
        total_wait_time=0,
        seconds_to_blink=3,
        creatures_start_on_screen=True,
        creature_corner=DL,
        **kwargs
    ):
        self.total_wait_time = total_wait_time
        self.seconds_to_blink = seconds_to_blink
        self.creatures_start_on_screen = creatures_start_on_screen
        self.creature_corner = creature_corner
        super().__init__(**kwargs)

    def setup(self):
        self.creatures = VGroup(*self.create_creatures())
        self.creature = self.get_primary_creature()
        if self.creatures_start_on_screen:
            self.add(*self.creatures)

    def create_creatures(self):
        """
        Likely updated for subclasses
        """
        return VGroup(self.create_creature())

    def create_creature(self):
        creature = TrebleCreature()
        creature.to_corner(DL)
        return creature

    def add_creature(self, creature):
        self.add(creature)

    def get_creatures(self):
        return self.creatures

    def get_primary_creature(self):
        return self.creatures[0]

    def any_creatures_on_screen(self):
        return len(self.get_on_screen_creatures()) > 0

    def get_on_screen_creatures(self):
        mobjects = self.get_mobject_family_members()
        return VGroup(*[c for c in self.get_creatures() if c in mobjects])

    def introduce_bubble(self, *args, **kwargs):
        if isinstance(args[0], TrebleCreature):
            creature = args[0]
            content = args[1:]
        else:
            creature = self.get_primary_creature()
            content = args

        bubble_class = kwargs.pop("bubble_class", SpeechBubble)
        target_mode = kwargs.pop(
            "target_mode", "thinking" if bubble_class is ThoughtBubble else "speaking"
        )
        bubble_kwargs = kwargs.pop("bubble_kwargs", {})
        bubble_removal_kwargs = kwargs.pop("bubble_removal_kwargs", {})
        added_anims = kwargs.pop("added_anims", [])

        anims = []
        on_screen_mobjects = self.camera.get_mobjects_to_display(self.mobjects)

        def has_bubble(creature):
            return (
                hasattr(creature, "bubble")
                and creature.bubble is not None
                and creature.bubble in on_screen_mobjects
            )

        creatures_with_bubbles = list(filter(has_bubble, self.get_creatures()))
        if creature in creatures_with_bubbles:
            creatures_with_bubbles.remove(creature)
            old_bubble = creature.bubble
            bubble = creature.get_bubble(
                *content, bubble_class=bubble_class, **bubble_kwargs
            )
            anims += [
                ReplacementTransform(old_bubble, bubble),
                ReplacementTransform(old_bubble.content, bubble.content),
                creature.change_mode,
                target_mode,
            ]
        else:
            anims.append(
                CreatureBubbleIntroduction(
                    creature,
                    *content,
                    bubble_class=bubble_class,
                    bubble_kwargs=bubble_kwargs,
                    target_mode=target_mode,
                    **kwargs,
                )
            )
        anims += [
            RemoveCreatureBubble(c, **bubble_removal_kwargs)
            for c in creatures_with_bubbles
        ]
        anims += added_anims

        return anims

    def creature_says(self, *args, **kwargs):
        return self.introduce_bubble(*args, bubble_class=SpeechBubble, **kwargs)

    def creature_thinks(self, *args, **kwargs):
        self.introduce_bubble(*args, bubble_class=ThoughtBubble, **kwargs)

    def say(self, *content, **kwargs):
        self.creature_says(self.get_primary_creature(), *content, **kwargs)

    def think(self, *content, **kwargs):
        self.creature_thinks(self.get_primary_creature(), *content, **kwargs)

    def compile_play_args_to_animation_list(self, *args, **kwargs):
        """
        Add animations so that all pi creatures look at the
        first mobject being animated with each .play call
        """
        animations = Scene.compile_play_args_to_animation_list(self, *args, **kwargs)
        anim_mobjects = Group(*[a.mobject for a in animations])
        all_movers = anim_mobjects.get_family()
        if not self.any_creatures_on_screen():
            return animations

        creatures = self.get_on_screen_creatures()
        non_creature_anims = [
            anim
            for anim in animations
            if len(set(anim.mobject.get_family()).intersection(creatures)) == 0
        ]
        if len(non_creature_anims) == 0:
            return animations
        first_anim = non_creature_anims[0]
        main_mobject = first_anim.mobject
        for creature in creatures:
            if creature not in all_movers:
                animations.append(
                    ApplyMethod(
                        creature.look_at,
                        main_mobject,
                    )
                )
        return animations

    def blink(self):
        self.play(Blink(random.choice(self.get_on_screen_creatures())))

    def joint_blink(self, creatures=None, shuffle=True, **kwargs):
        if creatures is None:
            creatures = self.get_on_screen_creatures()
        creatures_list = list(creatures)
        if shuffle:
            random.shuffle(creatures_list)

        def get_rate_func(pi):
            index = creatures_list.index(pi)
            proportion = float(index) / len(creatures_list)
            start_time = 0.8 * proportion
            return squish_rate_func(there_and_back, start_time, start_time + 0.2)

        self.play(
            *[Blink(pi, rate_func=get_rate_func(pi), **kwargs) for pi in creatures_list]
        )
        return self

    def wait(self, time=1, blink=True, **kwargs):
        if "stop_condition" in kwargs:
            self.non_blink_wait(time, **kwargs)
            return
        while time >= 1:
            time_to_blink = self.total_wait_time % self.seconds_to_blink == 0
            if blink and self.any_creatures_on_screen() and time_to_blink:
                self.blink()
            else:
                self.non_blink_wait(**kwargs)
            time -= 1
            self.total_wait_time += 1
        if time > 0:
            self.non_blink_wait(time, **kwargs)
        return self

    def non_blink_wait(self, time=1, **kwargs):
        Scene.wait(self, time, **kwargs)
        return self

    def change_mode(self, mode):
        self.play(self.get_primary_creature().change_mode, mode)

    def look_at(self, thing_to_look_at, creatures=None, **kwargs):
        if creatures is None:
            creatures = self.get_creatures()
        args = list(it.chain(*[[c.look_at, thing_to_look_at] for c in creatures]))
        self.play(*args, **kwargs)


class ClassScene(CreatureScene):
    def __init__(
        self, teacher_color=BLUE, seconds_to_blink=2, screen_height=3, **kwargs
    ):
        self.teacher_color = teacher_color
        self.seconds_to_blink = (seconds_to_blink,)
        self.screen_height = screen_height
        self.student_colors = [BLUE, BLUE_B, PINK, BLUE_A]
        self.student_scale_factor = 0.75
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.screen = ScreenRectangle(height=self.screen_height)
        self.screen.to_corner(UP + LEFT)
        self.hold_up_spot = self.teacher.get_corner(UL) + MED_LARGE_BUFF * UP

    def create_creatures(self):
        self.teacher = Json(color=self.teacher_color)
        self.teacher.to_corner(DL).shift(DOWN * 0.25)
        self.teacher.look(DR) 
        self.students = VGroup(
            *[Quarter(color=self.student_colors[-1])]
            + [Rest(color=GREY)]
            + [Quarter(color=c) for c in self.student_colors[:-1]]
        )
        self.students.arrange(LEFT, buff=1.5)
        self.students.scale(self.student_scale_factor)
        self.students.to_edge(RIGHT).shift(DOWN * 1.05)
        self.students[0].shift(UP * .3)
        self.teacher.look_at(self.students[-1].eyes)
        for student in self.students:
            student.look_at(self.teacher.eyes)

        return [self.teacher] + list(self.students)

    def get_teacher(self):
        return self.teacher

    def get_students(self):
        return self.students

    def teacher_says(self, *content, **kwargs):
        return self.creature_says(self.get_teacher(), *content, **kwargs)

    def student_says(self, *content, **kwargs):
        if "target_mode" not in kwargs:
            target_mode = random.choice(
                [
                    "raise_right_hand",
                    "raise_left_hand",
                ]
            )
            kwargs["target_mode"] = target_mode
        if "bubble_kwargs" not in kwargs:
            kwargs["bubble_kwargs"] = {"direction": LEFT}
        student = self.get_students()[kwargs.get("student_index", 2)]
        return self.creature_says(student, *content, **kwargs)

    def teacher_thinks(self, *content, **kwargs):
        return self.creature_thinks(self.get_teacher(), *content, **kwargs)

    def student_thinks(self, *content, **kwargs):
        student = self.get_students()[kwargs.get("student_index", 2)]
        return self.creature_thinks(student, *content, **kwargs)

    def change_all_student_modes(self, mode, **kwargs):
        self.change_student_modes(*[mode] * len(self.students), **kwargs)

    def change_student_modes(self, *modes, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        self.play(self.get_student_changes(*modes, **kwargs), *added_anims)

    def get_student_changes(self, *modes, **kwargs):
        pairs = list(zip(self.get_students(), modes))
        pairs = [(s, m) for s, m in pairs if m is not None]
        start = VGroup(*[s for s, m in pairs])
        target = VGroup(*[s.copy().change_mode(m) for s, m in pairs])
        if "look_at_arg" in kwargs:
            for student in target:
                student.look_at(kwargs["look_at_arg"])
        anims = [Transform(s, t) for s, t in zip(start, target)]
        return LaggedStart(
            *anims,
            lag_ratio=kwargs.get("lag_ratio", 0.15),
            run_time=1,
        )


class MusicScene(ClassScene):
    def __init__(self, teacher_color=GREY_BROWN):
        super().__init__(teacher_color=teacher_color)

    def setup(self):
        l1 = Line(LEFT * frame.frame_width / 2, RIGHT * frame.frame_width / 2)
        l2 = Line(LEFT * frame.frame_width / 2, RIGHT * frame.frame_width / 2).next_to(
            l1, 3 * DOWN
        )
        l3 = Line(LEFT * frame.frame_width / 2, RIGHT * frame.frame_width / 2).next_to(
            l2, 3 * DOWN
        )
        l4 = Line(LEFT * frame.frame_width / 2, RIGHT * frame.frame_width / 2).next_to(
            l3, 3 * DOWN
        )
        l5 = Line(LEFT * frame.frame_width / 2, RIGHT * frame.frame_width / 2).next_to(
            l4, 3 * DOWN
        )
        self.staff = VGroup(*[l1, l2, l3, l4, l5]).move_to(ORIGIN).shift(DOWN).set_color(DARK_GREY)
        self.add(self.staff)
        super().setup()
