from math import cos
from operator import index, sub
from typing_extensions import runtime
from manim import *
from manim.mobject.geometry import ArrowTriangleFilledTip
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLCamera
from numpy.lib.function_base import select
from sound import *
from manim_physics.wave import *


# Created with Manim v0.8.0
# class NewMarketLogo(GraphScene, MovingCameraScene):
#     def setup(self):
#         GraphScene.setup(self)
#         MovingCameraScene.setup(self)

#     def construct(self):
#         self.axes_color = BLACK
#         self.x_min = -3
#         self.x_max = 3
#         self.y_min = -3
#         self.y_max = 3
#         self.x_axis_width = 6
#         self.y_axis_height = 6
#         self.graph_origin = np.array([0, 0, 0])
#         self.x_axis_label = ""
#         self.y_axis_label = ""
#         self.camera.frame.save_state()
#         self.setup_axes(animate=False)

#         def stock_curve(x):
#             return (x - 0.125) ** 4 * (x + 1.875)

#         graph = self.get_graph(stock_curve, color=BLUE, x_min=-4, x_max=3)
#         deriv_graph = self.get_derivative_graph(graph)
#         dolly = self.get_graph(stock_curve, color=BLACK, x_min=-3, x_max=0)

#         def candlesticks(x):
#             coord = self.input_to_graph_point(x, graph)
#             before_coord = self.input_to_graph_point(x - 0.45, graph)
#             after_coord = self.input_to_graph_point(x + 0.45, graph)
#             deriv_coord = self.input_to_graph_point(x, deriv_graph)
#             color = GREEN
#             thin_top = after_coord[1]
#             thin_bot = before_coord[1]
#             if deriv_coord[1] < 0:
#                 color = RED
#                 tmp = thin_top
#                 thin_top = thin_bot
#                 thin_bot = tmp
#             height = coord[1]
#             if x == -2:
#                 height *= 2.5

#             r = Rectangle(
#                 fill_opacity=1, color=color, width=0.1, height=height
#             ).move_to(RIGHT * coord[0] + UP * coord[1])
#             top = Line(color=color, start=coord, end=(coord[0], thin_top, 0))
#             bot = Line(color=color, start=coord, end=(coord[0], thin_bot, 0))
#             return VGroup(r, top, bot)

#         sticks = [candlesticks(x) for x in range(-2, 2)]
#         sticks.pop(2)
#         moving_dot = Dot(fill_opacity=0).move_to(dolly.points[0])
#         self.add(moving_dot)
#         self.camera.frame.scale(0.5).move_to(moving_dot)
#         self.add(self.camera.frame)

#         def update_curve(mob):
#             mob.move_to(moving_dot.get_center())

#         self.camera.frame.add_updater(update_curve)
#         candles = VGroup(*sticks)
#         logo = SVGMobject("newmarket.svg").scale(0.5).move_to(0.5 * UP)
#         logo.submobjects[0].set(stroke_width=0)
#         logo.submobjects[1].set(stroke_width=0)
#         self.play(
#             AnimationGroup(
#                 MoveAlongPath(moving_dot, dolly, rate_func=ease_out_cubic, run_time=3),
#                 Write(graph, run_time=2.5, rate_func=ease_in_out_circ),
#                 Write(candles, run_time=4),
#             ),
#             Write(logo, run_time=3, rate_func=rush_into),
#         )
#         self.camera.frame.remove_updater(update_curve)

#         self.play(
#             AnimationGroup(
#                 Uncreate(graph),
#                 Uncreate(candles),
#                 logo.animate.shift(0.15 * DOWN),
#                 logo.submobjects[2].animate.set_fill(BLACK).shift(0.15 * DOWN),
#             ),
#             self.camera.frame.animate.scale(0.005),
#         )
#         self.wait()


class Chapter1Opening(Scene):
    def construct(self):

        line = "If I were not a physicist,"
        line1 = "I would probably be a musician."
        line2 = "I often think in music."
        line3 = "I live my daydreams in music."
        line4 = "I see my life in terms of music."
        hl = {"physicist": RED}
        hl1 = {"musician": ORANGE}
        hl2 = {"music": YELLOW}
        hl3 = {"music": GREEN}
        hl4 = {"music": BLUE}

        def tex_quote(line, hlt={}, max_width=config.frame_width - 1):
            quote = line.split()
            quote = Tex(*quote, tex_to_color_map=hlt, arg_separator=" ")
            quote[-1].shift(0.2 * LEFT)
            if quote.width > max_width:
                quote.scale_to_fit_width(max_width)
            return quote

        line = tex_quote(line, hl)
        line1 = tex_quote(line1, hl1)
        line2 = tex_quote(line2, hl2)
        line3 = tex_quote(line3, hl3)
        line4 = tex_quote(line4, hl4)
        line.to_edge(UP, buff=2)
        line1.next_to(line, DOWN).align_to(line, RIGHT)
        line2.next_to(line1, DOWN).align_to(line1, RIGHT)
        line3.next_to(line2, DOWN).align_to(line2, RIGHT)
        line4.next_to(line3, DOWN).align_to(line2, RIGHT)
        self.play(
            LaggedStart(
                Write(line),
                Write(line1),
                Write(line2),
                Write(line3),
                Write(line4),
                lag_ratio=0.75,
            )
        )
        author = "Albert Einstein"
        author = Tex("— " + author)
        author.next_to(line4, DOWN).align_to(line4, RIGHT)
        author.set_color(PURPLE)

        self.wait()
        self.play(Write(author), run_time=2, rate=smooth)
        quote = VGroup(line, line1, line2, line3, line4, author)
        self.wait()

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
        staff = (
            VGroup(*[l1, l2, l3, l4, l5]).move_to(ORIGIN).shift(DOWN).set_color(WHITE)
        )
        self.play(ReplacementTransform(quote, staff))
        self.wait()


class Introduction2(MusicScene):
    def __init__(self):
        super().__init__(GREY_BROWN)

    def construct(self):
        self.show_series()
        self.empower_audience()
        self.show_ideas()
        self.show_outline()

    def show_series(self):
        self.staff.set_color(WHITE)
        self.series = VideoSeries(num_videos=5)
        self.series.to_edge(UP)
        this_video = self.series[0]
        this_video.set_color(YELLOW)
        this_video.save_state()
        elip = MathTex(r"\cdots").set(width=self.series[-1].width*.9).move_to(self.series[-1])
        self.series[-1] = elip
        for v in self.series[1:]:
            v.save_state()
        self.series[1:].shift(RIGHT * 14)
        self.add(self.series)
        this_video.animate.restore()
        words = Tex("Welcome to \\\\", "Essentials of Music")
        words.set_color_by_tex("Essentials of Music", YELLOW)
        self.teacher.change_mode("happy")
        self.play(
            Blink(self.teacher),
        )
        self.teacher_says(words, target_mode="hooray")

        essence_words = words.get_part_by_tex("Essentials").copy()
        self.remove(words[-1])
        self.play(
            AnimationGroup(
                Uncreate(self.teacher.bubble),
                Unwrite(self.teacher.bubble.content[:-1]),
                essence_words.animate.move_to(ORIGIN + UP),
            ),
            self.staff.animate.set_color(DARK_GRAY),
            run_time=1,
            lag_ratio=0.2,
        )
        self.play(
            AnimationGroup(*[v.animate.restore() for v in self.series[1:]], lag_ratio=.2),
            run_time=2,
        )
        self.change_student_modes(
            *["pondering", "hooray", "plain", "happy", "hooray"],
            look_at_arg=self.series[1].get_left(),
            lag_ratio=0.04,
        )
        self.play(
            *[
                ApplyMethod(
                    video.shift,
                    0.25 * video.height * UP,
                    run_time=3,
                    rate_func=squish_rate_func(there_and_back, alpha, alpha + 0.3),
                )
                for video, alpha in zip(self.series, np.linspace(0, 0.7, len(self.series)))
            ],
            self.teacher.animate.change_mode("happy"),
        )

        # Favor Scientist
        self.play(
            self.students[4].animate.change_mode("plain"),
            self.students[3].animate.change_mode("happy"),
            self.students[2]
            .animate.change_mode("hooray")
            .make_eye_contact(self.teacher),
            self.students[1].animate.change_mode("plain"),
            self.students[0].animate.change_mode("happy"),
        )
        # Engineer
        self.play(
            self.students[4].animate.change_mode("erm"),
            self.students[3].animate.change_mode("hooray"),
            self.students[2].animate.change_mode("happy"),
            self.students[1].animate.change_mode("plain"),
            self.students[0]
            .animate.change_mode("hooray")
            .make_eye_contact(self.teacher),
        )
        # Musician
        self.play(
            self.students[4]
            .animate.change_mode("hooray")
            .make_eye_contact(self.teacher),
            self.students[3].animate.change_mode("happy"),
            self.students[2].animate.change_mode("happy"),
            self.students[1].animate.change_mode("hooray"),
            self.students[0].animate.change_mode("happy"),
        )
        self.wait()
        self.play(
            self.students[2].animate.change_mode("erm"),
            self.students[3].animate.change_mode("erm"),
        )
        self.play(
            self.students[2].animate.look_at(7*RIGHT),
            self.students[3].animate.look_at(7*RIGHT),
            rate_func=there_and_back
        )

        self.essence_words = essence_words

    def show_ideas(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{musicography}")
        self.cof = ImageMobject("Circle_of_fifths_deluxe_4.png")
        self.timesig = Tex(r"\musMeter{15}{16}", tex_template=myTemplate)
        self.doremi = Tex("Do", ", ", "Re", ", ", "Mi...")
        self.audio = SVGMobject("Audio.svg", color=YELLOW)
        self.audio[0].set_color(GRAY)
        self.audio[1].set_color(YELLOW)
        self.rules = [self.timesig, self.doremi, self.cof, self.audio]
        video_indices = [3, 1, 2, 0]
        alt_rules_list = list(self.rules[1:]) + [
            VectorizedPoint(self.teacher.eyes.get_top())
        ]
        for last_rule, rule, video_index in zip(self.rules, alt_rules_list, video_indices):
            video = self.series[video_index]
            last_rule.move_to(video)
            if last_rule.width <= last_rule.height:
                last_rule.set(height=video.height * 0.85)
            else:
                last_rule.set(width=video.width * 0.85)
            last_rule.save_state()
        self.audio.scale(1.5).next_to(self.teacher, RIGHT)
        self.timesig.scale(2).next_to(self.teacher, RIGHT)
        self.doremi.scale(3.5).next_to(self.teacher, RIGHT)
        self.cof.scale(3.5).next_to(self.teacher, RIGHT)
        self.play(
            self.teacher.animate.change_mode("pondering"),
        )
        for last_rule, rule, video_index in zip(self.rules, alt_rules_list, video_indices):
            video = self.series[video_index]
            if type(last_rule) == Tex:
                self.play(
                    Write(last_rule),
                    *[s.animate.look_at(last_rule) for s in self.students]
                    )
            else:
                self.play(
                    FadeIn(last_rule),
                    *[s.animate.look_at(last_rule) for s in self.students]
                )
            self.wait()
            self.play(
                last_rule.animate.restore(),
                FadeOut(self.series[video_index].submobjects[0]),
                *[s.animate.look_at(video) for s in self.students]
            )
            self.change_student_modes(*["pondering"] * 5, look_at_arg=last_rule)
        self.wait(2)
        self.joint_blink()
        self.wait()

    def empower_audience(self):
        you = self.students[3]
        self.students.remove(you)

        music = VGroup(*self.essence_words[-len("music") :].copy())
        music.generate_target()
        create = Tex("Create")
        create_music = VGroup(create, music.target)
        create_music.arrange(RIGHT, buff=MED_SMALL_BUFF)
        create_music.next_to(you, UP)

        fader = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.5,
            stroke_opacity=0,
        )
        self.add(fader, you)

        self.play(
            FadeIn(fader),
            FadeOut(self.essence_words),
            MoveToTarget(music),
            ApplyMethod(you.change_mode, "startled"),
            lag_ratio=0.25,
        )
        self.play(Write(create), you.animate.look_at(music))
        arrow = Arrow(music, you.get_center())
        arrow.set_color(color=YELLOW)
        self.play(Create(arrow), you.animate.change_mode("happy"))

        self.wait(1)
        self.play(Uncreate(arrow), Unwrite(create), Unwrite(music), FadeOut(fader))
        self.students.add(you)
        self.add(self.students)

    def show_outline(self):
        prev_video = self.series[0]
        self.play(
            FadeOut(self.staff),
            FadeOut(self.creatures),
            *[FadeOut(self.series[i][1]) for i in range(1,len(self.series)-1)],
            FadeOut(self.series[-1]),
            *[FadeOut(self.rules[i]) for i in range(len(self.rules))]
        )
        this_video = self.series[0]
        this_video[0].set_opacity(0)
        self.play(this_video.animate.move_to(ORIGIN).set(width=config.frame_width-1))
        section1 = Tex("What is sound?")
        section2 = Tex("How is sound made?").next_to(section1,DOWN).align_to(section1, LEFT)
        section3= Tex("Auditory perception").next_to(section2,DOWN).align_to(section1, LEFT)
        section4= Tex("Geometric basis of sound").next_to(section3,DOWN).align_to(section1, LEFT)
        section5= Tex("The wave equation").next_to(section4, DOWN).align_to(section1, LEFT)
        sections = VGroup(section1,section2, section3, section4, section5).move_to(ORIGIN)
        physics_b = BraceBetweenPoints(section1.get_corner(UL), section2.get_corner(DL), LEFT)
        bio_b = Brace(section3,LEFT)
        math_b = BraceBetweenPoints(section4.get_corner(UL), section5.get_corner(DL), LEFT)
        physics = Text("Physics", gradient=(RED,BLUE)).next_to(physics_b, LEFT)
        biology = Text("Biology", color=GREEN).next_to(bio_b, LEFT)
        math = Text("Math", color=WHITE).next_to(math_b, LEFT)
        braces = VGroup(VGroup(physics, physics_b), VGroup(biology, bio_b), VGroup(math, math_b))
        whole = VGroup(braces, sections).arrange()
        self.play(Write(sections))
        self.play(Write(braces))
        self.wait()



class WhatsInStore(Scene):
    def construct(self):
        frame = Rectangle(height=9, width=16, color=WHITE)
        frame.set_height(1.5 * config["frame_y_radius"])

        colors = iter(color_gradient([BLUE, YELLOW], 3))
        titles = [
            Text("Chapter %d:" % d, s).to_edge(UP).set_color(next(colors))
            for d, s in [
                (2, "Divisions of Sound"),
                (3, "Harmony and Unharmony"),
                (4, "Limits"),
            ]
        ]
        title = titles[0]

        frame.next_to(title, DOWN)

        self.add(frame, title)
        self.wait(3)
        for next_title in titles[1:]:
            self.play(Transform(title, next_title))
            self.wait(3)


class Keyboard(VGroup):
    def __init__(self, number_of_keys, start, **kwargs):
        VGroup.__init__(self, **kwargs)
        if number_of_keys <= 0:
            raise Exception("Number of keys must be positive")
        self.number_of_keys = int(number_of_keys)
        keys_to_start_index = {
            "c": 0,
            "c#": 1,
            "dflat": 1,
            "d": 2,
            "d#": 3,
            "eflat": 3,
            "e": 4,
            "fflat": 4,
            "e#": 5,
            "f": 5,
            "f#": 6,
            "gflat": 6,
            "g": 7,
            "g#": 8,
            "aflat": 8,
            "a": 9,
            "a#": 10,
            "bflat": 10,
            "b": 11,
            "b#": 0,
        }
        self.start = keys_to_start_index[start.lower()]
        white_keys = set([0, 2, 4, 5, 7, 9, 11])
        black_keys = set([1, 3, 6, 8, 10])
        prev_white_key = Point()
        counter = 0
        black_keys = []
        while True:
            rectangle = None
            if (counter + self.start) % 12 in white_keys:
                big_rectangle = (
                    Rectangle(height=1, width=0.2, stroke_opacity=1)
                    .next_to(prev_white_key, 0.1 * RIGHT)
                    .set_fill(WHITE, 1)
                )
                prev_white_key = big_rectangle
                self.add(prev_white_key)
            else:
                black_key = None
                if type(prev_white_key) == Point:
                    black_key = (
                        Rectangle(
                            height=2 / 3.0, width=0.125, color=BLACK, stroke_opacity=1
                        )
                        .move_to(
                            prev_white_key.get_center()
                            + 0.02 * RIGHT
                            + 0.25 * UP
                            - 1 / 12.0 * UP
                        )
                        .set_fill(BLACK, 1)
                    )
                else:
                    black_key = (
                        Rectangle(
                            height=2 / 3.0, width=0.125, color=BLACK, stroke_opacity=1
                        )
                        .move_to(
                            prev_white_key.get_center()
                            + 0.1125 * RIGHT
                            + 0.25 * UP
                            - 1 / 12.0 * UP
                        )
                        .set_fill(BLACK, 1)
                    )
                black_keys.append(black_key)
            if counter >= self.number_of_keys:
                break
            counter += 1
        self.add(*black_keys)
        self.center()
        background = Rectangle(
            width=self.width, height=1.1, color=GREY, stroke_opacity=0
        ).set_fill(GREY, 1)
        self.submobjects.insert(0, background)


class MindAndHand(Scene):
    def construct(self):
        self.theta1 = PI / 2
        self.theta2 = PI / 2

        hand = SVGMobject("Hand.svg")
        mind = SVGMobject("Mind.svg")
        hand.set_color(YELLOW)
        mind.set_color(YELLOW)
        self.add(mind)
        self.play(DrawBorderThenFill(mind))
        self.wait()
        self.add(hand)
        hand.scale(3)
        hand.shift(LEFT * 0.30, UP * 0.5)
        self.play(FadeIn(hand))
        self.wait()
        self.remove(hand, mind)
        theta1 = ValueTracker(self.theta1)
        theta2 = ValueTracker(self.theta2)
        minute_hand = Line(ORIGIN, UP * 2, color=YELLOW)
        hour_hand = Line(ORIGIN, UP * 1.5, color=BLUE)
        self.add(minute_hand, hour_hand)
        self.play(
            AnimationGroup(
                FadeOut(hand),
                FadeIn(hour_hand),
                ReplacementTransform(mind, minute_hand),
            )
        )
        self.wait()
        keyboard = Keyboard(36, "d#").scale(2)
        minute_hand.add_updater(lambda m: m.set_angle(theta1.get_value()))
        hour_hand.add_updater(lambda m: m.set_angle(theta2.get_value()))
        self.play(
            theta1.animate.increment_value(-48 * PI * 7 / 8),
            theta2.animate.increment_value(-4 * PI * 7 / 8),
            minute_hand.animate.set_opacity(0),
            rate_func=rush_into,
            run_time=10,
        )
        hour_hand.clear_updaters()
        self.remove(minute_hand)
        self.add(keyboard.set_opacity(0))
        self.play(
            AnimationGroup(
                Transform(hour_hand, keyboard),
                DrawBorderThenFill(keyboard.set_opacity(1)),
            ),
            lag_ratio=0.5,
        )
        self.remove(hour_hand)
        self.wait()
        self.play(FadeOut(keyboard))
        self.remove(keyboard)
        you = quarter_creature.Quarter()
        self.add(you)
        self.play(FadeIn(you))
        self.wait()
        self.play(creature_animations.Blink(you))
        self.wait()
        self.play(you.animate.change("pondering"))


def inverse_power_law(maxint, scale, cutoff, exponent):
    return lambda r: maxint * (cutoff / (r / scale + cutoff)) ** exponent


def inverse_square(maxint, scale, cutoff):
    return inverse_power_law(maxint, scale, cutoff, 2)


class SoundIndicator(VMobject):
    CONFIG = {
        "radius": 0.5,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "precision": 3,
        "measurement_point": ORIGIN,
        "sound_source": None,
    }

    def generate_points(self):
        self.background = Circle(color=GREEN, radius=self.radius)
        self.background.set_fill(opacity=1.0)
        self.foreground = Circle(color=ORANGE, radius=self.radius)
        self.foreground.set_stroke(color=WHITE, width=0.5)
        self.add(self.background, self.foreground)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        return self

    def get_measurement_point(self):
        if self.measurement_point != None:
            return self.measurement_point
        else:
            return self.get_center()

    def measured_intensity(self):
        distance = np.linalg.norm(
            self.get_measurement_point() - self.sound_source.get_source_point()
        )
        intensity = (
            self.sound_source.opacity_function(distance)
            / self.opacity_for_unit_intensity
        )
        return intensity

    def update_mobjects(self):
        if self.sound_source == None:
            print("Indicator cannot update, reason: no sound source found")


#         self.set_intensity(self.measured_intensity())


class Restore(ApplyMethod):
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject.restore, **kwargs)


class EmitWaveAtPoint(Animation):
    def __init__(
        self, source, small_radius=0, big_radius=10, lag_ratio=0.1, color=BLUE, **kwargs
    ):
        self.name = "EmitWaveAtPoint"
        self.small_radius = small_radius
        self.big_radius = big_radius
        self.start_stroke_width = 8
        self.color = color
        self.run_time = 1
        self.lag_ratio = lag_ratio
        self.rate_func = linear
        self.suspend_mobject_updating = False
        self.remover = False
        self.source = source
        self.mobject = Circle(
            radius=self.big_radius,
            stroke_color=self.color,
            stroke_width=self.start_stroke_width,
        )
        self.mobject.move_to(source)

        def spawn_at_point(mobj, dt):
            mobj.move_to(self.source)
            self.mobject.clear_updaters()

        self.mobject.add_updater(spawn_at_point)

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.set_width(alpha * self.big_radius)
        self.mobject.set_stroke(width=(1 - alpha) * self.start_stroke_width)


class EmitWaves(LaggedStart):
    def __init__(self, focal_point, n_circles=5, lag_ratio=0.6, color=BLUE, **kwargs):
        self.small_radius = 0.0
        self.big_radius = 10
        self.n_circles = n_circles
        self.start_stroke_width = 8
        self.focal_point = focal_point
        self.color = color
        self.remover = True
        self.lag_ratio = lag_ratio
        self.remover = True
        animations = [
            EmitWaveAtPoint(focal_point, lag_ratio=lag_ratio, color=color, **kwargs)
            for x in range(self.n_circles)
        ]
        super().__init__(*animations, **kwargs)


class IntroduceSound(Scene):
    def construct(self):
        sound = Tex("Sound", color=YELLOW)
        sound.save_state()
        sound.scale(0).set(fill_opacity=0)
        self.add(sound)
        self.play(sound.animate.restore(), EmitWaves(sound))

        what_is = Tex("What is")
        sound.generate_target()
        question = Tex("?")
        wis = VGroup(what_is, sound.target)
        wis.arrange(RIGHT, buff=MED_SMALL_BUFF)
        wisq = VGroup(wis, question)
        wisq.arrange(RIGHT, buff=SMALL_BUFF)
        self.play(
            LaggedStart(
                MoveToTarget(sound),
                FadeIn(what_is),
                FadeIn(question),
                lag_ratio=0.30,
            )
        )


class Stereocilia(Scene):
    def construct(self):
        self.show_image()
        self.show_ear()
        self.show_corti()
        self.wait()

    def show_image(self):
        image = ImageMobject("stereocilia.jpg")
        tag = Text("Stereocilia")
        stereocilia = Group(image, tag).arrange(DOWN)
        self.play(FadeIn(image), Write(tag))
        self.play(FadeOut(image), Unwrite(tag, reverse=False))
        self.clear()

    def show_ear(self):
        ear = SVGMobject("human_ear.svg", height=config.frame_height).shift(RIGHT * 2.5)
        ear.save_state()
        self.play(ear.animate.restore())
        inner_ear = VGroup(ear[3:15], ear[52:54])
        middle_ear = VGroup(
            ear[15:17],
            ear[21:23],
            ear[25:27],  # malles
            ear[41:42],
            ear[42:45],  # incus/stapes
            ear[49:52],
        )
        outer_ear = VGroup(ear[18:21], ear[22:23], ear[27:28], ear[31:41], ear[48:50])
        extraneous_parts = VGroup(
            ear[0:3], ear[17:18], ear[23:25], ear[27:31], ear[45:48], ear[54:]
        )
        inner_ear.save_state()
        middle_ear.save_state()
        outer_ear.save_state()

        self.play(
            Uncreate(extraneous_parts),
        )

        # Outer ear
        outer_ear_label = BraceLabel(
            outer_ear, "Outer ear", 2 * LEFT, label_constructor=Tex
        )
        self.wait()
        self.play(Indicate(outer_ear), FadeIn(outer_ear_label))
        self.play(FadeOut(outer_ear_label))
        self.remove(outer_ear_label)
        pinna = Tex("Pinna", color="#e9c6af").to_corner(UL)
        pinna_arrow = Arrow(pinna.get_bottom(), UL * 2)
        tympanic_m = (
            Tex("Typmanic Membrane", color="#4e9a06").to_edge(DOWN).shift(RIGHT * 2)
        )
        tympanic_m_arrow = Arrow(tympanic_m.get_top(), ear[27].get_center() + DR * 0.25)
        self.play(
            Write(tympanic_m),
            Create(tympanic_m_arrow),
            Write(pinna),
            Create(pinna_arrow),
        )
        self.play(
            Unwrite(tympanic_m, reverse=False),
            Uncreate(tympanic_m_arrow),
            Unwrite(pinna, reverse=False),
            Uncreate(pinna_arrow),
        )
        self.remove(tympanic_m, tympanic_m_arrow, pinna_arrow, pinna)
        self.play(Uncreate(outer_ear))
        self.remove(outer_ear)
        self.wait()

        # Middle ear

        self.play(middle_ear.animate.shift(LEFT * 3))
        middle_ear_label = BraceLabel(
            middle_ear, "Middle ear", 2 * LEFT, label_constructor=Tex
        )
        self.play(Indicate(middle_ear), FadeIn(middle_ear_label))
        self.play(FadeOut(middle_ear_label))
        self.remove(middle_ear_label)

        eustachian_tube = Tex("Eustachian tube", color="#ff8080").to_edge(DOWN)
        eustachian_arrow = Arrow(
            eustachian_tube.get_top(),
            middle_ear[0].get_corner(DR) + UP * 0.1 + UL * 0.5,
        )
        self.play(Write(eustachian_tube), Create(eustachian_arrow))
        self.play(Unwrite(eustachian_tube, reverse=False), Uncreate(eustachian_arrow))

        malleus = Tex("Malleus", color="#e6e6e6").to_corner(UL)
        malleus_arrow = Arrow(
            malleus.get_bottom(), middle_ear[2][0].get_bottom(), buff=0.02
        )

        incus = Tex("Incus", color="#e6e6e6").to_edge(UP)
        incus_arrow = Arrow(
            incus.get_bottom(), middle_ear[4][2].get_top() + LEFT * 0.2, buff=0.02
        )

        stapes = Tex("Stapes", color="#e6e6e6").to_corner(UR)
        stapes_arrow = Arrow(stapes.get_bottom(), middle_ear[4][0].get_top(), buff=0.02)
        self.play(
            Write(stapes),
            Create(stapes_arrow),
            Write(incus),
            Create(incus_arrow),
            Write(malleus),
            Create(malleus_arrow),
        )
        self.play(
            Wiggle(malleus),
        )
        self.play(
            Wiggle(incus),
        )
        self.play(
            Wiggle(stapes),
        )
        self.play(
            Unwrite(malleus, reverse=False),
            Uncreate(malleus_arrow),
            Unwrite(incus, reverse=False),
            Uncreate(incus_arrow),
            Unwrite(stapes, reverse=False),
            Uncreate(stapes_arrow),
        )

        self.play(Uncreate(middle_ear))
        self.remove(middle_ear)

        # Inner ear

        self.play(inner_ear.animate.shift(LEFT * 5))

        inner_ear_label = BraceLabel(inner_ear, "Inner ear", label_constructor=Tex)
        self.play(
            Create(inner_ear_label),
        )
        self.play(Unwrite(inner_ear_label, reverse=False))

        cochlea = Tex("Cochlea", color="#ad7fa8").to_corner(DL)
        cochlea_arrow = Arrow(cochlea.get_top(), inner_ear[0][10])
        cochlear_nerve = Tex("Cochlear nerve", color=YELLOW).to_corner(UR)
        cochlear_arrow = Arrow(cochlear_nerve.get_bottom(), inner_ear.get_right())
        self.play(
            Write(cochlea),
            Create(cochlea_arrow),
            Write(cochlear_nerve),
            Create(cochlear_arrow),
        )
        self.play(
            Unwrite(cochlea, reverse=False),
            Uncreate(cochlea_arrow),
            Unwrite(cochlear_nerve, reverse=False),
            Uncreate(cochlear_arrow),
        )

        oval_window = Tex("Oval window", color="#743dda").to_edge(LEFT).shift(UP)
        oval_window_arrow = Arrow(oval_window.get_right(), inner_ear[0][9], buff=0.02)

        round_window = Tex("Round window", color="#ad7fa8").to_edge(LEFT).shift(DOWN)
        round_window_arrow = Arrow(
            round_window.get_right(), inner_ear[0][10], buff=0.02
        )

        helicotrema = Tex("Helicotrema", color="#ad7fa8").to_corner(DR)
        helicotrema_arrow = Arrow(
            helicotrema.get_left(), inner_ear[0][8].get_center() + LEFT * 0.05
        )

        self.play(
            Write(oval_window),
            Write(round_window),
            Write(helicotrema),
            Create(oval_window_arrow),
            Create(round_window_arrow),
            Create(helicotrema_arrow),
        )

        self.play(
            Unwrite(oval_window, reverse=False),
            Unwrite(round_window, reverse=False),
            Unwrite(helicotrema, reverse=False),
            Uncreate(oval_window_arrow),
            Uncreate(round_window_arrow),
            Uncreate(helicotrema_arrow),
        )

        self.play(Uncreate(inner_ear))
        self.remove(inner_ear)
        self.clear()

    def show_corti(self):
        corti = SVGMobject("Organ_of_corti.svg")
        corti.set(width=config.frame_width)
        # inner_outter_hair_cells = corti[1:24] + corti[39:42]
        # corti[0:3] - fleshy part top right
        outer_hair_cell = VGroup(corti[17:25])
        inner_hair_cells = VGroup(corti[6:8], corti[34:40])
        basilar_membrane = corti[4:6]
        inner_hair_label = Text("Inner hair cell", color="#803300").to_corner(UR)
        outer_hair_label = Text("Outer hair cell", color="#ff6600").to_corner(UL)
        inner_arrow = Arrow(
            inner_hair_label, inner_hair_cells.get_corner(UL) + DR * 0.3
        )
        outer_arrow = Arrow(outer_hair_label, outer_hair_cell.get_corner(UR) + DL * 0.4)

        stereocilia = corti[72:73]
        self.play(
            Create(stereocilia),
            Create(inner_hair_cells),
            Create(outer_hair_cell),
            Write(inner_hair_label),
            Write(outer_hair_label),
            Create(inner_arrow),
            Create(outer_arrow),
            lag_ratio=0.7,
            runtime=4,
        )
        g = []
        for i in range(150):
            shift_val = ORIGIN
            while np.linalg.norm(shift_val) < 2.2:
                shift_val = random.uniform(-7, 7) * RIGHT + random.uniform(0, 2.8) * UP
            g.append(
                Dot(color=YELLOW, radius=DEFAULT_DOT_RADIUS * 0.5).shift(shift_val)
            )

        cations = VGroup(*g)
        self.mobjects.insert(0, cations)
        self.play(FadeIn(cations))
        self.wait()

        tectorial_membrane = corti[0:3]
        tectorial_membrane.set(opacity=0)
        tectorial_label = Text("Tectorial membrane", color="#d45500").to_edge(UP)
        tectorial_arrow = Arrow(
            tectorial_label.get_bottom(), tectorial_label.get_bottom() + DOWN, buff=0.02
        )
        basilar_label = Text("Basilar membrane", color="#ff9955").to_edge(DOWN)
        basilar_arrow = Arrow(basilar_label.get_top(), corti[31])
        other_inner_cells = VGroup(corti[3:6], corti[8:17], corti[40:70])
        self.mobjects.insert(1, other_inner_cells)
        self.mobjects.insert(1, tectorial_membrane)
        self.mobjects.insert(1, tectorial_membrane)
        self.play(
            AnimationGroup(
                Unwrite(inner_hair_label, reverse=False),
                Unwrite(outer_hair_label, reverse=False),
                FadeOut(inner_arrow),
                FadeOut(outer_arrow),
            ),
            Create(other_inner_cells),
            lag_ratio=0.5,
            run_time=2,
        )

        # Cochlear nerve
        cochlear_nerve = Text("Cochlear nerve", color=YELLOW).to_edge(DOWN)
        cochlear_arrow = Arrow(cochlear_nerve, DR * 3 + RIGHT)
        self.play(
            Write(cochlear_nerve, run_time=2),
            FadeIn(cochlear_arrow, run_time=2),
        )
        self.play(
            Unwrite(cochlear_nerve, run_time=2),
            FadeOut(cochlear_arrow, run_time=2),
        )

        # Membranes
        self.play(
            tectorial_membrane.animate.set_opactiy(1),
            Write(tectorial_label),
            FadeIn(tectorial_arrow),
            Write(basilar_label, reverse=False),
            FadeIn(basilar_arrow),
        )
        self.play(
            Unwrite(tectorial_label),
            FadeOut(tectorial_arrow),
            Unwrite(basilar_label, reverse=False),
            FadeOut(basilar_arrow),
        )
        self.play(Wiggle(stereocilia))

        scala_tympani = Rectangle(
            color=BLUE_B, fill_opacity=0, width=15, height=4
        ).shift(3 * DOWN)
        scala_media = Rectangle(color=BLUE_D, fill_opacity=0, width=15, height=6).shift(
            1.5 * UP
        )
        self.mobjects.insert(0, scala_media)
        self.mobjects.insert(0, scala_tympani)
        self.play(
            self.mobjects[0].animate.set_opacity(1),
            self.mobjects[1].animate.set_opacity(1),
        )

        scala_t_label = Tex("Scala tympani", color=BLUE_D).to_edge(DOWN)
        scala_m_label = Tex("Scala media", color=BLUE_B).to_edge(UP)
        self.play(
            Write(scala_t_label),
            Write(scala_m_label),
        )

        self.play(
            Unwrite(scala_t_label, revere=False),
            Unwrite(scala_m_label, revere=False),
        )

        path = VMobject().set_points_as_corners(
            [
                [-0.6, 1.8, 0],
                [-1.2, 0.2, 0],
                [2.3, -1, 0],
                [2.8, -1.8, 0],
                [4, -3, 0],
                [14, -5, 0],
            ]
        )
        path2 = VMobject().set_points_as_corners(
            [[1.2, 1.3, 0], [2.3, -1, 0], [2.8, -1.8, 0], [4, -3, 0], [14, -5, 0]]
        )
        dots = [MoveAlongPath(Dot(color=YELLOW, radius=0.05), path) for _ in range(30)]
        dots2 = [
            MoveAlongPath(Dot(color=YELLOW, radius=0.05), path2) for _ in range(30)
        ]
        self.play(
            AnimationGroup(*dots, lag_ratio=0.125, run_time=8),
            AnimationGroup(*dots2, lag_ratio=0.125, run_time=8),
        )
        self.clear()
        self.wait()

class StandingWaveExample(Scene):
    def construct(self):
        wave1 = StandingWave(1, color=RED)
        wave2 = StandingWave(2, color=ORANGE)
        wave3 = StandingWave(3, color=YELLOW)
        wave4 = StandingWave(4, color=GREEN)
        wave5 = StandingWave(5, color=BLUE)
        wave6 = StandingWave(6, color=PURPLE)
        waves_odd = VGroup(wave1, wave3, wave5).arrange().to_edge(UP)
        waves_even = VGroup(wave2, wave4, wave6).arrange().to_edge(DOWN)
        for wave in waves_odd:
            wave.start_wave()
        for wave in waves_even:
            wave.start_wave()
        self.play(
            Create(waves_odd),
            Create(waves_even),
            lag_ratio=.6
        )
        self.wait(1)

class ShowSpeaker(Scene):
    def construct(self):
        speaker = SVGMobject("audio.svg").scale(3).to_edge(LEFT)
        speaker.remove(speaker[1])
        speaker.save_state()
        speaker.shift(LEFT * 9)
        self.add(speaker)
        self.play(speaker.animate.restore())
        loudspeaker = SVGMobject("loudspeaker.svg").scale(1.5).rotate(-PI / 2)
        loudspeaker.to_edge(LEFT).shift(RIGHT * 1.1)
        self.play(FadeIn(loudspeaker))
        voice_coil = Tex("Voice coil", color=YELLOW).to_corner(DL)
        vc_arrow = Arrow(
            voice_coil.get_top(),
            loudspeaker[0].get_center() + DL * 0.9 + RIGHT * 0.1,
            color=YELLOW,
            buff=0.02,
        )
        diaphragm = Tex("Diaphragm", color="#ff00ff").next_to(voice_coil)
        d_arrow = Arrow(diaphragm.get_top(), loudspeaker[7], color="#ff00ff")
        magnet = Tex("Magnet", color="#ff0000").to_corner(UL)
        m_arrow = Arrow(magnet, loudspeaker[9].get_center(), color="#ff0000")
        self.play(
            Write(voice_coil),
            Write(diaphragm),
            Write(magnet),
            Create(vc_arrow),
            Create(d_arrow),
            Create(m_arrow),
        )
        self.play(
            Unwrite(voice_coil),
            Unwrite(diaphragm),
            Unwrite(magnet),
            Uncreate(vc_arrow, reverse=False),
            Uncreate(d_arrow, reverse=False),
            Uncreate(m_arrow, reverse=False),
        )
        self.wait()


class Speaker(Scene):
    def construct(self):
        self.setup_axes()
        self.move_speaker()

    def setup_axes(self):

        self.axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
            x_length=8,
            y_length=8,
            z_length=8,
            depth_test=True,
        )
        self.axes.x_axis.set_color(RED)
        self.axes.y_axis.set_color(GREEN)
        self.axes.z_axis.set_color(BLUE)
        self.add(self.axes)
        self.renderer.camera = OpenGLCamera(center_point=4*OUT)
        self.renderer.camera.rotate_about_origin(-PI / 2, UP)
        # self.renderer.camera.rotate_about_origin(PI / 2, OUT)

    def move_speaker(self):
        self.t = ValueTracker(0)
        self.amp = ValueTracker(1)
        self.kappa = ValueTracker(1)
        self.omega = ValueTracker(TAU)
        self.opacity = ValueTracker(0)
        num_dots = 600
        self.pf_phase = always_redraw(
            lambda: ParametricFunction(
                lambda x: self.axes.c2p(
                    0,
                    (
                        self.amp.get_value()
                        * np.sin(
                            self.kappa.get_value() * x
                            - self.omega.get_value() * self.t.get_value()
                        )
                    ),
                    x,
                ),
                t_range=[0, 3*TAU],
                color=RED,
                stroke_opacity=self.opacity.get_value(),
                depth_test=True,
            )
        )
        self.pf = always_redraw(
            lambda: ParametricFunction(
                lambda x: self.axes.c2p(
                    0,
                    (
                        self.amp.get_value()
                        * np.cos(
                            self.kappa.get_value() * x
                            - self.omega.get_value() * self.t.get_value()
                        )
                    ),
                    x,
                ),
                t_range=[0, 3*TAU],
                stroke_opacity=0,
            )
        )
        self.add(self.pf, self.pf_phase)
        seed = random.seed(0)
        dots = []
        for _ in range(num_dots):
            angle = TAU*random.uniform(-1,1)
            z_pos = random.uniform(2,10)
            scale = .95
            if z_pos > 3 and z_pos < 4.25:
                scale = .90 + 2 * (z_pos-3)
                z_pos += .35
            elif z_pos > 4.25:
                scale = 3.25
            dots.append(
                OpenGLSphere(
                    resolution=(51, 51),
                    radius=.04
                ).move_to(
                    self.axes.c2p(
                        random.uniform(0,scale)*np.sin(TAU*angle),
                        random.uniform(0,scale)*np.cos(TAU*angle),
                        z_pos
                    )
                )
            )

        dots = OpenGLGroup(*dots)
        copy_dots = dots.copy()

        def get_dot_y(mob):
            for i in range(len(mob)):
                y = self.pf.get_point_from_function(copy_dots[i].get_z())
                mob[i].move_to(copy_dots[i].get_center() + IN * y[1])

        dots.add_updater(lambda mob: get_dot_y(mob))

        class SquareTorus(OpenGLSurface):
            def __init__(self, u_range=None, v_range=None, r1=1.5, r2=0.5, **kwargs):
                u_range = u_range if u_range is not None else (0, TAU)
                v_range = v_range if v_range is not None else (0, TAU)
                self.r1 = r1
                self.r2 = r2
                self.color = RED
                super().__init__(u_range=u_range, v_range=v_range, **kwargs)

            def uv_func(self, u, v):
                P = np.array([np.cos(u), np.sin(u), 0])
                stuff = -1
                if np.sin(v) > 0:
                    stuff = 1
                return (self.r1 + self.r2 * np.cos(v)) * P + self.r2 * stuff * OUT

        magnet = SquareTorus(
            depth_test=True,
            color=RED,
        ).shift(1*IN)

        coil = ParametricFunction(
            lambda u: self.axes.c2p(1.1 * np.cos(2 * u), 1.1 * np.sin(2 * u), u * 0.0125),
            color=YELLOW,
            t_range=[0, 12*TAU-PI/4, 0.01],
            depth_test=True,
        )
        cylinder = OpenGLSurface(
            lambda u, v: self.axes.c2p(np.cos(u), np.sin(u), v),
            u_range=[0, 2 * PI],
            v_range=[0, 1],
            color=YELLOW_B,
            depth_test=True,
        )

        diaphragm = OpenGLSurface(
            lambda u, v: self.axes.c2p(v * np.sin(u), v * np.cos(u), v),
            u_range=[0, TAU],
            v_range=[1, 3],
            checkerboard_colors=["#ff00ff", "#ee00ee"],
            depth_test=True,
            color=PINK,
        )
        moving_parts = OpenGLGroup(
            cylinder,
            diaphragm,
            coil,
            depth_test=True,
        )
        copy_parts = moving_parts.copy()

        def get_y(mob: VMobject):
            for i in range(len(mob)):
                mob[i].move_to(
                    copy_parts[i].get_center()
                    + self.axes.c2p(0,0, self.amp.get_value() * np.sin(-self.omega.get_value() * self.t.get_value()))
                )

        moving_parts.add_updater(lambda mob: get_y(mob))
        self.play(Create(dots), Create(moving_parts), Create(magnet))

        self.play(
            self.t.animate.set_value(4),
            self.opacity.animate.set_value(1),
            run_time=4,
            rate_func=linear,
        )
        self.play(
            self.t.animate.set_value(8),
            run_time=4,
            rate_func=linear,
        )
        self.interactive_embed()


class Transducer(Scene):
    def construct(self):
        self.show_definition()

    def show_definition(self):
        word = Text(
            "transducer noun",
            t2c={"noun": ORANGE},
            size=2,
            disable_ligatures=True,
        )
        pronunciation = Text(
            "trans·​duc·​er | \\ tran(t)s-ˈdü-sər  , tranz-, -ˈdyü- \\",
            size=0.8,
        )
        definition = Text(
            "a device that receives a signal in the form of one type\nof energy and converts it to a signal in another form",
            disable_ligatures=True,
            t2c={
                "converts": RED_D,
                "device": GREEN_B,
                "energy": YELLOW_D,
                "signal": YELLOW,
            },
            t2g={
                "one type": [BLUE, RED],
                "another form": [RED, BLUE],
            },
            size=0.8,
        )
        diction = VGroup(word, pronunciation, definition).arrange(DOWN)
        word.to_edge(LEFT)
        pronunciation.to_edge(LEFT)
        definition.to_edge(LEFT)
        self.play(Write(diction), run_time=10)
        self.wait()


class DigitalMind(CreatureScene):
    def construct(self):
        student = Quarter(color=BLUE).to_corner(DR)
        student.make_eye_contact(self.creature)
        self.add_creature(student)
        self.wait()
        spacer = 2.25 * DOWN
        your_mind = SVGMobject("mind.svg")
        your_mind.set_color(BLUE).move_to(UR * 2 + UP * 0.25)
        my_mind = your_mind.copy()
        my_mind.set_color(GRAY_BROWN).move_to(UL * 2 + UP * 0.25)

        da = Line(my_mind, your_mind, buff=0.1, stroke_width=20).set_color_by_gradient(
            [BLUE, BLUE, GRAY_BROWN, GRAY_BROWN]
        )
        tip = ArrowTriangleFilledTip(color=GRAY_BROWN)
        end_tip = ArrowTriangleFilledTip(color=BLUE)
        da.add_tip(tip, at_start=True)
        da.add_tip(end_tip, at_start=False)

        my_waves = EmitWaves(
            my_mind.get_center() + spacer,
            big_radius=2,
            small_radius=1,
            lag_ratio=1,
            color=GRAY_BROWN,
        )
        your_waves = EmitWaves(
            your_mind.get_center() + spacer, big_radius=2, small_radius=1, lag_ratio=1
        )

        my_ea_transducer = Rectangle(width=2, color=GRAY_BROWN).next_to(
            my_waves.focal_point, spacer, buff=0.5
        )
        your_ea_transducer = Rectangle(width=2, color=BLUE).next_to(
            your_waves.focal_point, spacer, buff=0.5
        )

        self.play(
            student.animate.look_at(your_mind),
            self.creature.animate.look_at(my_mind),
            Write(my_mind),
            Write(your_mind),
            Write(da),
        )

        self.play(
            my_waves,
            your_waves,
            da.animate.move_to(my_waves.focal_point, coor_mask=[0, 1, 0]),
            student.animate.look_at(your_waves.focal_point),
            self.creature.animate.look_at(my_waves.focal_point),
            run_time=3,
        )

        self.play(
            my_waves,
            your_waves,
            da.animate.move_to(my_waves.focal_point, coor_mask=[0, 1, 0]),
            student.animate.look_at(your_waves.focal_point),
            self.creature.animate.look_at(my_waves.focal_point),
            run_time=3,
        )

        self.play(
            student.animate.look_at(your_ea_transducer),
            self.creature.animate.look_at(my_ea_transducer),
            Write(
                SVGMobject("microphone.svg")
                .set_color(GRAY_BROWN)
                .set(height=my_ea_transducer.height)
                .move_to(my_ea_transducer)
            ),
            Write(
                SVGMobject("Audio.svg")
                .set_color(BLUE)
                .set(width=your_ea_transducer.height)
                .move_to(your_ea_transducer)
            ),
            my_waves,
            your_waves,
            da.animate.move_to(my_ea_transducer, coor_mask=[0, 1, 0]),
            run_time=3,
        )
        self.play(
            my_waves,
            your_waves,
            student.animate.look_at(your_waves.focal_point),
            self.creature.animate.look_at(my_waves.focal_point),
            run_time=3,
        )

        self.play(my_waves, your_waves, run_time=3)


class Projection(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        self.show_axis()
        self.show_circle()
        self.demonstrate_radians()
        self.demonstrate_projection()
        self.demonstrate_period_and_frequency()
        self.wait()

    def show_axis(self):
        self.number_plane = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            x_length=4 * 7,
            y_length=16,
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 3,
                "stroke_opacity": 0.6,
            },
        )
        self.axes = Axes(
            x_range=[-7, 7],
            y_range=[-4, 4],
            x_length=4 * 7,
            y_length=16,
        )
        # self.axes.add_coordinates(
        #     dict(
        #         zip(
        #             [x for x in np.arange(-4 * PI, 5 * PI, PI)],
        #             [
        #                 MathTex(f"{x}\\pi")
        #                 if abs(x) > 1
        #                 else MathTex("\\pi")
        #                 if x == 1
        #                 else MathTex("-\\pi")
        #                 if x == -1
        #                 else ""
        #                 for x in range(-4, 5)
        #             ],
        #         )
        #     )
        # )
        self.play(Write(self.number_plane))
        self.theta = ValueTracker(0)
        self.theta_val = DecimalNumber(
            self.theta.get_value(), num_decimal_places=2, color=GREEN
        )

        self.line = always_redraw(
            lambda: Line(
                self.axes.c2p(0, 0),
                self.axes.c2p(
                    np.cos(self.theta.get_value()), np.sin(self.theta.get_value())
                ),
                color=YELLOW,
            )
        )
        self.ang = always_redraw(
            lambda: Angle(
                Line(self.axes.c2p(0, 0), self.axes.c2p(1, 0)), self.line, color=GREEN
            )
        )
        self.play(Write(self.line), Write(self.ang))

    def show_circle(self):
        self.circle = ParametricFunction(
            lambda x: self.axes.c2p(np.cos(x), np.sin(x), 0), t_range=[0, 2 * PI]
        )

        self.add(self.circle)

    def demonstrate_radians(self):
        theta_label = MathTex(r"\theta = ", color=GREEN).to_corner(UL)

        arc_vs_radius = MathTex(
            r"\frac{\textrm{Arc length}}{\textrm{Radius}}",
            "=",
        ).next_to(theta_label, RIGHT)
        for i in range(len(arc_vs_radius.submobjects[0])):
            if i in range(9):
                arc_vs_radius.submobjects[0][i].set_color(GREEN)
            elif i in range(10, 16):
                arc_vs_radius.submobjects[0][i].set_color(YELLOW)

        self.theta_val.add_updater(
            lambda mob: mob.next_to(arc_vs_radius).set_value(self.theta.get_value())
        )
        self.add(theta_label, arc_vs_radius, self.theta_val)

        flat = Line(self.axes.c2p(0, 0), self.axes.c2p(1, 0))

        def create_mathtex():
            point = Angle(
                flat,
                self.line,
                radius=0.5 + 2 * SMALL_BUFF,
            ).point_from_proportion(0.5)
            if point is None:
                point = RIGHT
            mathtex = MathTex(r"\theta", color=GREEN).move_to(point)
            mathtex.scale(min(1, self.theta.get_value()))
            return mathtex

        self.theta_close = always_redraw(create_mathtex)
        self.add(self.theta_close)
        self.circle_dot = always_redraw(
            lambda: Dot(color=ORANGE).move_to(self.line.get_end())
        )

        self.rad = always_redraw(
            lambda: ParametricFunction(
                lambda t: self.axes.c2p(np.cos(t), np.sin(t), 0),
                color=GREEN,
                t_range=[0, self.theta.get_value()],
            )
        )
        self.add(self.rad)
        self.add(self.circle_dot)
        self.play(self.theta.animate.set_value(1), rate_func=linear)
        rad = self.rad.copy()
        line = self.line.copy()
        self.play(rad.animate.shift(2 * RIGHT), line.animate.shift(2 * RIGHT))
        self.add(rad)
        vert_line = Line(self.axes.c2p(2, 0, 0), self.axes.c2p(2, 1, 0), color=YELLOW)
        self.play(ReplacementTransform(line, vert_line))
        self.play(ReplacementTransform(rad, vert_line))
        self.play(Uncreate(vert_line))

        self.play(self.theta.animate.set_value(PI + 0.00001), rate_func=linear)
        self.wait()

        self.play(self.theta.animate.set_value(TAU), rate_func=linear)
        self.wait()

        self.play(
            self.theta.animate.set_value(0),
            rate_func=linear,
        )
        self.play(
            Unwrite(arc_vs_radius),
            Unwrite(self.theta_close),
        )
        self.remove(arc_vs_radius, self.theta_close)

        self.theta_val.clear_updaters()
        self.play(theta_label.animate.next_to(self.theta_val, LEFT), rate_func=linear)

        self.theta_group = VGroup(theta_label, self.theta_val)

        self.play(
            self.theta_group.animate.to_corner(UR),
            rate_func=linear,
        )
        self.theta_val.add_updater(
            lambda mob: mob.next_to(theta_label).set_value(self.theta.get_value())
        )

    def demonstrate_projection(self):
        sin_phi = ValueTracker(0)
        self.cos_curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: self.axes.c2p(t, np.cos(t), 0),
                t_range=[0, self.theta.get_value()],
                color=BLUE,
            )
        )

        self.sin_curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: self.axes.c2p(t, np.sin(t + sin_phi.get_value()), 0),
                t_range=[0, self.theta.get_value()],
                color=RED,
            )
        )

        x_y_label = always_redraw(
            lambda: MathTex(
                "x",
                ",",
                "y",
                "=",
                "(",
                f"{np.round(np.cos(self.theta.get_value()), decimals=2)}",
                "r",
                ",",
                f"{np.round(np.sin(self.theta.get_value()), decimals=2)}",
                "r",
                ")",
                tex_to_color_map={
                    "r": YELLOW,
                    "x": BLUE,
                    f"{np.round(np.cos(self.theta.get_value()), decimals=2)}": BLUE,
                    "y": RED,
                    f"{np.round(np.sin(self.theta.get_value()), decimals=2)}": RED,
                },
            ).to_corner(UL)
        )
        vert_line = always_redraw(
            lambda: DashedLine(
                self.axes.c2p(self.theta.get_value(), -1),
                self.axes.c2p(self.theta.get_value(), 1),
                color=GRAY,
                fill_opacity=0.2,
            )
        )
        horiz_line = always_redraw(
            lambda: Line(
                self.axes.c2p(0, 0),
                self.axes.c2p(self.theta.get_value(), 0),
                color=GREEN,
                fill_opacity=0.2,
            )
        )
        x_axis_theta_label = MathTex("\\theta", color=GREEN).add_updater(
            lambda m: m.next_to(vert_line, DR)
        )
        cos_label = MathTex(r"\cos(\theta)", color=BLUE).next_to(x_y_label, DOWN)
        sin_label = MathTex(r"\sin(\theta)", color=RED).next_to(cos_label)
        self.add(
            self.sin_curve,
            self.cos_curve,
            vert_line,
            x_axis_theta_label,
            horiz_line,
        )
        self.play(
            Write(x_y_label),
            Write(cos_label),
            Write(sin_label),
        )
        self.play(
            self.theta.animate.set_value(PI / 2),
            rate_func=linear,
        )
        self.play(Wiggle(horiz_line), Wiggle(self.rad), Wiggle(self.theta_group))

        self.play(Wiggle(self.cos_curve), Wiggle(cos_label))

        self.play(Wiggle(self.sin_curve), Wiggle(sin_label))
        self.play(
            self.theta.animate.set_value(PI),
            rate_func=linear,
        )

        radius = self.axes.c2p(1, 0, 0)[0]
        positive_sin_brace = ArcBrace(Arc(radius, 0, PI), color=RED)
        positive_sign = Tex("+", color=RED).scale(2)
        background_rect = BackgroundRectangle(positive_sign)
        positive_sin_label = VGroup(background_rect, positive_sign).next_to(
            positive_sin_brace, UP
        )
        self.play(Write(positive_sin_brace), FadeIn(positive_sin_label))
        self.play(FadeOut(positive_sin_label), Unwrite(positive_sin_brace))
        self.remove(positive_sin_brace, positive_sin_label)

        self.play(
            self.theta.animate.set_value(3 * PI / 2),
            self.camera.frame.animate.shift(RIGHT * PI),
            cos_label.animate.shift(RIGHT * PI),
            sin_label.animate.shift(RIGHT * PI),
            rate_func=linear,
        )

        negative_cos_brace = ArcBrace(Arc(radius, PI / 2, PI), color=BLUE)
        negative_sign = Tex("-", color=BLUE).scale(2)
        background_rect = BackgroundRectangle(negative_sign)
        negative_cos_label = VGroup(background_rect, negative_sign).next_to(
            negative_cos_brace, LEFT
        )
        self.play(Write(negative_cos_brace), FadeIn(negative_cos_label))
        self.play(FadeOut(negative_cos_label), Unwrite(negative_cos_brace))
        self.remove(negative_cos_brace, negative_cos_label)

        sin_cos_labels = VGroup(cos_label, sin_label)
        self.play(
            self.theta.animate.set_value(TAU),
            self.camera.frame.animate.shift(RIGHT * PI),
            sin_cos_labels.animate.next_to(self.theta_val, DOWN),
            rate_func=linear,
        )

        new_sin_label = MathTex(r"\sin(\theta + \phi)", color=RED).next_to(cos_label)
        self.play(
            ReplacementTransform(
                sin_label.submobjects[0][0:5], new_sin_label.submobjects[0][0:5]
            ),
            FadeIn(new_sin_label.submobjects[0][5:7]),
            ReplacementTransform(
                sin_label.submobjects[0][5:], new_sin_label.submobjects[0][7:]
            ),
        )
        self.remove(sin_label)
        new_new_sin_label = always_redraw(
            lambda: MathTex(
                rf"\sin(\theta + {np.round(sin_phi.get_value(), decimals=2)})",
                color=RED,
            ).next_to(cos_label)
        )

        self.play(
            ReplacementTransform(
                new_sin_label.submobjects[0][0:6], new_new_sin_label.submobjects[0][0:6]
            ),
            FadeOut(new_sin_label.submobjects[0][6]),
            FadeIn(new_new_sin_label.submobjects[0][6:10]),
            ReplacementTransform(
                new_sin_label.submobjects[0][7], new_new_sin_label.submobjects[0][9:]
            ),
        )
        self.remove(new_sin_label)
        self.remove(new_new_sin_label)
        self.add(new_new_sin_label)
        self.play(sin_phi.animate.set_value(PI / 2))
        self.play(
            Unwrite(cos_label),
            Uncreate(self.cos_curve),
            Unwrite(new_new_sin_label),
            Uncreate(self.sin_curve),
            Uncreate(vert_line),
            Uncreate(horiz_line),
            Unwrite(x_axis_theta_label),
            lag_ratio=0.4,
        )
        self.remove(
            cos_label,
            new_new_sin_label,
            self.cos_curve,
            self.sin_curve,
            x_axis_theta_label,
        )
        self.play(
            self.camera.frame.animate.restore(),
            self.theta.animate.set_value(0),
            rate_func=linear,
        )
        self.play(Unwrite(x_y_label))
        self.remove(x_y_label)
        self.remove(horiz_line)
        self.wait()

    def demonstrate_period_and_frequency(self):
        background_rect = Rectangle(
            height=8, width=5, color=BLACK, fill_opacity=1, stroke_width=0
        ).shift(LEFT * 5.5)
        self.play(FadeIn(background_rect))
        ang_v = MathTex(
            r"{{\omega}} \equiv \frac{\theta}{t} {{\textrm{ rad/s} }}",
            tex_to_color_map={r"\omega": ORANGE},
        ).to_corner(UL)
        ang_v.submobjects[1][1].set_color(GREEN)

        theta_ang_v = (
            MathTex(
                r"\theta = ",
                "\omega",
                r" t {{\textrm{ rad} }}",
                tex_to_color_map={r"\omega": ORANGE, r"\theta": GREEN},
            )
            .next_to(ang_v, DOWN)
            .align_to(ang_v, LEFT)
        )

        self.play(Write(ang_v), self.theta.animate.set_value(TAU), rate_func=linear)
        self.play(Write(theta_ang_v))

        period_t = (
            MathTex("t = ", r"\frac{\theta}{\omega} {{\textrm{ s} }}")
            .next_to(theta_ang_v, DOWN)
            .align_to(ang_v, LEFT)
        )
        period = (
            MathTex("T = ", r"\frac{\tau}{\omega} {{\textrm{ s} }}")
            .next_to(theta_ang_v, DOWN)
            .align_to(ang_v, LEFT)
        )
        period_t.submobjects[1][0].set_color(GREEN)
        period.submobjects[1][0].set_color(GREEN)
        period_t.submobjects[1][2].set_color(ORANGE)
        period.submobjects[1][2].set_color(ORANGE)

        self.play(Write(period_t))
        self.wait()
        self.play(ReplacementTransform(period_t, period))

        freq = (
            MathTex(
                r"f = \frac{1}{T} =",
                r"\frac{\omega}{\tau}",
                r"\textrm{ 1/s}",
            )
            .next_to(period, DOWN)
            .align_to(ang_v, LEFT)
        )
        freq.submobjects[1][0].set_color(ORANGE)
        freq.submobjects[1][2].set_color(GREEN)
        self.play(Write(freq))

        ang_v2 = MathTex(r"\omega = \tau f")

        freq2 = MathTex(r"f = \frac{\omega}{2 \pi}")

        self.play(self.theta.animate.set_value(2 * TAU), rate_func=linear)
        # twice_as_slow = always_redraw(
        #     lambda: Line(
        #         self.axes.c2p(0, 0),
        #         self.axes.c2p(
        #             np.cos(.5*self.theta.get_value()), np.sin(.5*self.theta.get_value())
        #         ),
        #         color=ORANGE,
        #     )
        # )
        self.wait()


class SimpleWaves(ThreeDScene):
    def construct(self):
        self.setup_equation()

    def setup(self):
        self.axes = ThreeDAxes(
            x_range=[-4 * PI, 4 * PI, PI],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=14.2,
            y_length=6,
            z_length=6,
        )
        self.axes.add_coordinates(
            dict(
                zip(
                    [x for x in np.arange(-4 * PI, 5 * PI, PI)],
                    [
                        MathTex(f"{x}\\pi")
                        if abs(x) > 1
                        else MathTex("\\pi")
                        if x == 1
                        else MathTex("-\\pi")
                        if x == -1
                        else ""
                        for x in range(-4, 5)
                    ],
                )
            )
        )
        self.add(self.axes)
        super().setup()

    def setup_equation(self):
        color_map = {
            "x": RED,
            "t": BLUE,
            "A": GREEN,
            "\\omega": YELLOW,
            "\\phi": LIGHT_GRAY,
            "\\kappa": ORANGE,
        }
        self.simple_wave_eqn = MathTex(
            "u(",
            "x" "," "t",
            ")=",
            "A",
            "\\sin",
            "(",
            "\\kappa",
            "x" "-",
            "\\omega",
            "t",
            "+",
            "\\phi",
            ")",
            tex_to_color_map=color_map,
        )
        self.simple_wave_eqn.to_edge(UP)
        self.play(Write(self.simple_wave_eqn))

    def demonstrate_frequency(self):

        amp = ValueTracker(1)
        omega = ValueTracker(1)
        phi = ValueTracker(0)
        time = ValueTracker(0)
        freq = ValueTracker(2 * PI)
        sin = always_redraw(
            lambda: ParametricFunction(
                lambda t: self.axes.c2p(
                    t,
                    amp.get_value()
                    * np.sin(omega.get_value() * time.get_value() + phi.get_value()),
                    0,
                ),
                t_range=[-4 * PI, 4 * PI],
            )
        )
        self.add(sin)

        # self.play(omega.animate.set_value(0.125))


class WaveProp(Scene):
    def construct(self):

        time = ValueTracker(-2)

        def initial_u(p):
            arr = np.array(
                [
                    p,
                    np.exp(-0.5 * np.power(((p - float(time.get_value())) / 0.08), 2)),
                    0,
                ]
            )
            return arr

        wave = always_redraw(lambda: ParametricFunction(initial_u, t_range=[-7.3, 7.3]))

        def sin_wave_func(x, dt):
            return np.array([x, np.sin(x * float(time.get_value())), 0])

        def move_dot(dot, dt):

            dot.shift(RIGHT * sin_wave_func(dot.get_x(), dt)[1])
            return dot

        dots = VGroup(
            *[
                Dot().shift(RIGHT * random.uniform(-7, 7) + UP * random.uniform(-4, 4))
                for _ in range(100)
            ]
        )
        copy_dots = dots.copy()
        for i in range(len(dots)):
            dots[i].add_updater(move_dot(copy_dots[i]))

        self.add(dots)
        self.play(time.animate.set_value(2), run_time=4, rate_func=linear)


class Transmission(Scene):
    def construct(self):
        self.show_dots()
        self.compression_and_rarefaction()

    def show_dots(self):
        self.run_time = 5
        self.t = ValueTracker(0)
        self.amp = ValueTracker(0.5)
        self.kappa = ValueTracker(1)
        self.omega = ValueTracker(PI)
        self.opacity = ValueTracker(0)
        num_dots = 800
        self.pf_phase = always_redraw(
            lambda: ParametricFunction(
                lambda x: np.array(
                    [
                        x,
                        (
                            self.amp.get_value()
                            * np.sin(
                                self.kappa.get_value() * x
                                - self.omega.get_value() * self.t.get_value()
                            )
                        ),
                        0,
                    ]
                ),
                t_range=[-7.3, 7.3],
                color=RED,
                stroke_opacity=self.opacity.get_value(),
            )
        )
        self.pf = always_redraw(
            lambda: ParametricFunction(
                lambda x: np.array(
                    [
                        x,
                        (
                            self.amp.get_value()
                            * np.cos(
                                self.kappa.get_value() * x
                                - self.omega.get_value() * self.t.get_value()
                            )
                        ),
                        0,
                    ]
                ),
                t_range=[-7.3, 7.3],
                color=BLUE,
                stroke_opacity=0,
            )
        )
        self.add(self.pf, self.pf_phase)

        seed = random.seed(0)
        dots = VGroup(
            *[
                Dot().shift(RIGHT * random.uniform(-7, 7) + UP * random.uniform(-2, 2))
                for _ in range(num_dots)
            ]
        )
        copy_dots = dots.copy()

        def get_y(mob):
            for i in range(len(mob)):
                y = self.pf.get_point_from_function(copy_dots[i].get_x())
                mob[i].move_to(copy_dots[i].get_center() + RIGHT * y[1])

        dots.add_updater(lambda mob: get_y(mob))

        self.add(dots)
        self.t.set_value(-2)
        self.play(
            self.t.animate.set_value(2),
            self.opacity.animate.set_value(1),
            run_time=2 * self.run_time,
            rate_func=linear,
        )

        [
            dots[i].set_opacity(0.25) if i % 25 else dots[i].set_color(YELLOW)
            for i in range(len(dots))
        ]
        self.play(
            self.t.animate.set_value(4),
            run_time=self.run_time,
            rate_func=linear,
        )

    def compression_and_rarefaction(self):
        self.arrow_opacity = ValueTracker(0)

        def follow_wave(phase=0):
            def create_points():
                modulo = (
                    self.t.get_value() * self.omega.get_value() / self.kappa.get_value()
                    + phase / self.kappa.get_value()
                ) % (TAU / self.kappa.get_value())
                point = self.pf_phase.get_point_from_function(modulo)
                left_point = self.pf_phase.get_point_from_function(
                    modulo - (TAU / self.kappa.get_value())
                )
                return VGroup(
                    Dot(fill_opacity=0).move_to(left_point),
                    Dot(fill_opacity=0).move_to(point),
                )

            return create_points

        compression_label = Tex("Compression", color=RED).to_edge(UP)
        compression_dots = always_redraw(follow_wave(PI / 2))
        self.add(compression_dots)
        compression_arrow = always_redraw(
            lambda: VGroup(
                Arrow(compression_label, compression_dots[0], color=RED),
                Arrow(compression_label, compression_dots[1], color=RED),
            ).set_opacity(self.arrow_opacity.get_value())
        )

        self.add(compression_arrow)

        rarefaction_dots = always_redraw(follow_wave(phase=-PI / 2))
        self.add(rarefaction_dots)
        rarefaction_label = Tex("Rarefaction", color=BLUE).to_edge(DOWN)
        rarefaction_arrows = always_redraw(
            lambda: VGroup(
                Arrow(rarefaction_label, rarefaction_dots[0], color=BLUE),
                Arrow(rarefaction_label, rarefaction_dots[1], color=BLUE),
            ).set_opacity(self.arrow_opacity.get_value())
        )
        self.add(rarefaction_arrows)
        self.play(
            self.t.animate.set_value(6),
            Write(rarefaction_label),
            Write(compression_label),
            self.arrow_opacity.animate.set_value(1),
            run_time=self.run_time,
            rate_func=linear,
        )
        self.play(
            self.amp.animate.set_value(1),
            self.t.animate.set_value(8),
            run_time=self.run_time,
            rate_func=linear,
        )
        self.t.set_value(-2)
        self.play(
            self.t.animate.set_value(0),
            run_time=self.run_time,
            rate_func=linear,
        )
        self.play(
            self.kappa.animate.set_value(2),
            self.omega.animate.set_value(TAU),
            run_time=self.run_time,
            rate_func=linear,
        )
        self.play(
            self.t.animate.set_value(2),
            FadeOut(compression_label),
            FadeOut(rarefaction_label),
            self.arrow_opacity.animate.set_value(0),
            run_time=self.run_time,
            rate_func=linear,
        )
        self.play(
            self.t.animate.set_value(4),
            run_time=self.run_time,
            rate_func=linear,
        )


class MaxwellEquations(Scene):
    def construct(self):
        maxwell = ImageMobject("James_Clerk_Maxwell.png").scale(2)
        label = Text(
            "James C. Maxwell",
            gradient=(YELLOW, YELLOW, YELLOW, YELLOW, WHITE, BLUE, BLUE, BLUE, RED),
        )
        photo = Group(maxwell, label).arrange(DOWN)

        eq1 = MathTex(r"\nabla \cdot \mathbf{E} = \frac {\rho} {\varepsilon_0}")
        eq1[0][2].set_color(YELLOW)
        eq2 = MathTex(r"\nabla \cdot \mathbf{B} = 0")
        eq2[0][2].set_color([RED, BLUE])
        eq3 = MathTex(
            r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}} {\partial t}"
        )
        eq3[0][2].set_color(YELLOW)
        eq3[0][6].set_color([RED, BLUE])
        eq4 = MathTex(
            r"\nabla \times \mathbf{B} = \mu_0\left(\mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}} {\partial t})"
        )
        eq4[0][2].set_color([RED, BLUE])
        eq4[0][7].set_color(YELLOW_B)
        eq4[0][12].set_color(YELLOW)
        equations = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN)

        group_of_groups = Group(equations, photo).arrange(RIGHT)

        self.play(FadeIn(maxwell), Write(label))
        self.play(Write(equations))
        self.play(
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(photo),
            eq3.animate.move_to(ORIGIN + UP * 0.5),
            eq4.animate.move_to(ORIGIN + DOWN * 0.5),
        )

        magnet = Text("Magnetic field", gradient=(BLUE, RED)).to_corner(UR)
        m_a = Arrow(magnet.get_bottom(), eq3[0][7])
        current = Text("Current", color=YELLOW_B).to_edge(DOWN).shift(RIGHT)
        c_a = Arrow(current.get_top(), eq4[0][6])
        electric = Text("Electric field", color=YELLOW).to_corner(UL)
        e_a = Arrow(electric.get_bottom(), eq3[0][2])

        arrows = VGroup(magnet, current, electric, m_a, c_a, e_a)

        self.play(Write(arrows))
        self.play(Unwrite(arrows))
        time_varying_magnetic = VGroup(eq3[0][4:])
        time_varying_electric = VGroup(eq4[0][8:-1])
        self.play(
            Indicate(time_varying_electric),
        )
        self.play(
            Indicate(time_varying_magnetic),
        )
        self.play(
            Indicate(eq3[0][2]),
        )
        self.play(
            Indicate(eq4[0][7]),
        )
        self.play(
            Indicate(eq4[0][2]),
        )
        self.play(
            Wiggle(eq4[0][1]),
            Wiggle(eq3[0][1]),
        )

        self.wait()


class DeriveWaveFunction(Scene):
    def construct(self):
        self.setup_equations()
        self.setup_axes()
        self.show_time_dependence()
        self.wait(0.5)

    def setup_equations(self):
        self.ang_v_eqn = MathTex(
            r"{{\omega}} \equiv \frac{\theta}{t} {{\textrm{ rad/s} }}",
            tex_to_color_map={r"\omega": ORANGE},
        ).to_corner(UL)
        self.ang_v_eqn.submobjects[1][1].set_color(GREEN)

        self.theta_eqn = (
            MathTex(
                r"\theta = ",
                "\omega",
                r" t {{\textrm{ rad} }}",
                tex_to_color_map={r"\omega": ORANGE, r"\theta": GREEN},
            )
            .next_to(self.ang_v_eqn, DOWN)
            .align_to(self.ang_v_eqn, LEFT)
        )

        self.period_eqn = (
            MathTex("T = ", r"\frac{\tau}{\omega} {{\textrm{ s} }}")
            .next_to(self.theta_eqn, DOWN)
            .align_to(self.ang_v_eqn, LEFT)
        )
        self.period_eqn.submobjects[1][0].set_color(GREEN)
        self.period_eqn.submobjects[1][2].set_color(ORANGE)

        self.freq_eqn = (
            MathTex(
                r"f = \frac{1}{T} =",
                r"\frac{\omega}{\tau}",
                r"\textrm{ 1/s}",
            )
            .next_to(self.period_eqn, DOWN)
            .align_to(self.ang_v_eqn, LEFT)
        )
        self.freq_eqn.submobjects[1][0].set_color(ORANGE)
        self.freq_eqn.submobjects[1][2].set_color(GREEN)

        self.add(self.ang_v_eqn, self.theta_eqn, self.period_eqn, self.freq_eqn)
        self.wait()
        self.freq_eqn.generate_target()
        self.period_eqn.generate_target()
        group = VGroup(self.period_eqn.target, self.freq_eqn.target).to_corner(DL)
        self.play(
            MoveToTarget(self.freq_eqn),
            MoveToTarget(self.period_eqn),
        )

    def setup_axes(self):
        self.axes = Axes(
            x_range=[-2 * TAU, 2 * TAU, PI],
            y_range=[-2, 2],
            x_length=14,
            y_length=4,
            tips=False,
            x_axis_config={"color": GREEN},
        )
        self.axes.add_coordinates(
            dict(
                zip(
                    [x for x in np.arange(-4 * PI, 5 * PI, PI)],
                    [
                        MathTex(f"{x}\\pi")
                        if abs(x) > 1
                        else MathTex("\\pi")
                        if x == 1
                        else MathTex("-\\pi")
                        if x == -1
                        else ""
                        for x in range(-4, 5)
                    ],
                )
            )
        )
        self.play(Write(self.axes))

    def show_time_dependence(self):
        self.amp = ValueTracker(1)
        self.omega = ValueTracker(1)
        self.kappa = ValueTracker(1)
        self.time = ValueTracker(0)
        self.sin_curve = always_redraw(
            lambda: ParametricFunction(
                lambda x: self.axes.c2p(
                    x,
                    self.amp.get_value()
                    * np.cos(
                        self.kappa.get_value() * x
                        - self.omega.get_value() * self.time.get_value()
                    ),
                    0,
                ),
                t_range=[-4 * PI, 4 * PI],
                color=BLUE,
            )
        )

        zeroth_form = MathTex("f(", r"\theta", ")=", r"\cos(\theta)").to_edge(UP)
        zeroth_form.submobjects[0][0].set_color(BLUE)
        zeroth_form.submobjects[0][1].set_color(BLUE)
        zeroth_form.submobjects[2][0].set_color(BLUE)
        zeroth_form.submobjects[1][0].set_color(GREEN)
        zeroth_form.submobjects[3][4].set_color(GREEN)
        self.play(Write(zeroth_form), FadeIn(self.sin_curve), run_time=1)

        amp_line = always_redraw(
            lambda: DashedLine(
                self.axes.c2p(TAU / self.kappa.get_value(), 0, 0),
                self.sin_curve.get_point_from_function(TAU / self.kappa.get_value()),
                color=RED_A,
            )
        )
        first_form = MathTex(
            "f(", r"\theta", ")=", "A", r"\cos(\theta)", tex_to_color_map={"A": RED}
        ).to_edge(UP)
        first_form.submobjects[0][0].set_color(BLUE)
        first_form.submobjects[0][1].set_color(BLUE)
        first_form.submobjects[2][0].set_color(BLUE)
        first_form.submobjects[1][0].set_color(GREEN)
        first_form.submobjects[4][4].set_color(GREEN)
        amp_label = always_redraw(
            lambda: MathTex(
                "A = ", f"{np.round(self.amp.get_value(), decimals=2)}", color=RED
            )
            .move_to(DOWN * 3)
            .align_to(-2 * RIGHT, LEFT)
        )
        self.play(
            TransformMatchingTex(zeroth_form, first_form),
            Write(amp_line),
            Write(amp_label),
            run_time=1,
        )

        self.play(
            self.amp.animate.set_value(2),
            rate_func=there_and_back_with_pause,
            run_time=2,
        )

        wavelength = always_redraw(
            lambda: BraceBetweenPoints(
                self.sin_curve.get_point_from_function(0),
                self.sin_curve.get_point_from_function(TAU / self.kappa.get_value()),
                UP,
                color=PINK,
            )
        )
        length = MathTex(r"\lambda", color=PINK).next_to(wavelength, UP)
        length.add_updater(lambda m: m.next_to(wavelength, UP))
        second_form = MathTex(
            "f(",
            "x",
            ")=",
            "A",
            r"\cos(\frac{2 \pi}{\lambda} x)",
            tex_to_color_map={"A": RED},
        ).to_edge(UP)
        second_form.submobjects[0][0].set_color(BLUE)
        second_form.submobjects[0][1].set_color(BLUE)
        second_form.submobjects[2][0].set_color(BLUE)
        second_form.submobjects[1][0].set_color(GREEN_A)
        second_form.submobjects[4][7].set_color(PINK)
        second_form.submobjects[4][8].set_color(GREEN_A)
        self.play(Write(wavelength), Write(length), Unwrite(amp_line))
        self.remove(amp_line)
        self.play(TransformMatchingTex(first_form, second_form))

        third_form = MathTex(
            "f(", "x", ")=", "A", r"\cos(\kappa x)", tex_to_color_map={"A": RED}
        ).to_edge(UP)
        third_form.submobjects[0][0].set_color(BLUE)
        third_form.submobjects[0][1].set_color(BLUE)
        third_form.submobjects[2][0].set_color(BLUE)
        third_form.submobjects[1][0].set_color(GREEN_A)
        third_form.submobjects[4][4].set_color(PINK)
        third_form.submobjects[4][5].set_color(GREEN_A)
        self.play(TransformMatchingTex(second_form, third_form))

        kappa_label = always_redraw(
            lambda: MathTex(
                "\kappa = ",
                f"{np.round(self.kappa.get_value(), decimals=2)}",
                color=PINK,
            )
            .move_to(DOWN * 3)
            .align_to(ORIGIN, LEFT)
        )
        self.play(Write(kappa_label))
        self.play(self.kappa.animate.set_value(0.5))
        self.play(self.kappa.animate.set_value(2))
        self.play(Unwrite(wavelength), Unwrite(length))
        self.remove(wavelength, length)

        dot = always_redraw(
            lambda: Dot(color=YELLOW, radius=2 * DEFAULT_DOT_RADIUS).move_to(
                self.axes.c2p(
                    self.omega.get_value()
                    / self.kappa.get_value()
                    * self.time.get_value()
                    % TAU,
                    self.amp.get_value(),
                    0,
                )
            )
        )
        fourth_form = MathTex(
            "f(",
            "x",
            ",",
            "t",
            ")=",
            "A",
            r"\cos(\kappa x \pm \omega t)",
            tex_to_color_map={"A": RED},
        ).to_edge(UP)
        fourth_form.submobjects[0][0].set_color(BLUE)
        fourth_form.submobjects[0][1].set_color(BLUE)
        fourth_form.submobjects[1][0].set_color(GREEN_A)
        fourth_form.submobjects[2][0].set_color(BLUE)
        fourth_form.submobjects[4][0].set_color(BLUE)
        fourth_form.submobjects[6][4].set_color(PINK)
        fourth_form.submobjects[6][5].set_color(GREEN_A)
        fourth_form.submobjects[6][7].set_color(ORANGE)
        self.play(
            Wiggle(self.theta_eqn),
        )
        self.play(
            TransformMatchingTex(third_form, fourth_form),
            self.theta_eqn.animate.set_opacity(0.25),
        )

        omega_label = always_redraw(
            lambda: MathTex(
                "\omega = ",
                f"{np.round(self.omega.get_value(), decimals=2)}",
                color=ORANGE,
            )
            .move_to(DOWN * 3)
            .align_to(4 * RIGHT, LEFT)
        )
        time_label = always_redraw(
            lambda: MathTex("t = ", f"{np.round(self.time.get_value(), decimals=2)}")
            .move_to(DOWN * 3)
            .align_to(2 * RIGHT, LEFT)
        )
        self.play(Write(time_label), Write(omega_label), Create(dot), run_time=1)

        self.play(self.time.animate.set_value(TAU), rate_func=linear, run_time=TAU)
        self.wait()
        self.play(Wiggle(time_label), run_time=1)
        self.time.set_value(0)
        self.play(self.omega.animate.set_value(TAU))
        self.play(self.time.animate.set_value(1), rate_func=linear, run_time=1)
        self.time.set_value(0)

        velocity = MathTex("v =", r"\frac{\lambda}{T}").to_corner(UR)
        velocity.submobjects[0][0].set_color(MAROON)
        velocity.submobjects[1][0].set_color(PINK)
        self.play(
            Write(velocity), self.period_eqn.animate.set_opacity(0.25), run_time=1
        )
        velocity2 = MathTex("v =", r"\lambda f").to_corner(UR)
        velocity2.submobjects[0][0].set_color(MAROON)
        velocity2.submobjects[1][0].set_color(PINK)
        self.play(Wiggle(self.freq_eqn))
        self.play(
            ReplacementTransform(velocity, velocity2),
            self.freq_eqn.animate.set_opacity(0.25),
        )
        velocity3 = MathTex("v =", r"\frac{\omega}{\kappa}").to_corner(UR)
        velocity3.submobjects[0][0].set_color(MAROON)
        velocity3.submobjects[1][0].set_color(ORANGE)
        velocity3.submobjects[1][2].set_color(PINK)
        self.play(ReplacementTransform(velocity2, velocity3))

        # Short blurb about sampling rates
        self.play(
            self.omega.animate.set_value(config.frame_rate * TAU),
            self.time.animate.set_value(8),
            Unwrite(self.freq_eqn),
            Unwrite(self.period_eqn),
            Unwrite(self.theta_eqn),
            Unwrite(self.ang_v_eqn),
            rate_func=linear,
            run_time=8,
        )
        self.play(self.time.animate.set_value(13), rate_func=linear, run_time=5)
        self.play(
            self.omega.animate.set_value(config.frame_rate * TAU - 1),
            self.time.animate.set_value(14),
            rate_func=linear,
            run_time=1,
        )
        self.play(self.time.animate.set_value(17), rate_func=linear, run_time=3)
        self.play(
            self.omega.animate.set_value(config.frame_rate * TAU + 1),
            self.time.animate.set_value(18),
            rate_func=linear,
            run_time=1,
        )
        self.play(self.time.animate.set_value(21), rate_func=linear, run_time=3)


class FinishDerivation(Scene):
    def construct(self):
        self.setup_equation()
        self.wait()

    def setup_equation(self):
        fourth_form = MathTex(
            "f(",
            "x",
            ",",
            "t",
            ")=",
            "A",
            r"\cos(\kappa x \pm \omega t)",
            tex_to_color_map={"A": RED},
        ).to_edge(UP)
        fourth_form.submobjects[0][0].set_color(BLUE)
        fourth_form.submobjects[0][1].set_color(BLUE)
        fourth_form.submobjects[1][0].set_color(GREEN_A)
        fourth_form.submobjects[2][0].set_color(BLUE)
        fourth_form.submobjects[4][0].set_color(BLUE)
        fourth_form.submobjects[6][4].set_color(PINK)
        fourth_form.submobjects[6][5].set_color(GREEN_A)
        fourth_form.submobjects[6][7].set_color(ORANGE)
        self.add(fourth_form)
        fifth_form = MathTex(
            "f(",
            "x",
            ",",
            "t",
            ")=",
            "A",
            r"\cos(\kappa x \pm \omega t + \phi)",
            tex_to_color_map={"A": RED},
        ).to_edge(UP)
        fifth_form.submobjects[0][0].set_color(BLUE)
        fifth_form.submobjects[0][1].set_color(BLUE)
        fifth_form.submobjects[1][0].set_color(GREEN_A)
        fifth_form.submobjects[2][0].set_color(BLUE)
        fifth_form.submobjects[4][0].set_color(BLUE)
        fifth_form.submobjects[6][4].set_color(PINK)
        fifth_form.submobjects[6][5].set_color(GREEN_A)
        fifth_form.submobjects[6][7].set_color(ORANGE)
        fifth_form.submobjects[6][10].set_color(RED)
        self.play(TransformMatchingTex(fourth_form, fifth_form))
        minus_form = MathTex(
            "f(",
            "x",
            ",",
            "t",
            ")=",
            "A",
            r"\cos(\kappa x - \omega t + \phi)",
            tex_to_color_map={"A": RED},
        ).to_edge(UP)
        minus_form.submobjects[0][0].set_color(BLUE)
        minus_form.submobjects[0][1].set_color(BLUE)
        minus_form.submobjects[1][0].set_color(GREEN_A)
        minus_form.submobjects[2][0].set_color(BLUE)
        minus_form.submobjects[4][0].set_color(BLUE)
        minus_form.submobjects[6][4].set_color(PINK)
        minus_form.submobjects[6][5].set_color(GREEN_A)
        minus_form.submobjects[6][7].set_color(ORANGE)
        minus_form.submobjects[6][10].set_color(RED)
        self.play(ReplacementTransform(fifth_form, minus_form))

        partial_x = (
            MathTex(
                r"\frac{\partial f}{\partial x}",
                "=",
                r"-A \kappa",
                r"\sin(\kappa x - \omega t + \phi)",
            )
            .next_to(minus_form, DOWN)
            .align_to(7 * LEFT, LEFT)
        )
        partial_x.submobjects[0][1].set_color(BLUE)
        partial_x.submobjects[0][4].set_color(GREEN_A)
        partial_x.submobjects[2][1].set_color(RED)
        partial_x.submobjects[2][2].set_color(PINK)
        partial_x.submobjects[3][4].set_color(PINK)
        partial_x.submobjects[3][5].set_color(GREEN_A)
        partial_x.submobjects[3][7].set_color(ORANGE)
        partial_x.submobjects[3][10].set_color(RED)
        partial_t = (
            MathTex(
                r"\frac{\partial f}{\partial t}",
                "=",
                r"A \omega",
                r"\sin(\kappa x - \omega t + \phi)",
            )
            .next_to(minus_form, DOWN)
            .align_to(7 * RIGHT, RIGHT)
        )
        partial_t.submobjects[0][1].set_color(BLUE)
        partial_t.submobjects[2][0].set_color(RED)
        partial_t.submobjects[2][1].set_color(ORANGE)
        partial_t.submobjects[3][4].set_color(PINK)
        partial_t.submobjects[3][5].set_color(GREEN_A)
        partial_t.submobjects[3][7].set_color(ORANGE)
        partial_t.submobjects[3][10].set_color(RED)

        partial_x.submobjects[0].save_state()
        partial_t.submobjects[0].save_state()
        partial_x.submobjects[0].next_to(minus_form, DOWN).shift(LEFT)
        partial_t.submobjects[0].next_to(minus_form, DOWN).shift(RIGHT)
        self.play(
            Write(partial_x.submobjects[0]),
            Write(partial_t.submobjects[0]),
            lag_ratio=0.5,
        )
        self.play(
            partial_x.submobjects[0].animate.restore(),
            partial_t.submobjects[0].animate.restore(),
        )
        self.play(Indicate(minus_form.submobjects[6]))
        negative_sign_x = MathTex("-").next_to(partial_x.submobjects[3], LEFT)
        negative_sign_t = MathTex("-").next_to(partial_t.submobjects[3], LEFT)
        self.play(
            Write(partial_x.submobjects[1]),
            Write(partial_t.submobjects[1]),
            Write(partial_x.submobjects[3]),
            Write(partial_t.submobjects[3]),
            Write(negative_sign_t),
            Write(negative_sign_x),
            lag_ratio=0.5,
        )
        self.play(ReplacementTransform(negative_sign_x, partial_x.submobjects[2][0]))
        self.play(
            Indicate(minus_form.submobjects[6][5]),
        )
        self.play(
            TransformFromCopy(minus_form.submobjects[6][4], partial_x.submobjects[2][2])
        )
        self.play(
            TransformFromCopy(minus_form.submobjects[5][0], partial_x.submobjects[2][1])
        )
        self.play(
            Indicate(minus_form.submobjects[6][8]),
        )
        self.play(
            TransformFromCopy(
                minus_form.submobjects[6][7], partial_t.submobjects[2][1]
            ),
            Unwrite(negative_sign_t),
        )
        self.play(
            TransformFromCopy(
                minus_form.submobjects[5][0], partial_t.submobjects[2][0]
            ),
        )

        # Second partials
        partial_x_2 = (
            MathTex(
                r"\frac{\partial^2 f}{\partial x^2}",
                "=",
                r"-A \kappa^2",
                r"\cos(\kappa x - \omega t + \phi)",
            )
            .next_to(partial_x, DOWN)
            .align_to(7 * LEFT, LEFT)
        )
        partial_x_2.submobjects[0][2].set_color(BLUE)
        partial_x_2.submobjects[0][5].set_color(GREEN_A)
        partial_x_2.submobjects[0][6].set_color(GREEN_A)
        partial_x_2.submobjects[2][1].set_color(RED)
        partial_x_2.submobjects[2][2].set_color(PINK)
        partial_x_2.submobjects[2][3].set_color(PINK)
        partial_x_2.submobjects[3][4].set_color(PINK)
        partial_x_2.submobjects[3][5].set_color(GREEN_A)
        partial_x_2.submobjects[3][7].set_color(ORANGE)
        partial_x_2.submobjects[3][10].set_color(RED)

        partial_t_2 = (
            MathTex(
                r"\frac{\partial^2 f}{\partial t^2}",
                "=",
                r"-A \omega^2",
                r"\cos(\kappa x - \omega t + \phi)",
            )
            .next_to(partial_t, DOWN)
            .align_to(7 * RIGHT, RIGHT)
        )
        partial_t_2.submobjects[0][2].set_color(BLUE)
        partial_t_2.submobjects[2][1].set_color(RED)
        partial_t_2.submobjects[2][2].set_color(ORANGE)
        partial_t_2.submobjects[2][3].set_color(ORANGE)
        partial_t_2.submobjects[3][4].set_color(PINK)
        partial_t_2.submobjects[3][5].set_color(GREEN_A)
        partial_t_2.submobjects[3][7].set_color(ORANGE)
        partial_t_2.submobjects[3][10].set_color(RED)
        self.play(
            Write(partial_x_2.submobjects[0]),
            Write(partial_t_2.submobjects[0]),
        )
        self.play(
            Indicate(partial_x.submobjects[3]), Indicate(partial_t.submobjects[3])
        )
        self.play(
            Write(partial_x_2.submobjects[1]),
            Write(partial_t_2.submobjects[1]),
            Write(partial_x_2.submobjects[3]),
            Write(partial_t_2.submobjects[3]),
        )
        self.play(
            TransformFromCopy(
                partial_x.submobjects[2][0], partial_x_2.submobjects[2][0]
            ),
            TransformFromCopy(
                partial_x.submobjects[2][1], partial_x_2.submobjects[2][1]
            ),
            TransformFromCopy(
                partial_x.submobjects[2][2], partial_x_2.submobjects[2][2]
            ),
        )
        self.play(Indicate(partial_x.submobjects[3][5]))
        self.play(
            TransformFromCopy(
                partial_x.submobjects[3][4], partial_x_2.submobjects[2][3]
            )
        )
        self.play(
            TransformFromCopy(
                partial_t.submobjects[2][0], partial_t_2.submobjects[2][1]
            ),
            TransformFromCopy(
                partial_t.submobjects[2][1], partial_t_2.submobjects[2][2]
            ),
        )
        self.play(Indicate(partial_t.submobjects[3][8]))
        self.play(
            TransformFromCopy(
                partial_t.submobjects[3][7], partial_t_2.submobjects[2][3]
            ),
            TransformFromCopy(
                partial_t.submobjects[3][6], partial_t_2.submobjects[2][0]
            ),
        )
        da = Line(
            partial_x_2, partial_t_2, buff=0.1, stroke_width=20
        ).set_color_by_gradient([WHITE, WHITE, GREEN_A, GREEN_A])

        self.play(Create(da))
        wave_equation = (
            MathTex(
                r"\frac{\partial^2 f}{\partial x^2}",
                r"\frac{1}{\kappa^2}",
                "=",
                r"\frac{\partial^2 f}{\partial t^2}",
                r"\frac{1}{\omega^2}",
            )
            .next_to(da, DOWN)
            .shift(DOWN)
        )
        wave_equation.submobjects[0][2].set_color(BLUE)
        wave_equation.submobjects[0][5].set_color(GREEN_A)
        wave_equation.submobjects[0][6].set_color(GREEN_A)
        wave_equation.submobjects[1][2].set_color(PINK)
        wave_equation.submobjects[1][3].set_color(PINK)
        wave_equation.submobjects[3][2].set_color(BLUE)
        wave_equation.submobjects[4][2].set_color(ORANGE)
        wave_equation.submobjects[4][3].set_color(ORANGE)
        omega_sqr = VGroup(
            wave_equation.submobjects[4][2], wave_equation.submobjects[4][3]
        )
        self.play(
            Indicate(partial_x_2.submobjects[2][2]),
            Indicate(partial_x_2.submobjects[2][3]),
            Indicate(partial_t_2.submobjects[2][2]),
            Indicate(partial_t_2.submobjects[2][3]),
        )
        self.play(Write(wave_equation), Uncreate(da))
        self.play(
            Unwrite(wave_equation.submobjects[1][0]),
            Unwrite(wave_equation.submobjects[4][0]),
            Unwrite(wave_equation.submobjects[4][1]),
        )
        self.play(
            omega_sqr.animate.move_to(
                wave_equation.submobjects[1][0].get_center() + UP * 0.2
            ),
        )
        velocity = MathTex("v^2", color=MAROON).move_to(wave_equation.submobjects[1][1])
        kappa_sqr = VGroup(
            wave_equation.submobjects[1][1],
            wave_equation.submobjects[1][2],
            wave_equation.submobjects[1][3],
        )
        w_k_2 = VGroup(omega_sqr, kappa_sqr)
        self.play(ReplacementTransform(w_k_2, velocity))


class RecallWaveSpeed(Scene):
    def construct(self):
        student = Quarter(mode="pondering", color=BLUE)
        # student.get_bubble(r"v=\frac{\omega}{\kappa}", bubble_class=ThoughtBubble)
        b = student.get_bubble(r"H o v ", bubble_class=ThoughtBubble)
        b.shift(2 * DOWN)
        velocity3 = MathTex("v =", r"\frac{\omega}{\kappa}").move_to(b).shift(UL * 0.3)
        velocity3.submobjects[0][0].set_color(MAROON)
        velocity3.submobjects[1][0].set_color(ORANGE)
        velocity3.submobjects[1][2].set_color(PINK)
        self.add(student, b)
        self.wait()
        self.play(FadeIn(velocity3))
        self.wait()
        self.play(student.animate.blink(), rate_func=there_and_back)
        self.wait()


class ThresholdHearing(Scene):
    def construct(self):
        t1 = Table(
            [
                ["Source", "Distance", "Pa"],
                ["Hearing begins", "At ear", "0.0000200"],
                ["Calm breathing", "Ambient", "0.0000632"],
                ["Calm room", "Ambient", "0.000632"],
                ["Whispering", "1 m", "0.002-0.02"],
                ["Talking", "1 m", "0.002-0.02"],
                ["Ticking watch", "1 m", ".0002"],
                ["Hearing damage", "At ear", ".36"],
                ["Busy traffic", "10 m", "0.2-0.63"],
                ["Car stereo", "1 m", "2.0"],
                ["Jackhammer", "1 m", "2.0"],
                ["Chainsaw", "1 m", "6.32"],
                ["Pain", "At ear", "20+"]
            ],
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT}
        )
        t1.scale(0.3).to_edge(LEFT)
        self.add(t1)

class RadialWaves(OpenGLSurface):
    def __init__(
        self,
        *sources,
        wavelength=1,
        period=1,
        amplitude=0.3,
        x_range=[-5, 5],
        y_range=[-5, 5],
        **kwargs,
    ):
        self.wavelength = wavelength
        self.period = period
        self.amplitude = amplitude
        self.dampening = 1
        self.time = 0
        self.extra = {**kwargs}
        self.sources = sources
        self.u_range = x_range
        self.v_range = y_range
        super().__init__(
            lambda u, v: np.array([u, v, self.wave_z(u, v, *sources)]),
            u_range=self.u_range,
            v_range=self.v_range,
            **kwargs,
        )

    def wave_z(self, u, v, *sources):
        z = 0
        for source in sources:
            x0, y0, z0 = source
            distance_from_source = ((u - x0) ** 2 + (v - y0) ** 2) ** 0.5

            decay = np.exp(-self.dampening * self.time)
            phi = 0
            wavelength = self.wavelength
            if distance_from_source < 0.001:
                distance_from_source = 0.001
            z += (
                self.amplitude
                # * decay
                # / (distance_from_source ** 2)
                * np.cos(2*PI/wavelength * distance_from_source - self.time * PI + phi)
            )
        return z

    def update_wave(self, mob, dt):
        self.time += dt
        mob.become(
            OpenGLSurface(
                lambda u, v: np.array([u, v, self.wave_z(u, v, *self.sources)]),
                u_range=self.u_range,
                v_range=self.v_range,
                **self.extra,
            )
        )

    def start_wave(self):
        self.add_updater(self.update_wave)

    def stop_wave(self):
        self.remove_updater(self.update_wave)

class SignOff(Scene):
    def construct(self):
        l8r = Json(mode="happy").look_at(ORIGIN+2*UP+RIGHT*.5)
        homies = Text("Thanks for watching!",gradient=(RED,GREEN)).to_edge(UP)
        self.add(l8r)
        self.play(l8r.animate.blink(), rate_func=there_and_back_with_pause)
        self.play(Write(homies), l8r.animate.look_at(homies))
        self.play(l8r.animate.change_mode("hooray"))
        self.play(l8r.animate.blink(), rate_func=there_and_back_with_pause)
        self.wait()
class TwoDWave(Scene):
    def construct(self):
        self.renderer.camera = OpenGLCamera()
        self.renderer.camera.rotate_about_origin(3/8*PI, RIGHT)
        self.renderer.camera.rotate_about_origin(3/8*PI, OUT)
        self.renderer.camera.scale(2)
        s = RadialWaves(ORIGIN, color=BLUE_B)
        self.add(s)
        s.start_wave()
        self.wait(8)
        self.interactive_embed()

class Musimathics(Scene):
    def construct(self):
        loy = ImageMobject("GarethLoyHeadShotWeb")
        label= Tex("Gareth Loy")
        group_l = Group(loy, label).scale(1).arrange(DOWN)

        me = Json(mode="happy").to_corner(DL) # *grunting noises*
        me.look_at(loy)

        m1 = ImageMobject("musimathics1").scale_to_fit_width(2.6).to_edge(DR)
        m2 = ImageMobject("musimathics2").scale_to_fit_width(2.6).to_corner(UR)
        self.play(FadeIn(group_l), FadeIn(me))
        self.play(FadeIn(m1), FadeIn(m2), lag_ratio=.6)

        self.wait()
        self.play(FadeOut(group_l))
        bub= me.get_bubble("Interesting!").shift(.25*DR)
        self.play(me.animate.change_mode("pondering"), FadeIn(bub))
        bub.content.shift(.25*DR)
        self.play(Write(bub.content))
        self.wait()

class Inefficient(MusicScene):
    def construct(self):
        self.teacher.make_eye_contact(self.creatures[0])
        self.wait()
        self.teacher.make_eye_contact(self.creatures[0])
        anim1 = self.teacher_says("Inefficient!", target_mode="giddy")
        self.change_student_modes(
            "jawdrop",
            "puzzled",
            "pondering",
            "erm",
            "jawdrop",
            added_anims=anim1
        )
        self.joint_blink()
        self.play(
            self.teacher.animate.make_eye_contact(self.creatures[4])
        )
        self.play(Uncreate(self.teacher.bubble), Unwrite(self.teacher.bubble.content))
        self.wait()
        anim2 = self.teacher_says("You!", target_mode="hooray")
        self.change_student_modes(
            "hooray",
            "happy",
            "happy",
            "happy",
            "hooray",
            added_anims=anim2
        )
        self.wait()
        self.joint_blink()
        self.wait()
        self.wait()

class Takeaway(Scene):
    def construct(self):
        student = Quarter(mode="pondering", color=PINK).to_corner(DR)
        b = ThoughtBubble()
        small_bub = Circle(color=WHITE).scale(.25).next_to(student.get_center() + LEFT)
        c = b[-1].scale(2).shift(UL)
        self.add(student,small_bub, c)
        self.wait()
        self.play(student.animate.blink(), rate_func=there_and_back)
class WaveEquation(Scene):
    def construct(self):
        self.setup_axes()
        self.show_3d()

    def setup_axes(self):
        self.axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
            x_length=config.frame_height - 1.5,
            y_length=config.frame_height - 1.5,
            z_length=config.frame_height - 1.5,
            depth_test=True,
        )
        # self.axes.add_coordinates(
        #     dict(
        #         zip(
        #             [x for x in np.arange(-TAU, TAU, PI)],
        #             [
        #                 MathTex(f"{x}\\pi")
        #                 if abs(x) > 1
        #                 else MathTex("\\pi")
        #                 if x == 1
        #                 else MathTex("-\\pi")
        #                 if x == -1
        #                 else ""
        #                 for x in range(-4, 5)
        #             ],
        #         )
        #     ),
        #     range(-2, 3, 1),
        #     None
        # )
        x_axis = self.axes.x_axis
        x_numbers = x_axis.get_number_mobjects(*range(1,11))
        x_axis_label = Tex("x")
        x_axis_label.next_to(x_axis.get_right(), UP)
        self.add(self.axes)
        self.add(x_axis_label, x_numbers)
        # time_label = Tex("Time").rotate(PI/2, about_point=ORIGIN,axis=RIGHT).rotate(PI/2, about_point=ORIGIN,axis=OUT).shift(self.axes.c2p(0,2,2))
        # self.add(time_label)

    def show_3d(self):
        self.amp = ValueTracker(1)
        self.omega = ValueTracker(TAU)
        self.kappa = ValueTracker(1)
        self.time = ValueTracker(1)

        self.pf = always_redraw(
            lambda: ParametricSurface(
                lambda u,v: self.axes.c2p(
                    u,
                    v,
                    self.amp.get_value()
                    * np.cos(
                        self.kappa.get_value()*u
                        - self.omega.get_value() * v
                    ),
                ),
                u_range=[-TAU,TAU],
                v_range=[0,3],
                fill_opacity=.5,
                checkerboard_colors=[DARK_GRAY,LIGHT_GRAY]
            )
        )
        # self.add(self.pf)

        self.plane = always_redraw(
            lambda: Rectangle(
                width=self.axes.c2p(TAU,0,0)[0],
                height=self.axes.c2p(0,2,0)[1],
                fill_opacity=.5,
                fill_color=LIGHT_GRAY
            ).rotate(PI/2, about_point=ORIGIN,axis=RIGHT).shift(self.axes.c2p(PI,self.time.get_value(),0))
        )
        # self.add(self.plane)
        self.cos = always_redraw(
            lambda: ParametricFunction(
                lambda x: self.axes.c2p(
                    x,
                    self.time.get_value(),
                    (
                        self.amp.get_value()
                        * np.cos(
                            self.kappa.get_value()* x - self.omega.get_value() * self.time.get_value()
                        )
                    ),
                ),
                t_range=[-TAU, TAU],
                color=BLUE,
            )
        )
        # self.add(self.cos)
        self.renderer.camera = OpenGLCamera(euler_angles=[0,PI/2,0],center_point=self.axes.c2p(PI, 1, 0))
        # self.play(
        #     self.time.animate.set_value(3),
        #     run_time=3,
        #     rate_func=linear,
        # )
        # self.play(
        #     self.time.animate.set_value(0),
        #     run_time=1,
        #     rate_func=linear,
        # )
        # self.play(
        #     self.kappa.animate.set_value(2),
        #     rate_func=linear,
        # )
        # Plane = Axes(x_range =[-5,5,1],y_range =[-5,5,1])
        # Graph = Plane.get_graph(lambda x : x**2)
        # Secant = Plane.get_secant_slope_group(graph=Graph,x=0.4,dx=0.1)

        
        # self.add(Graph,Plane,Secant)
        dot_x = Dot().shift(self.axes.c2p(1,0,0))
        dot_y = Dot().shift(self.axes.c2p(0,2,0))
        dot_z = Dot().shift(self.axes.c2p(0,0,3))
        self.add(dot_x, dot_y, dot_z)
        self.interactive_embed()

class Section2(Scene):
    def construct(self):
        title = Tex("How is sound made?")
        self.play(
            Write(title)
        )
        self.play(
            Unwrite(title, reverse=False)
        )
        self.wait()

class Section3(Scene):
    def construct(self):
        title = Tex("Auditory perception")
        self.play(
            Write(title)
        )
        self.play(
            Unwrite(title, reverse=False)
        )
        self.wait()

class Section4(Scene):
    def construct(self):
        title = Tex("Geometric basis of sound")
        self.play(
            Write(title)
        )
        self.play(
            Unwrite(title, reverse=False)
        )
        self.wait()

class Section5(Scene):
    def construct(self):
        title = Tex("The wave equation")
        self.play(
            Write(title)
        )
        self.play(
            Unwrite(title, reverse=False)
        )
        self.wait()