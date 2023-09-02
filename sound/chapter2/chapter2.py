from manim import *
from manim.opengl import *
from manim.utils import *
from manim.renderer.opengl_renderer import OpenGLCamera
from scipy.io import wavfile
from typing import Optional
from sound import *
from pydub import AudioSegment
from scipy import special


SR = 48000  # Sample Rate
BD = 2  # Byte depth a.k.a. bit depth
EXPANDED_BD = int(2 ** (8 * BD) // 2 - 1)
CHANNELS = 2
MEDIA_DIR = "../assets/creatures/svg_images/"

# Pythagorean Intervals
PYTH_MINOR_SECOND = 256 / 243
PYTH_MAJOR_SECOND = 9 / 8
PYTH_MINOR_THIRD = 32 / 27
PYTH_MAJOR_THIRD = 81 / 64
PYTH_PERFECT_FOURTH = 4 / 3
PYTH_DIMINISHED_FIFTH = 1024 / 729
PYTH_AUGMENTED_FOURTH = 729 / 512
PYTH_PERFECT_FIFTH = 3 / 2
PYTH_MINOR_SIXTH = 128 / 81
PYTH_MAJOR_SIXTH = 27 / 16
PYTH_MINOR_SEVENTH = 16 / 9
PYTH_MAJOR_SEVENTH = 243 / 128
PYTH_OCTAVE = 2.0
PYTHAGOREAN_MAJOR_SCALE = [
    PYTH_MAJOR_SECOND,
    PYTH_MAJOR_THIRD,
    PYTH_PERFECT_FOURTH,
    PYTH_PERFECT_FIFTH,
    PYTH_MAJOR_SIXTH,
    PYTH_MAJOR_SEVENTH,
    PYTH_OCTAVE,
]
PYTHAGOREAN_CHROMATIC_SCALE = [
    PYTH_MINOR_SECOND,
    PYTH_MAJOR_SECOND,
    PYTH_MINOR_THIRD,
    PYTH_MAJOR_THIRD,
    PYTH_PERFECT_FOURTH,
    PYTH_AUGMENTED_FOURTH,
    PYTH_PERFECT_FIFTH,
    PYTH_MINOR_SIXTH,
    PYTH_MAJOR_SIXTH,
    PYTH_MINOR_SEVENTH,
    PYTH_MAJOR_SEVENTH,
    PYTH_OCTAVE,
]


def segment(
    x: np.array, frame_rate=SR, sample_width=BD, channels=CHANNELS
) -> AudioSegment:
    """
    Helper function to package audio data into a PyDub Audio segment for use
    with the Manim's SceneFileWriter.
    """
    a = np.int16(EXPANDED_BD * x)
    return AudioSegment(
        a.tobytes(), frame_rate=frame_rate, sample_width=sample_width, channels=channels
    )


class NewMarketLogo(MovingCameraScene):
    def setup(self):
        MovingCameraScene.setup(self)

    def construct(self):
        self.graph_origin = np.array([0, 0, 0])
        self.camera.frame.save_state()
        self.axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            tips=False,
            axis_config={"include_numbers": True},
        )

        def stock_curve(x):
            return (x - 0.125) ** 4 * (x + 1.875)

        graph = self.axes.plot(stock_curve, color=BLUE, x_range=[-4, 3])
        deriv_graph = self.axes.plot_derivative_graph(graph)
        dolly = self.axes.plot(stock_curve, color=BLACK, x_range=[-3, 0])

        def candlesticks(x):
            coord = self.axes.input_to_graph_point(x, graph)
            before_coord = self.axes.input_to_graph_point(x - 0.45, graph)
            after_coord = self.axes.input_to_graph_point(x + 0.45, graph)
            deriv_coord = self.axes.input_to_graph_point(x, deriv_graph)
            color = GREEN
            thin_top = after_coord[1]
            thin_bot = before_coord[1]
            if deriv_coord[1] < 0:
                color = RED
                tmp = thin_top
                thin_top = thin_bot
                thin_bot = tmp
            height = coord[1]
            if x == -2:
                height *= 2.5

            r = Rectangle(
                fill_opacity=1, color=color, width=0.1, height=height
            ).move_to(RIGHT * coord[0] + UP * coord[1])
            top = Line(color=color, start=coord, end=(coord[0], thin_top, 0))
            bot = Line(color=color, start=coord, end=(coord[0], thin_bot, 0))
            return VGroup(r, top, bot)

        sticks = [candlesticks(x) for x in range(-2, 2)]
        sticks.pop(2)
        moving_dot = Dot(fill_opacity=0).move_to(dolly.points[0])
        self.add(moving_dot)
        self.camera.frame.scale(0.5).move_to(moving_dot)
        self.add(self.camera.frame)

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        candles = VGroup(*sticks)
        logo = SVGMobject("newmarket.svg").scale(0.5).move_to(0.5 * UP)
        logo.submobjects[0].set(stroke_width=0)
        logo.submobjects[1].set(stroke_width=0)
        self.play(
            AnimationGroup(
                MoveAlongPath(
                    moving_dot,
                    dolly,
                    rate_func=rate_functions.ease_out_cubic,
                    run_time=3,
                ),
                Write(graph, run_time=2.5, rate_func=rate_functions.ease_in_out_circ),
                Write(candles, run_time=4),
            ),
            Write(logo, run_time=3, rate_func=rush_into),
        )
        self.camera.frame.remove_updater(update_curve)

        self.play(
            AnimationGroup(
                Uncreate(graph),
                Uncreate(candles),
                logo.animate.shift(0.15 * DOWN),
                logo.submobjects[2].animate.set_opacity(0).shift(0.15 * DOWN),
            ),
            self.camera.frame.animate.scale(0.005),
        )
        self.wait()


class Chapter2Opening(Scene):
    def construct(self):
        # line = Text("Works of art make rules;", t2c={"[:12]": BLUE, "[18:23]": YELLOW})
        # line1 = Text(
        #     "rules do not make works of art.",
        #     t2c={"[:5]": YELLOW, "[6:12]": RED, "[18:30]": BLUE},
        # )
        # line.to_edge(UP, buff=2)
        # line1.next_to(line, DOWN).align_to(line, RIGHT)
        # author = Text("— Claude Debussy")
        line = Text(
            "Music is the pleasure the human mind",
            t2c={"Music": PURPLE, "pleasure": BLUE, "human mind": GREEN},
        ).to_edge(UP, buff=2)
        line1 = (
            Text(
                "experiences from counting without being",
                t2c={"experiences": YELLOW, "counting": ORANGE},
            )
            .next_to(line, DOWN)
            .align_to(line, RIGHT)
        )
        line2 = (
            Text("aware that it is counting.", t2c={"counting": ORANGE})
            .next_to(line1, DOWN)
            .align_to(line, RIGHT)
        )
        author = Text("— Gottfried Wilhelm Leibniz", color=RED)
        author.next_to(line2, DOWN).align_to(line2, RIGHT)
        quote = VGroup(line, line1, line2, author).center()

        self.play(
            LaggedStart(
                Write(line),
                Write(line1),
                Write(line2),
                lag_ratio=0.75,
            )
        )
        self.wait()
        self.play(Write(author), run_time=2, rate=smooth)

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
            VGroup(*[l1, l2, l3, l4, l5])
            .move_to(ORIGIN)
            .shift(DOWN)
            .set_color(DARK_GRAY)
        )
        self.play(ReplacementTransform(quote, staff))
        self.wait()


class Hook(MusicScene):
    def construct(self):
        fader = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.5,
            stroke_opacity=0,
        )
        self.wait()
        self.add(fader, self.teacher)
        self.play(FadeIn(fader))
        thought = self.teacher_thinks("", bubble_kwargs={"width": 3})
        self.play(*thought)
        self.joint_blink()
        self.wait()
        self.play(FadeOut(fader), FadeOut(self.mobjects[-2]))
        self.wait()
        self.joint_blink()
        self.change_student_modes(
            *["pondering", "puzzled", "plain", "pondering", "erm"],
            look_at_arg=self.teacher.get_top(),
            lag_ratio=0.04,
        )
        self.wait()


class MonchoRoastingMe(Scene):
    def construct(self):
        me = Json().move_to(2 * LEFT)
        me.change_mode("hooray")
        me.set(height=2.5)
        brother = TrebleCreature(color=GREY).flip().shift(2 * RIGHT)
        brother.set(height=3)
        brother.align_to(me, DOWN)
        brother.look_at(me)
        brother.save_state()
        brother.look_at(me)
        brother.to_edge(RIGHT)
        self.play(FadeIn(me))
        self.play(FadeIn(brother))
        self.wait()
        self.play(brother.animate.restore())
        question = brother.get_bubble("Who sings that song?")
        answer = me.get_bubble("Chester Bennington")
        roast = brother.get_bubble("Let's keep it that way!")
        self.play(Write(question), me.animate.look_at(brother), run_time=0.3)
        self.wait()
        self.play(Unwrite(question, reverse=False), run_time=0.1)
        self.play(Write(answer), me.animate.change_mode("smirk"), run_time=0.3)
        self.wait()
        self.play(Unwrite(answer, reverse=False), run_time=0.1)
        self.play(
            Write(roast),
            brother.animate.change_mode("smirk"),
            lag_ratio=0.3,
            run_time=0.3,
        )
        self.play(me.animate.change_mode("sad"))
        self.play(me.animate.look(DOWN))
        self.wait()


class Infathomable(Scene):
    def construct(self):
        me = Json()
        me.change_mode("pondering")
        me.set(height=2.5)
        self.add(me)
        self.wait()
        self.play(Blink(me))
        self.wait()


class Introduction(MusicScene):
    def __init__(self):
        super().__init__(GREY_BROWN)

    def construct(self):
        self.change_student_modes(
            *["pondering", "puzzled", "plain", "pondering", "erm"],
            look_at_arg=self.teacher.get_top(),
            lag_ratio=0.04,
        )
        self.show_series()
        self.show_outline()

    def show_series(self):
        self.series = VideoSeries(num_videos=5)
        self.series.to_edge(UP)
        prev_video = self.series[0]
        this_video = self.series[1]
        prev_video.set_color(GRAY)
        this_video.set_color(YELLOW)
        elip = (
            MathTex(r"\cdots")
            .set(width=self.series[-1].width * 0.9)
            .move_to(self.series[-1])
        )
        self.series[-1] = elip
        for v in self.series:
            v.save_state()
        self.teacher.change_mode("pondering")
        self.series[2:].shift(RIGHT * 14)
        self.play(
            FadeIn(prev_video), FadeIn(this_video), self.staff.animate.set_color(WHITE)
        )
        self.remove(prev_video, this_video)
        self.add(self.series)
        self.play(
            Blink(self.teacher),
        )
        self.play(
            AnimationGroup(
                *[v.animate.restore() for v in self.series[1:]], lag_ratio=0.2
            ),
            run_time=2,
        )
        self.change_student_modes(
            *["happy", "puzzled", "happy", "pondering", "erm"],
            look_at_arg=self.teacher.get_top(),
            lag_ratio=0.04,
        )

    def show_outline(self):
        this_video = self.series[1]
        self.play(
            FadeOut(self.staff),
            FadeOut(self.creatures),
            *[FadeOut(self.series[i]) for i in range(len(self.series) - 1) if i != 1],
            FadeOut(self.series[-1]),
            this_video[0].animate.set_opacity(0),
        )
        self.play(
            this_video[1].animate.move_to(ORIGIN).set(width=config.frame_width - 1),
        )
        section1 = Text("Intervals")
        section2 = (
            Text("Superposition & Linearity")
            .next_to(section1, DOWN)
            .align_to(section1, LEFT)
        )
        section3 = (
            Text("Resonance, Overtones & Harmonics")
            .next_to(section2, DOWN)
            .align_to(section1, LEFT)
        )
        section4 = Text("Formants").next_to(section3, DOWN).align_to(section1, LEFT)
        sections = VGroup(section1, section2, section3, section4).move_to(ORIGIN)
        self.play(Write(section1))
        self.play(Write(section2))
        self.play(Write(section3))
        self.play(Write(section4))
        self.wait()
        self.play(
            FadeOut(sections),
        )
        self.play(this_video.animate.set_color(GRAY))


class AudioGenerator:
    def __init__(
        self,
        freq: Optional[float] = 440.0,
        volume: Optional[float] = 0.5,
        pan: Optional[float] = 0.5,
    ):
        """
        Freq - frequency of tone
        Volume - Audio volume
        Pan - Left (0) Center (.5) Right (1)
        """
        self.f_i = freq
        self.f_f = freq
        log_freq = np.log10(freq)
        self.v_i = volume
        self.v_f = volume
        self.p_i = pan
        self.p_f = pan
        self.freq_t = ValueTracker(freq)
        self.log_freq_t = ValueTracker(log_freq)
        self.vol_t = ValueTracker(volume)
        self.last_val = 0.0
        self.second_last_val = 0.0
        self.duration = 0.0
        self.last_freq = 0.0

    def __repr__(self):
        return f"\
        Freq: {self.f_i} {self.f_f}\
        Volume: {self.v_i} {self.v_f}\
        Pan: {self.p_i} {self.p_f}\
        "

    def modify(
        self, freq=None, vol=None, pan=None, rate_func=linear, use_last_val=True
    ):
        """
        Freq - frequency of tone
        Volume - Audio volume
        Pan - Left (0) Center (.5) Right (1)
        """
        if freq is None:
            freq = self.f_i
        if vol is None:
            vol = self.v_i
        if pan is None:
            pan = self.p_i
        self.use_last_val = use_last_val
        self.f_f = freq
        F_f = np.log10(freq)

        self.v_f = vol
        self.p_f = pan
        anims = [
            self.log_freq_t.animate.set_value(F_f),
            self.freq_t.animate(rate_func=rate_func if rate_func else linear).set_value(
                self.f_f
            ),
            self.vol_t.animate(rate_func=rate_func if rate_func else linear).set_value(
                self.v_f
            ),
        ]
        return anims

    def freq_interp(
        self, duration, f1, f2, phi=0.0, use_last_val=False, rate_func=linear
    ):
        """
        Smoothly interpolates sinusoid wave form between two frequencies.
        """
        num_samples = int(SR * duration)
        if rate_func == linear:
            f = np.linspace(f1, f2, num_samples, endpoint=False)
            phase = 2 * np.pi * np.cumsum(f) / SR
        else:
            log_f1 = np.log10(f1)
            log_f2 = np.log10(f2)
            f = np.logspace(log_f1, log_f2, num_samples, endpoint=False)
            phase = 2 * np.pi * np.cumsum(f) / SR
        self.duration += duration

        if use_last_val:
            phi = np.arccos(self.last_val)
            if self.second_last_val > self.last_val:
                phi *= -1.0
        samples = np.cos(phase - phi)

        self.last_val = samples[-1]
        self.second_last_val = samples[-2]
        self.last_freq = f2
        self.f_i = f2
        return f, samples

    def volume_filter(self, dur, v1, v2):
        num_samples = int(SR * dur)
        if v2 == 0:
            v2 = 0.00001
        if v1 == 0:
            v1 = 0.00001

        buffer = np.geomspace(v1, v2, endpoint=True, num=num_samples)
        # buffer = np.linspace(v1, v2, endpoint=True, num=num_samples)
        self.v_i = v2
        return buffer

    def pan(self, n: np.array, s: float, t: float) -> np.array:
        """
        Takes a mono audio source and pans it left, or right, into a stereo audio output.
        0 is left, .5 is center, 1, is right.

        n - Mono audio source
        s - starting pan
        t - ending pan
        """
        l_s = 2.0 * (-s + 1.0) if s > 0.5 else 1.0
        l_t = 2.0 * (-t + 1.0) if t > 0.5 else 1.0
        r_s = 2.0 * s if s < 0.5 else 1.0
        r_t = 2.0 * t if t < 0.5 else 1.0
        left = n * np.linspace(l_s, l_t, len(n), True)
        right = n * np.linspace(r_s, r_t, len(n), True)
        panned = np.vstack((left, right)).T
        self.p_i = t
        return panned

    def next(self, duration=1.0, use_last_val=True, rate_func=linear):
        f, x = self.freq_interp(
            duration, self.f_i, self.f_f, use_last_val=use_last_val, rate_func=rate_func
        )
        x *= self.volume_filter(duration, self.v_i, self.v_f)
        xs = self.pan(x, self.p_i, self.p_f)

        # fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
        # ax1.plot(t, new_t)
        # ax1.set_title("Time Remap")
        # ax2.plot(t, f)
        # ax2.set_title("Frequency plot")
        # ax3.plot(t[::2], xs[1::2])
        # ax3.set_title("AUDIO")
        return segment(xs)


class AudioScene(Scene):
    def __init__(self, audio_generators=[], **kwargs):
        super().__init__(**kwargs)
        self.audio_generators: list[AudioGenerator] = audio_generators

    def add_audio_generator(self, gen: AudioGenerator = AudioGenerator()):
        self.audio_generators.append(gen)

    def wait(
        self,
        duration: float = DEFAULT_WAIT_TIME,
        stop_condition: Callable[[], bool] | None = None,
        frozen_frame: bool | None = None,
        **kwargs,
    ):
        self.play(
            Wait(
                duration,
                stop_condition=stop_condition,
                frozen_frame=frozen_frame,
            ),
            run_time=duration,
            **kwargs,
        )

    def play(
        self,
        *args,
        subcaption=None,
        subcaption_duration=None,
        subcaption_offset=0,
        **kwargs,
    ):
        offset = self.renderer.time
        super().play(*args, **kwargs)
        time = float(kwargs.get("run_time", 1.0))
        rate = kwargs.get("rate_func", linear)
        use_last = kwargs.get("use_last_value", True)
        for gen in self.audio_generators:
            seg = gen.next(duration=time, rate_func=rate, use_last_val=use_last)
            self.renderer.file_writer.add_audio_segment(seg, offset)


class Intervals(AudioScene):
    def __init__(self):
        super().__init__(random_seed=0)

    def construct(self):
        self.nl()
        self.interval()
        self.consonant()
        self.dissonant()

    def nl(self):
        self.x = NumberLine(
            # x_range=[1, 5],
            # length=14.2,
            x_range=[1.301029, 4.301029],
            length=13,
            include_ticks=False,
            scaling=LogBase(10),
        )
        custom_ticks = [20, 200, 2000, 20000]
        self.x.ticks = VGroup()
        for t in custom_ticks:
            self.x.ticks.add(self.x.get_tick(t))
        self.x.add(self.x.get_tick_marks())
        self.x.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.add(self.x)

        y = (
            NumberLine(
                x_range=[1.301029, 4.301029],
                length=13,
                include_ticks=False,
                scaling=LogBase(10),
            )
            .to_edge(DOWN)
            .shift(UP)
        )
        y.ticks = VGroup()
        for t in custom_ticks:
            y.ticks.add(y.get_tick(t))
        y.add(y.get_tick_marks())
        y.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )

        self.left_channel = AudioGenerator(20, 0.0, 0.5)
        self.left = always_redraw(
            lambda: Dot(self.x.n2p(self.left_channel.freq_t.get_value())).set_opacity(
                4 * self.left_channel.vol_t.get_value()
            )
        )
        self.add(self.left)
        self.add_audio_generator(self.left_channel)
        self.play(
            *self.left_channel.modify(2000, 0.25, 0.5),
            run_time=2,
            rate_func=rate_functions.loglinear,
        )
        self.play(
            *self.left_channel.modify(200, 0.25, 0.5),
            run_time=2,
            rate_func=rate_functions.loglinear,
        )
        self.play(*self.left_channel.modify(420.69, 0.25, 0.5), run_time=2)
        self.play(
            *self.left_channel.modify(420.69, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )

        self.right_channel = AudioGenerator(420.69 / 8, 0.0, 0.5)
        self.right = always_redraw(
            lambda: Dot(
                self.x.n2p(self.right_channel.freq_t.get_value()), color=RED
            ).set_opacity(4 * self.right_channel.vol_t.get_value()),
        )
        self.add(self.right)
        self.add_audio_generator(self.right_channel)
        self.play(
            *self.right_channel.modify(420.69 / 4, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.wait(2)
        self.play(
            *self.right_channel.modify(420.69 * 8, 0.25, 0.5),
            run_time=3,
            rate_func=rate_functions.loglinear,
        )
        self.play(
            *self.right_channel.modify(420.69 / 4, 0.25, 0.5),
            run_time=2,
            rate_func=rate_functions.loglinear,
        )

    def interval(self):
        # Interval
        self.brace = always_redraw(
            lambda: BraceBetweenPoints(self.right, self.left, UP, buff=0).shift(
                UP * 0.01
            )
        )
        self.label_interval = Text("Interval").add_updater(
            lambda m: m.next_to(self.brace, UP)
        )
        self.play(*[FadeIn(self.brace), Write(self.label_interval)])
        self.play(
            *self.right_channel.modify(420.69 / 2, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.play(
            *self.right_channel.modify(420.69, 0.25, 0.5),
            run_time=5,
            rate_func=rate_functions.loglinear,
        )

    def consonant(self):
        # Consonant
        self.label_consonant = Text("Consonant", color=BLUE).shift(3 * UP)
        self.label_unison = Text(
            "1:1",
            font="monospace",
        ).next_to(self.brace, UP)
        self.label_unison[2].set_color(RED)
        self.play(
            Unwrite(self.label_interval, reverse=False),
            Write(self.label_unison),
            Write(self.label_consonant),
        )
        self.play(
            self.label_unison.animate.next_to(
                self.label_consonant, DOWN, aligned_edge=LEFT
            )
        )
        self.play(
            *self.right_channel.modify(420.69 * PYTH_PERFECT_FOURTH, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.label_fourth = Text("3:4", font="monospace", t2c={"4": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_fourth))
        self.play(
            self.label_fourth.animate.next_to(
                self.label_consonant, DOWN, aligned_edge=RIGHT
            )
        )
        self.wait(1)
        self.play(
            *self.right_channel.modify(420.69 * PYTH_PERFECT_FIFTH, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.smooth,
        )
        self.label_fifth = Text("2:3", font="monospace", t2c={"3": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_fifth))
        self.play(
            self.label_fifth.animate.next_to(self.label_unison, DOWN, aligned_edge=LEFT)
        )
        self.wait(1)
        self.play(
            *self.right_channel.modify(420.69 * PYTH_OCTAVE, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.smooth,
        )
        self.label_octave = Text("1:2", font="monospace", t2c={"2": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_octave))
        self.play(
            self.label_octave.animate.next_to(
                self.label_fourth, DOWN, aligned_edge=RIGHT
            )
        )
        self.wait(1)

        # Disonant

    def dissonant(self):
        self.label_dissonant = Text("Dissonant", color=RED).shift(DOWN)
        self.play(
            *self.right_channel.modify(420.69 * PYTH_MAJOR_SECOND, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.label_second = Text("8:9", font="monospace", t2c={"9": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_dissonant), Write(self.label_second))
        self.play(
            self.label_second.animate.next_to(self.label_dissonant.get_corner(DL), DOWN)
        )
        self.play(
            *self.right_channel.modify(420.69 * PYTH_MAJOR_THIRD, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.label_third = Text("64:81", font="monospace", t2c={"81": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_third))
        self.play(
            self.label_third.animate.next_to(self.label_dissonant.get_corner(DR), DOWN)
        )
        self.play(
            *self.right_channel.modify(420.69 * PYTH_MAJOR_SIXTH, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.label_sixth = Text("16:27", font="monospace", t2c={"27": RED}).next_to(
            self.brace, UP
        )
        self.play(Write(self.label_sixth))
        self.play(self.label_sixth.animate.next_to(self.label_second, DOWN))
        self.play(
            *self.right_channel.modify(420.69 * PYTH_MAJOR_SEVENTH, 0.25, 0.5),
            run_time=1,
            rate_func=rate_functions.loglinear,
        )
        self.label_seventh = Text(
            "128:243", font="monospace", t2c={"243": RED}
        ).next_to(self.brace, UP)
        self.play(Write(self.label_seventh))
        self.play(self.label_seventh.animate.next_to(self.label_third, DOWN))
        self.wait(1)

        self.play(
            *self.right_channel.modify(420.69 * 2, 0.25, 0.5),
            run_time=2,
            rate_func=rate_functions.loglinear,
        )

        self.play(
            Unwrite(self.brace),
            *self.left_channel.modify(420.69, 0.0, 0.5)
            + self.right_channel.modify(420.59 * 2, 0.0, 0.5),
            run_time=2,
            rate_func=rate_functions.loglinear,
        )

        self.wait()
        # self.play(FadeOut(self.x))


class Pythagoras(Scene):
    def construct(self):
        pythagoras = ImageMobject("Pythagoras.jpg").scale(2)
        name = Text(
            "Pythagoras",
            gradient=(BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE),
        )
        photo = Group(pythagoras, name).arrange(DOWN)

        theorem = MathTex(
            "a^2 + b^2 = c^2", tex_to_color_map={"a^2": BLUE, "b^2": RED, "c^2": GREEN}
        )
        tuning = MathTex("\\dfrac{3^x}{2^y}")
        accomplishments = Group(theorem, tuning).arrange(DOWN, aligned_edge=LEFT)
        ltr = Group(photo, accomplishments).arrange(RIGHT, buff=2, aligned_edge=UP)
        a = Square(3, fill_opacity=1, color=BLUE_A, stroke_color=BLUE_E)
        b = Square(4, fill_opacity=1, color=RED_A, stroke_color=RED_E).shift(
            (RIGHT + UP) * 3.5
        )
        c = (
            Square(5, fill_opacity=1, color=GREEN_A, stroke_color=GREEN_E)
            .rotate(0.93)
            .shift(UP * 5 + LEFT * 2)
        )
        ltr.to_edge(LEFT)
        g = Group(a, b, c).scale(0.5).center().to_edge(RIGHT)

        a2 = theorem[0].save_state()
        b2 = theorem[2].save_state()
        c2 = theorem[4].save_state()
        a2.move_to(a)
        b2.move_to(b)
        c2.move_to(c)

        self.play(FadeIn(photo))
        self.play(Write(a), Write(b), Write(c))
        self.play(Write(a2), Write(b2), Write(c2))
        self.play(
            a2.animate.restore(),
            FadeOut(a),
            FadeIn(theorem[1]),
            b2.animate.restore(),
            FadeOut(b),
            FadeIn(theorem[3]),
            c2.animate.restore(),
            FadeOut(c),
            lag_ratio=0.2,
            run_time=4,
        )
        pythagorean_theorem = Text(
            "Pythagorean theorem", gradient=(GREEN, RED, BLUE)
        ).move_to(theorem, aligned_edge=LEFT)
        pythagorean_tuning = Text("Pythagorean tuning", color=YELLOW).move_to(
            tuning, aligned_edge=LEFT
        )
        self.play(ReplacementTransform(theorem, pythagorean_theorem))
        tuning.save_state()
        tuning.center()
        self.play(Write(tuning))
        self.wait()
        self.play(
            ReplacementTransform(tuning, pythagorean_tuning),
            FadeOut(pythagorean_theorem),
        )
        self.play(FadeOut(photo), pythagorean_tuning.animate.center().to_edge(UP))
        self.wait()


class DiatonicDerivation(AudioScene):
    def nl(self):
        self.x_zoom = ValueTracker(0)
        self.x_down = ValueTracker(0)

        def construct_x():
            custom_ticks = [20, 200, 2000, 20000]
            x = NumberLine(
                x_range=[
                    1.301029 + self.x_zoom.get_value(),
                    4.301029 - self.x_zoom.get_value(),
                ],
                length=13,
                include_ticks=False,
                scaling=LogBase(10),
            )
            x.ticks = VGroup()
            for t in custom_ticks:
                x.ticks.add(x.get_tick(t))
            x.add(x.get_tick_marks())
            x.add_labels(
                dict(
                    zip(custom_ticks, custom_ticks),
                )
            )
            return x.shift(DOWN * self.x_down.get_value())

        self.x = always_redraw(lambda: construct_x())

    def consonant(self):
        self.label_consonant = Text("Consonant", color=BLUE).shift(3 * UP)
        self.label_unison = Text(
            "1:1",
            font="monospace",
        ).next_to(self.label_consonant, DOWN, aligned_edge=LEFT)
        self.label_unison[2].set_color(RED)
        self.label_fourth = Text("3:4", font="monospace", t2c={"4": RED}).next_to(
            self.label_consonant, DOWN, aligned_edge=RIGHT
        )
        self.label_fifth = Text("2:3", font="monospace", t2c={"3": RED}).next_to(
            self.label_unison, DOWN, aligned_edge=LEFT
        )
        self.label_octave = Text("1:2", font="monospace", t2c={"2": RED}).next_to(
            self.label_fourth, DOWN, aligned_edge=RIGHT
        )

    def dissonant(self):
        self.label_dissonant = Text("Dissonant", color=RED).shift(DOWN)
        self.label_M2 = Text("8:9", font="monospace", t2c={"9": RED}).next_to(
            self.label_dissonant.get_corner(DL), DOWN
        )
        self.label_M3 = Text("64:81", font="monospace", t2c={"81": RED}).next_to(
            self.label_dissonant.get_corner(DR), DOWN
        )
        self.label_M6 = Text("16:27", font="monospace", t2c={"27": RED}).next_to(
            self.label_M2, DOWN
        )
        self.label_M7 = Text("128:243", font="monospace", t2c={"243": RED}).next_to(
            self.label_M3, DOWN
        )

    def construct(self):
        pythagorean_tuning = Text("Pythagorean tuning", color=YELLOW).to_edge(UP)
        self.add(pythagorean_tuning)
        self.play(FadeOut(pythagorean_tuning))
        self.nl()
        self.consonant()
        self.dissonant()
        self.play(
            *[
                FadeIn(x)
                for x in [
                    self.x,
                    self.label_consonant,
                    self.label_unison,
                    self.label_fourth,
                    self.label_fifth,
                    self.label_octave,
                    self.label_dissonant,
                    self.label_M2,
                    self.label_M3,
                    self.label_M6,
                    self.label_M7,
                ]
            ],
            lag_ratio=0.3,
        )
        root = 420.69
        self.wait()

        label_consonant = Text("Consonant", color=BLUE).shift(2.5 * UP + 2 * LEFT)
        label_unison = Text(
            "1:1",
            font="monospace",
        ).next_to(label_consonant, DOWN, aligned_edge=LEFT)
        label_unison[2].set_color(RED)
        label_unison.next_to(label_consonant, DOWN, aligned_edge=LEFT)
        label_fourth = Text("3:4", font="monospace", t2c={"4": RED}).next_to(
            label_unison, DOWN, aligned_edge=LEFT
        )
        label_fifth = Text("2:3", font="monospace", t2c={"3": RED}).next_to(
            label_fourth, DOWN, aligned_edge=LEFT
        )
        label_octave = Text("1:2", font="monospace", t2c={"2": RED}).next_to(
            label_fifth, DOWN, aligned_edge=LEFT
        )

        label_dissonant = Text("Dissonant", color=RED).shift(2.5 * UP + 2 * RIGHT)
        label_M2 = Text("8:9", font="monospace", t2c={"9": RED}).next_to(
            label_dissonant, DOWN, aligned_edge=LEFT
        )
        label_M3 = Text("64:81", font="monospace", t2c={"81": RED}).next_to(
            label_M2, DOWN, aligned_edge=LEFT
        )
        label_M6 = Text("16:27", font="monospace", t2c={"27": RED}).next_to(
            label_M3, DOWN, aligned_edge=LEFT
        )
        label_M7 = Text("128:243", font="monospace", t2c={"243": RED}).next_to(
            label_M6, DOWN, aligned_edge=LEFT
        )
        self.play(
            Transform(self.label_consonant, label_consonant),
            Transform(self.label_unison, label_unison),
            Transform(self.label_fourth, label_fourth),
            Transform(self.label_fifth, label_fifth),
            Transform(self.label_octave, label_octave),
            Transform(self.label_dissonant, label_dissonant),
            Transform(self.label_M2, label_M2),
            Transform(self.label_M3, label_M3),
            Transform(self.label_M6, label_M6),
            Transform(self.label_M7, label_M7),
            self.x_down.animate.set_value(2),
        )

        consonant = VGroup(
            self.label_unison, self.label_fourth, self.label_fifth, self.label_octave
        )
        major_dissonant = VGroup(
            self.label_M2, self.label_M3, self.label_M6, self.label_M7
        )

        intervals = VGroup(
            self.label_unison,
            self.label_M2,
            self.label_M3,
            self.label_fourth,
            self.label_fifth,
            self.label_M6,
            self.label_M7,
            self.label_octave,
        )

        def construct_nl():
            custom_ticks = [20, 200, 2000, 20000]
            x = NumberLine(
                x_range=[
                    1.301029 + self.x_zoom.get_value(),
                    4.301029 - self.x_zoom.get_value(),
                ],
                length=13,
                include_ticks=False,
                scaling=LogBase(10),
            )
            x.ticks = VGroup()
            for t in custom_ticks:
                x.ticks.add(x.get_tick(t))
            x.add(x.get_tick_marks())
            x.add_labels(
                dict(
                    zip(custom_ticks, custom_ticks),
                )
            )
            return x.shift(DOWN * self.x_down.get_value())

        dot_P1 = always_redraw(lambda: Dot(construct_nl().n2p(root), color=BLUE))
        dot_P8 = always_redraw(lambda: Dot(construct_nl().n2p(root * 2), color=BLUE))

        def replace_intervals(intervals: list, names: list, colors):
            anims = []
            pairings = zip(intervals, names, colors)
            for i, n, c in pairings:
                anims.append(
                    Transform(i, Text(f"{n}", color=c).move_to(i, aligned_edge=LEFT))
                )
            return anims

        names = [
            "Unison",
            "Major 2nd",
            "Major 3rd",
            "Perfect 4th",
            "Perfect 5th",
            "Major 6th",
            "Major 7th",
            "Octave",
        ]
        colors = [BLUE, RED, RED, BLUE, BLUE, RED, RED, BLUE]
        replacements = replace_intervals(intervals, names, colors)
        self.play(FadeIn(dot_P1), replacements[0])

        self.play(FadeIn(dot_P8), replacements[-1])

        # ZOOOOOOOOOOOOOM
        self.play(self.x_zoom.animate.set_value(1))
        self.x = construct_nl()

        brace_octave = BraceBetweenPoints(
            self.x.n2p(root), self.x.n2p(2 * root), DOWN, buff=0.75
        )
        brace_fifth = BraceBetweenPoints(self.x.n2p(root), self.x.n2p(root * 3 / 2), UP)

        timesfifth = (
            MathTex("\\times \\dfrac{3}{2}")
            .scale(0.5)
            .add_updater(lambda m: m.next_to(brace_fifth, UP))
        )
        timesoctave = (
            MathTex("\\times 2")
            .scale(0.5)
            .add_updater(lambda m: m.next_to(brace_octave, DOWN))
        )

        self.play(
            Write(brace_octave),
            Write(timesoctave),
        )

        dot_P5 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * 3 / 2), color=BLUE)
        )
        tick_P5 = (
            MathTex("\\dfrac{3}{2}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_P5, DOWN))
        )
        self.play(
            replacements[4],
            TransformFromCopy(self.label_fifth, dot_P5),
            Write(timesfifth),
            Write(brace_fifth),
            Write(tick_P5),
        )
        self.play(
            brace_fifth.animate.align_to(self.x.n2p(root * 2), RIGHT),
            Transform(
                timesfifth,
                MathTex("\\div \\dfrac{3}{2}")
                .scale(0.5)
                .add_updater(lambda m: m.next_to(brace_fifth, UP)),
            ),
        )

        dot_P4 = always_redraw(lambda: Dot(self.x.n2p(root * 4 / 3), color=BLUE))
        tick_P4 = (
            MathTex("\\dfrac{4}{3}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_P4, DOWN))
        )
        self.play(
            replacements[3],
            TransformFromCopy(self.label_fourth, dot_P4),
            Write(tick_P4),
        )
        tick_9_4 = (
            MathTex("\\dfrac{9}{4}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(self.x.n2p(root * 9 / 4), DOWN))
        )
        self.play(
            Transform(
                timesfifth,
                MathTex("\\times \\dfrac{3}{2}")
                .scale(0.5)
                .add_updater(lambda m: m.next_to(brace_fifth, UP)),
            ),
            brace_fifth.animate.align_to(self.x.n2p(root * 9 / 4), RIGHT),
            Write(tick_9_4),
        )
        self.play(
            Transform(
                timesoctave,
                MathTex("\\div 2")
                .scale(0.5)
                .add_updater(lambda m: m.next_to(brace_octave, DOWN)),
            ),
            brace_octave.animate.align_to(self.x.n2p(root * 9 / 4), RIGHT),
        )

        # Dissonant
        dot_M2 = Dot(self.x.n2p(root * 9 / 8), color=RED)
        tick_M2 = (
            MathTex("\\dfrac{9}{8}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_M2, DOWN))
        )
        dot_M3 = Dot(self.x.n2p(root * 81 / 64), color=RED)
        tick_M3 = (
            MathTex("\\dfrac{81}{64}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_M3, DOWN))
        )
        dot_M6 = Dot(self.x.n2p(root * 27 / 16), color=RED)
        tick_M6 = (
            MathTex("\\dfrac{27}{16}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_M6, DOWN))
        )
        dot_M7 = Dot(self.x.n2p(root * 243 / 128), color=RED)
        tick_M7 = (
            MathTex("\\dfrac{243}{128}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_M7, DOWN))
        )
        dot_A4 = Dot(self.x.n2p(root * PYTH_AUGMENTED_FOURTH), color=RED)
        tick_A4 = (
            MathTex("\\dfrac{729}{512}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(dot_A4, DOWN))
        )
        tick_721256 = (
            MathTex("\\dfrac{729}{256}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(self.x.n2p(root * 729 / 256), DOWN))
        )

        label81_32 = (
            MathTex("\\dfrac{81}{32}")
            .scale(0.333)
            .add_updater(lambda m: m.next_to(self.x.n2p(root * 81 / 32), DOWN))
        )
        self.play(
            TransformFromCopy(self.label_M2, dot_M2),
            Write(tick_M2),
            replacements[1],
        )
        self.play(
            brace_fifth.animate.align_to(self.x.n2p(root * 27 / 16), RIGHT),
            brace_octave.animate.align_to(self.x.n2p(root * 27 / 16), RIGHT),
        )
        self.play(
            TransformFromCopy(self.label_M6, dot_M6),
            Write(tick_M6),
            replacements[5],
        )
        self.play(
            brace_fifth.animate.align_to(self.x.n2p(root * 81 / 32), RIGHT),
            Write(label81_32),
            brace_octave.animate.align_to(self.x.n2p(root * 81 / 32), RIGHT),
        )

        self.play(
            replacements[2],
            TransformFromCopy(self.label_M3, dot_M3),
            Write(tick_M3),
        )
        self.play(
            brace_fifth.animate.align_to(self.x.n2p(root * 243 / 128), RIGHT),
            brace_octave.animate.align_to(self.x.n2p(root * 243 / 128), RIGHT),
        )
        self.play(
            Write(tick_M7),
            TransformFromCopy(self.label_M7, dot_M7),
            replacements[6],
        )
        self.play(
            brace_fifth.animate.set_opacity(0),
            brace_octave.animate.set_opacity(0),
            timesfifth.animate.set_opacity(0),
            timesoctave.animate.set_opacity(0),
        )

        # Audio segment - Pythagorean major scale
        left_audio = AudioGenerator(420.69, 0.0, 0.0)
        right_audio = AudioGenerator(420.69, 0.0, 1.0)
        self.add_audio_generator(left_audio)
        self.add_audio_generator(right_audio)
        right_arrow = Vector(DOWN, color=RED).add_updater(
            lambda m: m.next_to(self.x.n2p(right_audio.freq_t.get_value()), UP)
        )
        left_arrow = Vector(DOWN).add_updater(
            lambda m: m.next_to(self.x.n2p(left_audio.freq_t.get_value()), UP)
        )

        self.play(
            Write(right_arrow),
            *left_audio.modify(root, 0.25),
            *right_audio.modify(root, 0.25),
            FadeIn(left_arrow),
        )
        for interval in PYTHAGOREAN_MAJOR_SCALE:
            self.play(*right_audio.modify(root * interval, 0.25), run_time=0.1)
            self.wait(0.5)

        self.play(
            *right_audio.modify(vol=0),
            *left_audio.modify(vol=0),
            left_arrow.animate.set_opacity(0),
            right_arrow.animate.set_opacity(0),
        )

        # Augmented 4th
        self.play(
            brace_fifth.animate.set_opacity(1),
            brace_octave.animate.set_opacity(1),
            timesfifth.animate.set_opacity(1),
            timesoctave.animate.set_opacity(1),
        )
        self.play(
            brace_fifth.animate.align_to(
                self.x.n2p(root * PYTH_AUGMENTED_FOURTH * 2), RIGHT
            ),
            Write(tick_721256),
            brace_octave.animate.align_to(
                self.x.n2p(root * PYTH_AUGMENTED_FOURTH * 2), RIGHT
            ),
        )

        major_dissonant.generate_target()
        distance = self.label_M3.get_center() - self.label_M2.get_center()
        major_dissonant.target[2].shift(distance)
        major_dissonant.target[3].shift(distance)
        major_dissonant.target.to_corner(UR)

        self.label_A4 = Text("Augmented 4th", color=YELLOW)
        self.play(
            self.label_consonant.animate.shift(UP * 5),
            self.label_dissonant.animate.shift(UP * 5),
            consonant.animate.to_corner(UL),
            MoveToTarget(major_dissonant),
            Write(self.label_A4),
        )
        dot_A4 = Dot(self.x.n2p(root * PYTH_AUGMENTED_FOURTH), color=YELLOW)
        self.play(TransformFromCopy(self.label_A4, dot_A4), Write(tick_A4))

        self.play(Transform(self.label_A4, Text("Aug 4th", color=YELLOW)))
        self.play(
            self.label_A4.animate.move_to(self.label_M3)
            .align_to(self.label_M3, LEFT)
            .shift(distance),
            brace_fifth.animate.set_opacity(0),
            brace_octave.animate.set_opacity(0),
            timesfifth.animate.set_opacity(0),
            timesoctave.animate.set_opacity(0),
        )

        intervals += self.label_A4
        # Minor intervals
        self.label_m2 = Text("Minor 2nd", color=ORANGE).align_to(self.label_M2, UP)
        self.label_m3 = Text("Minor 3rd", color=ORANGE).align_to(self.label_M3, UP)
        self.label_m6 = Text("Minor 6th", color=ORANGE).align_to(self.label_M6, UP)
        self.label_m7 = Text("Minor 7th", color=ORANGE).align_to(self.label_M7, UP)
        self.label_d5 = Text("Diminished 5th", color=ORANGE).align_to(self.label_A4, UP)
        minor_dissonant = VGroup(
            self.label_m2, self.label_m3, self.label_d5, self.label_m6, self.label_m7
        )
        self.play(intervals.animate.set_opacity(0.5))

        major_scale_dots = VGroup(
            dot_P1, dot_M2, dot_M3, dot_P4, dot_A4, dot_P5, dot_M6, dot_M7, dot_P8
        ).copy()

        self.play(major_scale_dots.animate.shift(UP * 2))
        self.play(Rotate(major_scale_dots, about_point=major_scale_dots.get_center()))
        self.play(intervals.animate.set_opacity(1))
        self.play(*[Flash(major_scale_dots[x]) for x in [0, 3, 5, 8]])
        self.play(
            *[Flash(major_scale_dots[x]) for x in [1, 2, 4, 6, 7]]
            + [major_scale_dots[x].animate.set_color(ORANGE) for x in [1, 2, 4, 6, 7]]
        )
        self.play(
            major_scale_dots.animate.shift(DOWN * 2),
            FadeIn(minor_dissonant),
        )
        self.x = construct_nl()
        dot_m2 = Dot(self.x.n2p(PYTH_MINOR_SECOND), color=ORANGE).add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_MINOR_SECOND))
        )
        dot_m3 = Dot(self.x.n2p(PYTH_MINOR_THIRD), color=ORANGE).add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_MINOR_THIRD))
        )
        dot_m6 = Dot(self.x.n2p(PYTH_MINOR_SIXTH), color=ORANGE).add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_MINOR_SIXTH))
        )
        dot_m7 = Dot(self.x.n2p(PYTH_MINOR_SEVENTH), color=ORANGE).add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_MINOR_SEVENTH))
        )
        dot_d5 = Dot(self.x.n2p(PYTH_DIMINISHED_FIFTH), color=ORANGE).add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_DIMINISHED_FIFTH))
        )
        self.add(dot_m2, dot_m3, dot_m6, dot_m7, dot_d5)
        self.remove(major_scale_dots)
        # Add updaters

        dot_M2.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_MAJOR_SECOND)))
        dot_M3.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_MAJOR_THIRD)))
        dot_M6.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_MAJOR_SIXTH)))
        dot_M7.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_MAJOR_SEVENTH)))
        dot_A4.add_updater(
            lambda m: m.move_to(self.x.n2p(root * PYTH_AUGMENTED_FOURTH))
        )
        dot_P1.add_updater(lambda m: m.move_to(self.x.n2p(root * 1)))
        dot_P8.add_updater(lambda m: m.move_to(self.x.n2p(root * 2)))
        dot_P4.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_PERFECT_FOURTH)))
        dot_P5.add_updater(lambda m: m.move_to(self.x.n2p(root * PYTH_PERFECT_FIFTH)))

        # self.play(self.x.animate.scale(3))

        sruti = [
            1,
            256 / 243,
            16 / 15,
            10 / 9,
            9 / 8,
            32 / 27,
            6 / 5,
            5 / 4,
            81 / 64,
            4 / 3,
            27 / 20,
            45 / 32,
            729 / 512,
            3 / 2,
            128 / 81,
            8 / 5,
            5 / 3,
            27 / 16,
            16 / 9,
            9 / 5,
            15 / 8,
            243 / 128,
            2,
        ]

        sruti_scale = VGroup(
            *[Dot(color=WHITE).next_to(self.x.n2p(root * x), UP * 0.5) for x in sruti]
        )
        self.play(FadeIn(sruti_scale, lag_ratio=0.3))
        self.wait()
        self.play(FadeOut(sruti_scale, lag_ratio=0.3))
        TET_12 = [2 ** (x / 12) for x in range(13)]
        TET_scale = VGroup(
            *[Dot(color=GREEN).next_to(self.x.n2p(root * x), UP * 0.5) for x in TET_12]
        )
        self.play(FadeIn(TET_scale, lag_ratio=0.3))

        self.play(*left_audio.modify(420.69, 0, 0) + right_audio.modify(420.69, 0, 1))
        self.play(
            *left_audio.modify(420.69, 0.25, 0) + right_audio.modify(420.69, 0.25, 1),
            left_arrow.animate.set_opacity(1),
            right_arrow.animate.set_opacity(1),
        )
        for left, right in zip(TET_12[1:], PYTHAGOREAN_CHROMATIC_SCALE):
            self.play(
                *left_audio.modify(root * left) + right_audio.modify(root * right),
                run_time=0.1,
            )
            self.wait(0.5)
        self.play(
            *left_audio.modify(root * 2, 0, 0) + right_audio.modify(root * 2, 0, 1),
            left_arrow.animate.set_opacity(0),
            right_arrow.animate.set_opacity(0),
        )

        self.wait()


class Questions(MusicScene):
    def construct(self):
        q1 = self.students[0].get_bubble("What makes consonance?")
        self.teacher.change_mode("pondering")
        self.change_student_modes(
            *["puzzled", "pondering", "pondering", "pondering", "pondering"],
            look_at_arg=q1.content.get_left(),
            lag_ratio=0.04,
            added_anims=[Write(q1)],
        )
        self.joint_blink()
        q2 = self.students[1].get_bubble("What intervals are best?")
        q3 = self.students[3].get_bubble("What scales exist?")
        self.play(
            q1.animate.set_opacity(0),
            q1.content.animate.set_opacity(1).center().to_edge(UP),
        )
        self.change_student_modes(
            *["puzzled", "puzzled", "pondering", "pondering", "pondering"],
            look_at_arg=q1.content.get_left(),
            lag_ratio=0.04,
            added_anims=[Write(q2)],
        )
        self.play(
            q2.animate.set_opacity(0),
            q2.content.animate.next_to(q1.content, DOWN)
            .align_to(q1.content, LEFT)
            .set_opacity(1),
            self.teacher.animate.change_mode("happy"),
        )
        self.change_student_modes(
            *["puzzled", "puzzled", "puzzled", "pondering", "pondering"],
            look_at_arg=q1.content.get_left(),
            lag_ratio=0.04,
            added_anims=[Write(q3)],
        )
        self.joint_blink()
        self.play(
            q3.animate.set_opacity(0),
            q3.content.animate.next_to(q2.content, DOWN)
            .align_to(q2.content, LEFT)
            .set_opacity(1),
            self.teacher.animate.change_mode("giddy"),
        )
        self.joint_blink()
        self.wait()


class Superposition(Scene):
    def construct(self):
        self.wave_time = ValueTracker(0)
        self.speed1 = PI / 5
        self.speed2 = -PI / 5
        self.x_start = -1.5 * PI
        self.x_end = 5 * PI
        self.arrow_left = ValueTracker(PI)
        self.arrow_right = ValueTracker(PI)
        self.func1_color = BLUE_E
        self.func2_color = RED
        self.func3_color = PURPLE
        self.func4_color = ORANGE

        self.show_properties()
        self.setup_axes()
        self.demonstration()
        self.wait()

    def show_properties(self):
        self.superposition = Text("Superposition Principle", color=YELLOW).to_edge(UP)
        self.additivity = MathTex(
            "F(x_1 + x_2) = F(x_1) + F(x_2)",
            tex_to_color_map={
                "F(x_1 + x_2)": self.func3_color,
                "F(x_1)": self.func1_color,
                "F(x_2)": self.func2_color,
            },
        ).next_to(self.superposition, DOWN)
        self.homogeneity = MathTex(
            "F(cx_1 + cx_2) = cF(x_1 + x_2)",
            tex_to_color_map={
                "c": YELLOW,
                "F(cx_1 + cx_2)": self.func4_color,
                "F(x_1 + x_2)": self.func3_color,
            },
        ).next_to(self.additivity, DOWN)
        self.play(Write(self.superposition))
        self.play(Write(self.additivity))

    def demonstration(self):
        self.opac1 = ValueTracker(1)
        self.opac2 = ValueTracker(1)
        self.opac3 = ValueTracker(1)
        self.opac4 = ValueTracker(0)
        self.opac5 = ValueTracker(0)
        start_amp = 0.75
        self.amp2 = ValueTracker(start_amp)

        def func1(x):
            return np.sin(x - PI / 2 - self.wave_time.get_value() * self.speed1)

        def func2(x):
            return start_amp * np.sin(
                PI / 4 + 3 / 2 * x - self.wave_time.get_value() * self.speed2
            )

        def func3(x):
            return func2(x) + func1(x)

        sin_wave1 = always_redraw(
            lambda: self.axes.plot(
                lambda x: func1(x),
                [self.x_start, self.x_end],
                color=self.func1_color,
                stroke_opacity=self.opac1.get_value(),
            )
        )
        sin_wave2 = always_redraw(
            lambda: self.axes.plot(
                lambda x: func2(x),
                [self.x_start, self.x_end],
                color=self.func2_color,
                stroke_opacity=self.opac2.get_value(),
            )
        )

        tip_to_tail = ValueTracker(0)
        arrow_left = always_redraw(
            lambda: Arrow(
                self.axes.c2p(self.arrow_left.get_value(), 0, 0),
                self.axes.c2p(
                    self.arrow_left.get_value(),
                    self.axes.p2c(
                        sin_wave1.get_point_from_function(self.arrow_left.get_value())
                    )[1],
                    0,
                ),
                buff=0,
                color=self.func1_color,
                fill_opacity=self.opac1.get_value(),
            )
        )
        arrow_right = always_redraw(
            lambda: Arrow(
                self.axes.c2p(
                    self.arrow_right.get_value(),
                    tip_to_tail.get_value()
                    * self.axes.p2c(
                        sin_wave2.get_point_from_function(self.arrow_right.get_value())
                    )[1],
                    0,
                ),
                self.axes.c2p(
                    self.arrow_right.get_value(),
                    tip_to_tail.get_value()
                    * self.axes.p2c(
                        sin_wave2.get_point_from_function(self.arrow_right.get_value())
                    )[1]
                    + self.axes.p2c(
                        sin_wave1.get_point_from_function(self.arrow_right.get_value())
                    )[1],
                    0,
                ),
                buff=0,
                color=self.func1_color,
                fill_opacity=self.opac1.get_value(),
            )
        )
        arrow2_left = always_redraw(
            lambda: Arrow(
                self.axes.c2p(
                    self.arrow_left.get_value(),
                    tip_to_tail.get_value()
                    * self.axes.p2c(
                        sin_wave1.get_point_from_function(self.arrow_left.get_value())
                    )[1],
                    0,
                ),
                self.axes.c2p(
                    self.arrow_left.get_value(),
                    tip_to_tail.get_value()
                    * self.axes.p2c(
                        sin_wave1.get_point_from_function(self.arrow_left.get_value())
                    )[1]
                    + self.axes.p2c(
                        sin_wave2.get_point_from_function(self.arrow_left.get_value())
                    )[1],
                    0,
                ),
                buff=0,
                color=self.func2_color,
                fill_opacity=self.opac1.get_value(),
            )
        )
        arrow2_right = always_redraw(
            lambda: Arrow(
                self.axes.c2p(
                    self.arrow_right.get_value(),
                    0,
                    0,
                ),
                self.axes.c2p(
                    self.arrow_right.get_value(),
                    self.axes.p2c(
                        sin_wave2.get_point_from_function(self.arrow_right.get_value())
                    )[1],
                    0,
                ),
                buff=0,
                color=self.func2_color,
                fill_opacity=self.opac1.get_value(),
            )
        )
        self.play(Write(sin_wave1))
        self.play(FadeIn(arrow_left), FadeIn(arrow_right))
        self.play(Write(sin_wave2))
        self.play(FadeIn(arrow2_left), FadeIn(arrow2_right))
        self.play(
            tip_to_tail.animate.set_value(1),
            self.opac1.animate.set_value(0.175),
            self.opac2.animate.set_value(0.175),
            run_time=2,
        )

        sin_wave3 = always_redraw(
            lambda: self.axes.plot(
                lambda x: func3(x),
                [self.arrow_left.get_value(), self.arrow_right.get_value()],
                color=self.func3_color,
                stroke_opacity=self.opac3.get_value(),
            )
        )
        self.add(sin_wave3)
        self.play(
            self.arrow_left.animate.set_value(-PI),
            self.arrow_right.animate.set_value(4 * PI),
            run_time=5,
        )
        self.play(self.wave_time.animate.set_value(4), run_time=4, rate_func=linear)
        sin_wave2_copy = always_redraw(
            lambda: self.axes.plot(
                lambda x: self.amp2.get_value() * func3(x),
                [self.x_start, self.x_end],
                color=self.func4_color,
                stroke_opacity=self.opac4.get_value(),
            )
        )
        c = always_redraw(
            lambda: Text(
                f"c={self.amp2.get_value():.2f}", font="monospace", color=YELLOW
            )
            .next_to(self.homogeneity, RIGHT, buff=MED_LARGE_BUFF)
            .set_opacity(self.opac5.get_value())
        )
        self.add(sin_wave2_copy, c)
        self.play(
            self.wave_time.animate(rate_func=linear).set_value(5),
            self.opac3.animate.set_value(0.8),
            self.opac4.animate.set_value(0.8),
            self.opac5.animate.set_value(1),
            Write(self.homogeneity),
            run_time=1,
        )

        self.play(
            self.amp2.animate(rate_func=there_and_back).set_value(2),
            self.wave_time.animate(rate_func=linear).set_value(10),
            run_time=5,
        )
        self.play(
            self.amp2.animate(rate_func=smooth).set_value(-1),
            self.wave_time.animate(rate_func=linear).set_value(15),
            run_time=5,
        )
        self.play(
            self.wave_time.animate(rate_func=linear).set_value(20),
            run_time=5,
        )

    def setup_axes(self):
        self.axes = Axes(
            x_range=[-1.5 * PI, 4.5 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=14,
            y_length=2.97,
            tips=False,
        ).shift(DOWN)
        self.axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )
        self.play(FadeIn(self.axes), lag_ratio=0.1)


class TriangleWave(AudioScene):
    def construct(self):
        self.setup_axes()
        self.demonstration()
        self.wait(2)

    def demonstration(self):
        gens: list[AudioGenerator] = [
            AudioGenerator(210.345 * i, 0.000001, 0.5) for i in range(1, 2 * 5, 2)
        ]
        c = [PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        def add_dot(gen):
            return always_redraw(
                lambda: Dot(
                    self.axes.c2p(gen.freq_t.get_value(), gen.vol_t.get_value())
                )
            )

        dots = [add_dot(gen) for gen in gens]
        self.add(*dots)

        start = -TAU
        end = TAU

        def func(x, freq_t: ValueTracker):
            return np.sin(freq_t.get_value() * TAU * x)

        total_wave = always_redraw(
            lambda: self.hidden_axes.plot(
                lambda x: reduce(
                    lambda a, b: a(x) if type(a) != np.float64 else a + b,
                    [gen.vol_t.get_value() * func(x, gen.freq_t) for gen in gens],
                ),
                [start, end],
                color=WHITE,
            )
        )

        def add_wave(idx, gen):
            return always_redraw(
                lambda: self.hidden_axes.plot(
                    lambda x: gen.vol_t.get_value() * func(x, gen.freq_t),
                    [start, end],
                    color=c[idx % len(c)],
                    stroke_opacity=0.25,
                )
            )

        waves = [add_wave(i, gen) for i, gen in enumerate(gens)]

        self.add(*waves)
        self.add(total_wave)
        for gen in gens:
            self.add_audio_generator(gen)
        for i in range(len(gens)):
            self.play(*gens[i].modify(vol=0.5 * (-1) ** i / (2 * i + 1) ** 2))

    def setup_axes(self):
        self.axes = Axes(
            x_range=[1.301029, 4.301029],
            x_length=12,
            y_range=[-1, 1, 1],
            tips=False,
            x_axis_config={"scaling": LogBase(10), "include_ticks": False},
            y_axis_config={"include_numbers": True},
        )
        custom_ticks = [20, 200, 2000, 20000]
        x = self.axes.x_axis
        x.ticks = VGroup()
        for t in custom_ticks:
            x.ticks.add(x.get_tick(t))
        self.axes.x_axis.add(self.axes.x_axis.get_tick_marks())
        self.axes.x_axis.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.add(self.axes)
        self.hidden_axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1, 1, 0.5],
            x_length=12,
            y_length=5,
            tips=False,
        )
        self.hidden_axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )


class SawtoothWave(AudioScene):
    def construct(self):
        self.setup_axes()
        self.demonstration()
        self.wait(5)

    def demonstration(self):
        gens: list[AudioGenerator] = [
            AudioGenerator(210.345 * i, 0.000001, 0.5) for i in range(1, 95)
        ]
        c = [PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        def add_dot(gen):
            return always_redraw(
                lambda: Dot(
                    self.axes.c2p(gen.freq_t.get_value(), gen.vol_t.get_value())
                )
            )

        dots = [add_dot(gen) for gen in gens]
        self.add(*dots)

        start = -TAU
        end = TAU

        def func(x, freq_t):
            return np.sin(freq_t.get_value() * TAU * x)

        total_wave = always_redraw(
            lambda: self.hidden_axes.plot(
                lambda x: reduce(
                    lambda a, b: a(x) if type(a) != np.float64 else a + b,
                    [gen.vol_t.get_value() * func(x, gen.freq_t) for gen in gens],
                ),
                [start, end],
                color=WHITE,
            )
        )

        def add_wave(idx, gen):
            return always_redraw(
                lambda: self.hidden_axes.plot(
                    lambda x: gen.vol_t.get_value() * func(x, gen.freq_t),
                    [start, end],
                    color=c[idx % len(c)],
                    stroke_opacity=0.25,
                )
            )

        waves = [add_wave(i, gen) for i, gen in enumerate(gens)]

        self.add(*waves)
        self.add(total_wave)
        for gen in gens:
            self.add_audio_generator(gen)
        for i in range(len(gens)):
            self.play(
                *gens[i].modify(vol=0.25 * (-1) ** (i + 1) / (i + 1)), run_time=0.1
            )

        # for i in range(len(gens)):
        #     total_anims += gens[i].modify(vol=.25* (-1)**(i+1) / (i + 1))
        # self.play(
        #     *total_anims
        # )

    def setup_axes(self):
        self.axes = Axes(
            x_range=[1.301029, 4.301029],
            x_length=12,
            y_range=[-1, 1, 1],
            tips=False,
            x_axis_config={"scaling": LogBase(10), "include_ticks": False},
            y_axis_config={"include_numbers": True},
        )
        custom_ticks = [20, 200, 2000, 20000]
        x = self.axes.x_axis
        x.ticks = VGroup()
        for t in custom_ticks:
            x.ticks.add(x.get_tick(t))
        self.axes.x_axis.add(self.axes.x_axis.get_tick_marks())
        self.axes.x_axis.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.add(self.axes)
        self.hidden_axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1, 1, 0.5],
            x_length=12,
            y_length=5,
            tips=False,
        )
        self.hidden_axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )


class SquareWave(AudioScene):
    def construct(self):
        self.setup_axes()
        self.demonstration()
        self.wait(5)

    def demonstration(self):
        gens: list[AudioGenerator] = [
            AudioGenerator(210.345 * i, 0.000001, 0.5) for i in range(1, 16, 2)
        ]
        c = [PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        def add_dot(gen):
            return always_redraw(
                lambda: Dot(
                    self.axes.c2p(gen.freq_t.get_value(), gen.vol_t.get_value())
                )
            )

        dots = [add_dot(gen) for gen in gens]
        self.add(*dots)

        start = -TAU
        end = TAU

        def func(x, i):
            return np.sin(gens[i].freq_t.get_value() * TAU * x)

        total_wave = always_redraw(
            lambda: self.hidden_axes.plot(
                lambda x: reduce(
                    lambda a, b: a(x) if type(a) != np.float64 else a + b,
                    [
                        gens[idx].vol_t.get_value() * func(x, idx)
                        for idx in range(len(gens))
                    ],
                ),
                [start, end, 0.1],
                color=WHITE,
            )
        )

        def add_wave(idx, gen):
            return always_redraw(
                lambda: self.hidden_axes.plot(
                    lambda x: gen.vol_t.get_value() * func(x, idx),
                    [start, end],
                    color=c[idx % len(c)],
                    stroke_opacity=0.25,
                )
            )

        waves = [add_wave(i, gen) for i, gen in enumerate(gens)]

        self.add(*waves)
        self.add(total_wave)
        for gen in gens:
            self.add_audio_generator(gen)
        for i in range(len(gens)):
            self.play(*gens[i].modify(vol=0.25 * 1 / (2 * i + 1)), run_time=1)

        # for i in range(len(gens)):
        #     total_anims += gens[i].modify(vol=.25* (-1)**(i+1) / (i + 1))
        # self.play(
        #     *total_anims
        # )

    def setup_axes(self):
        self.axes = Axes(
            x_range=[1.301029, 4.301029],
            x_length=12,
            y_range=[-1, 1, 1],
            tips=False,
            x_axis_config={"scaling": LogBase(10), "include_ticks": False},
            y_axis_config={"include_numbers": True},
        )
        custom_ticks = [20, 200, 2000, 20000]
        x = self.axes.x_axis
        x.ticks = VGroup()
        for t in custom_ticks:
            x.ticks.add(x.get_tick(t))
        self.axes.x_axis.add(self.axes.x_axis.get_tick_marks())
        self.axes.x_axis.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.add(self.axes)
        self.hidden_axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1, 1, 0.5],
            x_length=12,
            y_length=5,
            tips=False,
        )
        self.hidden_axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )


class String(Scene):
    def construct(self):
        self.equation()
        self.setup_axes()
        self.show_harmonics()
        # self.wait()

    def equation(self):
        f = MathTex(
            "f_n", "\\approx", "\\dfrac{n}{2L}", "\\sqrt{\dfrac{T}{\mu}}"
        ).to_edge(UP)
        length = Text("Length")
        tension = Text("Tension")
        mass = Text("Mass")
        vg1 = VGroup(length, tension, mass).arrange(RIGHT, buff=1).shift(UP)
        L = MathTex("f", "\\propto", r"\dfrac{1}{L}").next_to(length, DOWN)
        T = (
            MathTex("f", "\\propto", "\\sqrt{T}")
            .next_to(tension, DOWN)
            .shift(0.3 * DOWN)
        )
        M = (
            MathTex("f", "\\propto", "\\sqrt{\dfrac{1}{\mu}}")
            .next_to(mass, DOWN)
            .shift(0.05 * DOWN)
        )
        vg2 = VGroup(L, T, M)
        self.add(vg1, vg2)
        self.play(Write(vg1), Write(vg2), lag_ratio=0.5)
        self.wait()
        self.play(
            Unwrite(L[1]),
            Unwrite(T[1]),
            Unwrite(M[1]),
            Unwrite(length),
            Unwrite(tension),
            Unwrite(mass),
            Transform(L[0], f[0]),
            Transform(T[0], f[0]),
            Transform(M[0], f[0]),
            Write(f[1]),
            Transform(L[2], f[2]),
            Transform(T[2], f[3]),
            Transform(M[2], f[3]),
            run_time=2,
            lag_ratio=0.2,
        )
        self.remove(M[2])
        self.wait()
        self.play(
            L[2][3].animate.scale(2),
        )
        self.play(
            T[2][2].animate.scale(0.5),
        )
        self.play(
            T[2][4].animate.scale(2),
        )
        self.wait()
        self.play(
            L[2][3].animate.scale(0.333),
        )
        self.play(
            T[2][2].animate.scale(3.5),
        )
        self.play(
            T[2][4].animate.scale(0.333),
        )
        self.wait()
        self.r = Rectangle(fill_color=BLACK, fill_opacity=1, width=16, height=16)
        self.play(
            FadeIn(self.r),
        )
        L[2][3].scale(1 / 0.666)
        T[2][2].scale(2 / 3.5)
        T[2][4].scale(1 / 0.666)

    def show_harmonics(self):
        self.total_time = 0
        axes = self.axes
        self.length = 13

        def create_harmonic(val, i):
            return Harmonic(val, n=i, length=13, amplitude=i)

        trackers = [ValueTracker(1)] + [ValueTracker(0) for _ in range(3)]
        harmonics = [create_harmonic(trackers[i], i + 1) for i in range(len(trackers))]
        left = Dot(self.axes.c2p(-PI, 0), color=RED)
        right = Dot(self.axes.c2p(PI, 0), color=RED)
        nodes_label = Text("Node", color=RED).to_edge(DOWN)
        a_l = Arrow(nodes_label.get_corner(UL), left, color=RED)
        a_r = Arrow(nodes_label.get_corner(UR), right, color=RED)
        anti_node_label = Text("Anti-node", color=BLUE).to_edge(UP)
        a_m = Arrow(anti_node_label.get_bottom(), axes.c2p(0, 0.75), color=BLUE)
        self.play(
            FadeIn(harmonics[0]),
            FadeIn(left),
            FadeIn(right),
        )
        self.wait()
        harmonics[0].start_wave(self.total_time)
        self.play(
            FadeIn(a_l),
            FadeIn(a_r),
            Write(nodes_label),
            Write(anti_node_label),
            FadeIn(a_m),
        )
        self.wait(3)
        self.play(
            FadeOut(a_l),
            FadeOut(a_r),
            Unwrite(nodes_label),
            FadeOut(a_m),
            Unwrite(anti_node_label),
        )
        n = Text("N = 1", color=BLUE, font="monospace").to_edge(DOWN)
        self.play(FadeOut(self.r), Write(n))

        for i in range(1, len(trackers)):
            # for i in range(1, 2):
            self.add(harmonics[i])
            harmonics[i].start_wave(self.total_time)
            new_n = Text(f"N = {i+1}", color=BLUE, font="monospace").to_edge(DOWN)
            self.play(
                trackers[i - 1].animate.set_value(0),
                trackers[i].animate.set_value(1),
                Transform(n, new_n),
            )
            self.wait()
            harmonics[i - 1].stop_wave()
            self.remove(harmonics[i - 1])
        self.play(FadeOut(n))

        for i in range(len(trackers) - 1):
            harmonics[i].time = harmonics[-1].time
            self.add(harmonics[i])
            harmonics[i].time = harmonics[-1].time
            harmonics[i].start_wave(harmonics[-1].time)
            harmonics[i].time = harmonics[-1].time

        self.play(*[t.animate.set_value(0.2) for t in trackers])
        self.wait(2)
        self.total_time = harmonics[-1].time
        for h in harmonics:
            h.time = self.total_time
        last_t = ValueTracker(0)

        def update_wave(mob: Mobject, dt: float) -> None:
            def func(t, n):
                return (
                    2
                    / n
                    * np.sin(n * PI * t / self.length)
                    * np.cos(self.total_time * (PI / 2 + TAU))
                )

            self.total_time += dt
            mob.become(
                ParametricFunction(
                    lambda t: np.array(
                        [
                            t,
                            sum([func(t, x) for x in range(1, len(trackers) + 1)]),
                            0,
                        ]
                    ),
                    t_range=[0, self.length],
                    stroke_opacity=last_t.get_value(),
                )
            )
            mob.shift([-self.length / 2, 0, 0])

        total = VMobject()
        total.add_updater(update_wave)
        self.add(total)
        self.play(last_t.animate.set_value(1))
        self.wait(2)

    def setup_axes(self):
        self.axes = Axes(
            x_range=[-PI, PI, PI],
            y_range=[-1, 1, 0.5],
            x_length=13,
            y_length=5,
            tips=False,
        )
        self.axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )
        # self.add(self.axes)


class StringBreak(String):
    def construct(self):
        self.setup_axes()

        def create_harmonic(val, i):
            return Harmonic(val, n=i, length=13, amplitude=i)

        trackers = [ValueTracker(1)] + [ValueTracker(0) for _ in range(2)]
        harmonics = [
            create_harmonic(trackers[i], i + 1.5) for i in range(len(trackers))
        ]
        left = Dot(self.axes.c2p(-PI, 0), color=RED)
        right = Dot(self.axes.c2p(PI, 0), color=RED)
        n = Text(f"N = {1.5}", color=BLUE, font="Monospace").to_edge(DOWN)
        self.add(left, right, harmonics[0], n)
        harmonics[0].start_wave(0)
        self.wait(2)


class Harmonic(ParametricFunction):
    def __init__(
        self,
        opacity_tracker: ValueTracker,
        n: int = 1,
        length: float = 4,
        period: float = 1,
        amplitude: float = 1,
        **kwargs,
    ):
        self.n = n
        self.length = length
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.opacity_tracker = opacity_tracker
        self.kwargs = kwargs

        super().__init__(
            lambda t: np.array(
                [t, 2 * np.sin(self.n * PI * t / self.length) / self.amplitude, 0]
            ),
            t_range=[0, self.length],
            stroke_opacity=self.opacity_tracker.get_value(),
            **kwargs,
        )
        dots = [
            Dot(
                [self.length / i, 0, 0],
                color=RED,
                fill_opacity=self.opacity_tracker.get_value(),
            )
            for i in range(2, int(n) + 1)
        ]
        self.add(*dots)
        self.shift([-self.length / 2, 0, 0])

    def _update_wave(self, mob: Mobject, dt: float) -> None:
        self.time += dt
        mob.become(
            ParametricFunction(
                lambda t: np.array(
                    [
                        t,
                        2
                        / self.amplitude
                        * np.sin(self.n * PI * t / self.length)
                        * np.cos(self.time * self.period * (PI / 2 + TAU)),
                        0,
                    ]
                ),
                t_range=[0, self.length],
                stroke_opacity=self.opacity_tracker.get_value(),
                **self.kwargs,
            )
        )
        dots = [
            Dot(
                [i * self.length / self.n, 0, 0],
                color=RED,
                fill_opacity=self.opacity_tracker.get_value(),
            )
            for i in range(1, int(self.n))
        ]
        mob.add(*dots)
        mob.shift([-self.length / 2, 0, 0])

    def start_wave(self, time):
        self.wave_center = self.get_center()
        self.time = time
        self.add_updater(self._update_wave)

    def stop_wave(self):
        self.remove_updater(self._update_wave)


class Wind(Scene):
    def construct(self):
        self.equation()
        self.setup_axes()
        self.show_harmonics()
        self.wait()

    def equation(self):
        f1 = MathTex("f_n", "\\approx", "\\dfrac{v}{2L}", "n").to_edge(UP)
        f2 = MathTex("f_n", "\\approx", "\\dfrac{v}{4L}", "n_{odd}").to_edge(DOWN)
        length = Text("Length")
        speed = Text("Speed")
        vg1 = VGroup(length, speed).arrange(RIGHT, buff=1).shift(UP)
        L = MathTex("f", "\\propto", r"\dfrac{1}{L}").next_to(length, DOWN)
        S = MathTex("f", "\\propto", "v").next_to(speed, DOWN).shift(0.3 * DOWN)
        vg2 = VGroup(L, S)
        self.play(Write(vg1), Write(vg2), lag_ratio=0.5, run_time=2)
        self.wait()
        self.play(
            Unwrite(L[1]),
            Unwrite(S[1]),
            Unwrite(length),
            Unwrite(speed),
            Transform(L[0], f1[0]),
            Transform(S[0], f2[0]),
            Write(f1[1]),
            Write(f2[1]),
            Write(f1[3]),
            Write(f2[3]),
            Transform(L[2], f1[2]),
            Transform(S[2], f2[2]),
            run_time=2,
            lag_ratio=0.2,
        )

    def show_harmonics(self):
        vtop = ValueTracker(11)
        amp = ValueTracker(1)
        opac = ValueTracker(0)
        func1 = always_redraw(
            lambda: self.axes.plot(
                lambda x: amp.get_value()
                * 1.5
                * np.sin(vtop.get_value() * x / 2 + PI / 2 * (vtop.get_value() - 1.0))
                + 2.5,
                x_range=[-PI, PI],
                color=GREEN,
                stroke_opacity=opac.get_value(),
            )
        )
        top_pipe_top = Line(self.axes.c2p(-PI, 4), self.axes.c2p(PI, 4))
        top_pipe_bot = Line(self.axes.c2p(-PI, 1), self.axes.c2p(PI, 1))
        top_pipe_blowhole = Line(
            self.axes.c2p(-PI + 0.5, 4), self.axes.c2p(-PI + 1, 4), color=BLUE_E
        )
        re_top_pipe_blowhole = Line(
            self.axes.c2p(-PI + 0.5, 4),
            self.axes.c2p(-PI + 1, 4),
            color=BLUE_E,
            stroke_width=16,
        )

        c = [RED, GREEN]
        func2 = always_redraw(
            lambda: self.axes.plot(
                lambda x: amp.get_value()
                * 1.5
                * np.sin(x / 4 * vtop.get_value() + PI / 4 * vtop.get_value())
                - 2.5,
                x_range=[-PI, PI],
                stroke_opacity=opac.get_value(),
                color=c[round(vtop.get_value()) % 2],
            )
        )
        bottom_pipe_top = Line(self.axes.c2p(-PI, -4), self.axes.c2p(PI, -4))
        bottom_pipe_bot = Line(self.axes.c2p(-PI, -1), self.axes.c2p(PI, -1))
        bottom_pipe_blowhole = Line(
            self.axes.c2p(-PI, -1), self.axes.c2p(-PI, -4), color=BLUE_E
        )
        re_bottom_pipe_blowhole = Line(
            self.axes.c2p(-PI, -1),
            self.axes.c2p(-PI, -4),
            color=BLUE_E,
            stroke_width=16,
        )

        self.play(
            Write(top_pipe_top),
            Write(top_pipe_bot),
            Write(top_pipe_blowhole),
            Write(bottom_pipe_top),
            Write(bottom_pipe_bot),
            Write(bottom_pipe_blowhole),
        )
        self.play(
            Transform(
                bottom_pipe_blowhole, re_bottom_pipe_blowhole, rate_func=there_and_back
            ),
            Transform(
                top_pipe_blowhole, re_top_pipe_blowhole, rate_func=there_and_back
            ),
        )
        n = always_redraw(
            lambda: Text(
                f"n={vtop.get_value():.2f}",
                font="Monospace",
                fill_opacity=opac.get_value(),
            )
        )
        self.wait()
        self.add(func1, func2, n)
        self.play(opac.animate.set_value(1), vtop.animate.set_value(1))
        for i in range(2, 8):
            self.play(amp.animate(rate_func=there_and_back).set_value(-1))
            self.play(vtop.animate.set_value(i))
        self.play(amp.animate(rate_func=there_and_back).set_value(-1))

    def setup_axes(self):
        self.axes = Axes(
            x_range=[-PI, PI, PI],
            y_range=[-4, 4, 1],
            x_length=13,
            y_length=5,
            tips=False,
        )
        self.axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )
        # self.add(self.axes)


class OctaveSidebar(Scene):
    def construct(self):
        self.x_zoom = ValueTracker(0)
        self.construct_nl()

        def construct_nl():
            custom_ticks = [20, 200, 2000, 20000]
            x = NumberLine(
                x_range=[
                    1.301029 + self.x_zoom.get_value(),
                    4.301029 - self.x_zoom.get_value(),
                ],
                length=13,
                include_ticks=False,
                scaling=LogBase(10),
            )
            x.ticks = VGroup()
            for t in custom_ticks:
                x.ticks.add(x.get_tick(t))
            x.add(x.get_tick_marks())
            x.add_labels(
                dict(
                    zip(custom_ticks, custom_ticks),
                )
            )
            return x.shift(DOWN * 2)

        self.add(self.x)
        root = 420.69
        dot_P1 = always_redraw(lambda: Dot(construct_nl().n2p(root), color=BLUE))
        dot_P8 = always_redraw(lambda: Dot(construct_nl().n2p(root * 2), color=BLUE))

        self.add(dot_P1, dot_P8)
        dot1 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**-2)), color=GREEN)
        )
        dot2 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**-1)), color=GREEN)
        )
        dot3 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**2)), color=GREEN)
        )
        dot4 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**3)), color=GREEN)
        )
        dot5 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**-3)), color=GREEN)
        )
        dot6 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**-4)), color=GREEN)
        )
        dot7 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**4)), color=GREEN)
        )
        dot8 = always_redraw(
            lambda: Dot(construct_nl().n2p(root * (2**5)), color=GREEN)
        )
        self.play(
            FadeIn(dot1),
            FadeIn(dot2),
            FadeIn(dot3),
            FadeIn(dot4),
            FadeIn(dot5),
            FadeIn(dot6),
            FadeIn(dot7),
            FadeIn(dot8),
            lag_ratio=0.2,
        )
        self.play(self.x_zoom.animate.set_value(1))
        self.play(
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(dot3),
            FadeOut(dot4),
            FadeOut(dot5),
            FadeOut(dot6),
            FadeOut(dot7),
            FadeOut(dot8),
            lag_ratio=0.2,
        )
        self.wait()

    def construct_nl(self):
        def construct_x():
            x = NumberLine(
                x_range=[
                    1.301029 + self.x_zoom.get_value(),
                    4.301029 - self.x_zoom.get_value(),
                ],
                length=13,
                include_ticks=False,
                scaling=LogBase(10),
            )
            custom_ticks = [20, 200, 2000, 20000]
            x.ticks = VGroup()
            for t in custom_ticks:
                x.ticks.add(x.get_tick(t))
            x.add(x.get_tick_marks())
            x.add_labels(
                dict(
                    zip(custom_ticks, custom_ticks),
                )
            )
            x = x.shift(DOWN * 2)
            return x

        self.x = always_redraw(lambda: construct_x())
        return self.x


class Highlight(Scene):
    def construct(self):
        rectangle = Rectangle(
            height=6,
            width=10.65,
        )
        self.play(Circumscribe(rectangle, fade_out=True, stroke_width=12))
        self.wait()


class Swing(VGroup):
    def phi_function(self, amplitude, acceleration, length, time):
        # return amplitude * np.sin(np.sqrt(acceleration / length) * TAU * time - np.pi / 2)
        return amplitude * np.sin(TAU * time + np.pi / 10)

    def __init__(self, amplitude, acceleration, length, time):
        VGroup.__init__(self)
        self.sound_stamps_there = []
        self.sound_stamps_back = []

        self.amplitude = amplitude
        self.acceleration = acceleration
        self.length = length
        self.time = time
        self.phi = self.phi_function(amplitude, acceleration, length, time)
        self.anchor = Dot(ORIGIN)
        self.line = Line(ORIGIN, length * DOWN)
        self.line.rotate(self.phi * DEGREES, about_point=self.line.get_start())
        self.mass = QuarterCreature(mode="happy", color=BLUE).scale(0.75)
        self.mass.move_to(self.line.get_end())
        self.mobj = VGroup(self.line, self.anchor, self.mass)
        self.add(self.mobj)

    def start(self):
        self.mobj.current_time = 0.0

        def updater(mob, dt):
            mob.current_time += dt
            new_phi = self.phi_function(
                self.amplitude, self.acceleration, self.length, mob.current_time
            )
            mob[0].rotate(
                (new_phi - self.phi) * DEGREES, about_point=self.line.get_start()
            )
            if np.sign(self.phi) < np.sign(new_phi):
                self.sound_stamps_there.append(mob.current_time)
            if np.sign(self.phi) > np.sign(new_phi):
                self.sound_stamps_back.append(mob.current_time)

            self.phi = new_phi
            self.mass.move_to(self.line.get_end()).align_to(
                self.line.get_end(), DOWN
            ).shift(DOWN * 0.05)
            self.mass.look_at(self.line.get_start())

        self.mobj.add_updater(updater)


class Swinging(Scene):
    def construct(self):
        self.start_swing()
        self.interactive_embed()

    def start_swing(self):
        s = Swing(amplitude=32, acceleration=6, length=6, time=0).to_edge(UP)
        pusher = always_redraw(
            lambda: Json()
            .flip()
            .to_edge(RIGHT, DEFAULT_MOBJECT_TO_EDGE_BUFFER * 2)
            .look_at(s.mass.get_bottom())
        )
        pusher_push = always_redraw(
            lambda: Json(mode="push")
            .flip()
            .to_edge(RIGHT, DEFAULT_MOBJECT_TO_EDGE_BUFFER * 2)
            .look_at(s.mass.get_bottom())
        )
        self.add(s, pusher)
        s.start()
        tex = MathTex(r"\dfrac{1\ push}{1\ swings}").to_corner(UL)
        self.add(tex)
        for _ in range(2):
            self.play(Transform(pusher, pusher_push, rate_func=there_and_back))
        for i in range(0, 2):
            new_tex = MathTex(
                r"\dfrac{1\ push}{" + str(i + 2) + r"\ swings}"
            ).to_corner(UL)
            self.play(
                Transform(tex, new_tex),
            )
            self.wait(i)
            self.play(
                Transform(pusher, pusher_push, rate_func=there_and_back),
            )
        new_tex = MathTex(r"\dfrac{1\ push}{N\ swings}").to_corner(UL)
        self.play(Transform(tex, new_tex))
        self.play(
            Transform(pusher, pusher_push, rate_func=there_and_back),
        )
        self.wait()
        self.play(
            Transform(pusher, pusher_push, rate_func=there_and_back),
        )
        self.wait()


class Option2(Scene):
    def construct(self):
        two = Tex("2", color=BLUE).scale(9)
        self.add(two)


class TakeawayCH1(AudioScene):
    def construct(self):
        label_lin = Text("Linear").to_edge(UP)

        audio = AudioGenerator(20, 0.0, 0.5)

        spectrum = [20, 20000]
        custom_ticks = [20, 200, 2000, 20000]
        nl = NumberLine(
            x_range=[20, 20001],
            length=13,
            include_ticks=False,
        )
        ticks = VGroup()
        for t in custom_ticks:
            ticks.add(nl.get_tick(t))
        nl.add(ticks)
        nl.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.play(Write(nl))
        dot = always_redraw(
            lambda: Dot(
                nl.n2p(audio.freq_t.get_value()),
                fill_opacity=audio.vol_t.get_value() * 10,
            )
        )
        # freq = always_redraw(
        #     lambda: Text(
        #         f"{audio.freq_t.get_value()}"
        #     )
        # )
        self.add(dot)
        self.add_audio_generator(audio)

        self.wait()
        self.play(*audio.modify(vol=0.25))
        self.play(
            *audio.modify(freq=20000, rate_func=linear), run_time=3, rate_func=linear
        )
        self.play(*audio.modify(vol=0.0))
        self.remove(dot)
        self.play(*audio.modify(freq=20))
        nl_target = nl.generate_target()
        nl_target.next_to(label_lin)
        self.play(Write(label_lin))
        label_log = Text("Logarithmic")
        lognl = NumberLine(
            x_range=[1.301029, 4.30102999],
            length=13,
            include_ticks=False,
            scaling=LogBase(10),
        ).next_to(label_log, DOWN, buff=1)

        logticks = VGroup()
        for t in custom_ticks:
            logticks.add(lognl.get_tick(t))
        lognl.add(logticks)
        lognl.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.play(
            TransformFromCopy(nl, lognl),
            TransformFromCopy(label_lin, label_log),
            nl.animate.next_to(label_lin, DOWN, buff=1),
        )
        dot = always_redraw(
            lambda: Dot(
                nl.n2p(np.power(10, audio.log_freq_t.get_value())),
                fill_opacity=audio.vol_t.get_value() * 10,
            )
        )
        dot_log = always_redraw(
            lambda: Dot(
                lognl.n2p(np.power(10, audio.log_freq_t.get_value())),
                fill_opacity=audio.vol_t.get_value() * 10,
            )
        )
        self.add(dot, dot_log)
        self.wait()
        self.play(*audio.modify(vol=0.25))
        self.play(
            *audio.modify(freq=20000, rate_func=rate_functions.loglinear),
            run_time=5,
            rate_func=rate_functions.loglinear,
        )
        self.play(*audio.modify(vol=0.0))
        copy_lognl = lognl.copy()
        extra_ticks = [40, 80, 400, 800, 4000, 8000]
        for t in extra_ticks:
            copy_lognl.add(copy_lognl.get_tick(t))
        copy_lognl.add_labels(
            dict(
                zip(extra_ticks, extra_ticks),
            )
        )
        self.play(*audio.modify(freq=20), FadeIn(copy_lognl), FadeOut(lognl))
        self.play(
            FadeOut(nl),
            Unwrite(label_lin),
            copy_lognl.animate.center(),
            label_log.animate.to_edge(UP),
        )
        brace = BraceBetweenPoints(
            copy_lognl[3].get_center(), copy_lognl[4].get_center(), UP
        )
        brace.add(Text("1:2").next_to(brace, UP))
        self.play(Write(brace))
        self.play(
            brace.animate.move_to(
                copy_lognl.n2p(200), aligned_edge=LEFT, coor_mask=np.array([1, 0, 0])
            )
        )
        self.wait()
        self.play(
            brace.animate.move_to(
                copy_lognl.n2p(2000), aligned_edge=LEFT, coor_mask=np.array([1, 0, 0])
            )
        )
        self.wait()
        self.play(Unwrite(brace))
        brace = BraceBetweenPoints(
            copy_lognl[3].get_center(), copy_lognl[5].get_center(), UP
        )
        brace.add(Text("1:10").next_to(brace, UP))
        brace.move_to(
            copy_lognl.n2p(20), aligned_edge=LEFT, coor_mask=np.array([1, 0, 0])
        )
        low = Text("Low", color=BLUE).next_to(brace, UP)
        self.play(Write(brace), Write(low))
        self.play(
            brace.animate.move_to(
                copy_lognl.n2p(200), aligned_edge=LEFT, coor_mask=np.array([1, 0, 0])
            ),
            low.animate.to_edge(UP).set_opacity(0),
        )
        mid = Text("Mid", color=GREEN).next_to(brace, UP)
        self.play(Write(mid))
        self.play(
            brace.animate.move_to(
                copy_lognl.n2p(2000), aligned_edge=LEFT, coor_mask=np.array([1, 0, 0])
            ),
            mid.animate.to_edge(UP).set_opacity(0),
        )
        high = Text("High", color=YELLOW).next_to(brace, UP)
        self.play(Write(high))
        self.play(Unwrite(brace), high.animate.to_edge(UP).set_opacity(0))
        self.wait()

        self.remove(low, mid, high)
        values = [20, 40, 200, 1000, 2000, 20000]
        points = [copy_lognl.n2p(f) for f in values]
        arcs = []
        for p in range(len(points) - 1):
            arcs.append(ArcBetweenPoints(points[p + 1], points[p]).set_color(BLUE))
        v = ValueTracker(20)
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(copy_lognl.n2p(v.get_value()))
        )
        label = MathTex("\\dfrac{Hz_{f}}{Hz_{o}}").shift(2 * DOWN)
        equals1 = MathTex("=").next_to(label, RIGHT)

        fraction_bar = Text("—").stretch(4, 0).next_to(equals1, RIGHT)
        ratio = always_redraw(
            lambda: VGroup(
                Text(f"{int(v.get_value())}", font="Monospace", color=YELLOW).next_to(
                    fraction_bar, UP
                ),
                Text("20", font="Monospace").next_to(fraction_bar, DOWN),
            )
        )
        equals2 = MathTex("=").next_to(fraction_bar, RIGHT)
        simplified = always_redraw(
            lambda: Text(
                f"{round(v.get_value()/20, 2)}", font="Monospace", color=BLUE
            ).next_to(equals2, RIGHT)
        )
        grouped = always_redraw(
            lambda: VGroup(label, equals1, fraction_bar, ratio, equals2, simplified)
            .center()
            .to_edge(DOWN)
        )
        self.play(FadeIn(dot), FadeIn(grouped))
        self.wait()
        self.play(FadeIn(arcs[0]))
        for p in range(len(points) - 1):
            factor = (
                MathTex(f"{values[p+1]/values[p]}", color=BLUE)
                .move_to(arcs[p].get_top())
                .align_to(arcs[2], UP)
                .shift(1.5 * UP)
            )
            self.play(
                TransformFromCopy(arcs[p], factor),
                v.animate.set_value(values[p + 1]),
                FadeIn(arcs[p + 1]) if p < len(points) - 2 else Wait(),
                lag_ratio=0.5,
            )
            self.wait()

        # reduced = MathTex("\\dfrac{22}{125}", color=RED).move_to(factor2).shift(RIGHT)
        # factors = [factor3, factor4]
        # self.play(
        #     factor1.animate.move_to(factor2[0][4:6]).set_opacity(0),
        #     factor2[0][3:6].animate.set_opacity(0),
        #     AnimationGroup(
        #         *[ReplacementTransform(f, reduced) for f in factors], lag_ratio=0.05
        #     ),
        # )
        # self.wait()
        # self.play(
        #     factor2.animate.move_to(reduced[0][3:]).set_opacity(0),
        #     reduced[0][2:].animate.set_opacity(0),
        #     reduced[0][:2].animate.set_color(BLUE),
        #     lag_ratio=0.05,
        # )


class Superpose(AudioScene):
    def construct(self):
        left_speaker = SVGMobject("Audio").set_color(WHITE).to_edge(LEFT)
        right_speaker = SVGMobject("Audio").set_color(RED).flip().to_edge(RIGHT)
        self.play(
            Write(left_speaker),
            Write(right_speaker),
        )

        left_audio = AudioGenerator(420.69, 0)
        right_audio = AudioGenerator(420.69, 0)
        self.add_audio_generator(left_audio)
        self.add_audio_generator(right_audio)

        TET_12 = [2 ** (x / 12) for x in range(13)]
        self.play(*left_audio.modify(vol=0.1) + right_audio.modify(vol=0.1))
        for left in TET_12[1:]:
            self.play(
                *left_audio.modify(420.69 * left),
                run_time=0.2,
            )
            self.wait(0.8, use_last_val=False)
        self.play(*left_audio.modify(vol=0.0) + right_audio.modify(vol=0.0))


def plot_x_y(ax: ThreeDAxes, func, offset=2):
    t_range = np.array(ax.x_range, dtype=float)
    t_range = np.array([20, 20000, 1])
    graph = ParametricFunction(
        lambda t: ax.coords_to_point(t, func(t), offset),
        t_range=t_range,
    )
    return graph


class FourierTransform(Scene):
    sample_density = 1 / 20
    audio_file = Path.cwd() / "instruments.wav"
    production = True
    graph_point = 0.46
    time_selection = (6.0, 0.5)

    def construct(self):
        self.plot_audio_waveform()
        self.zoom_to_selection(self.graph_point, self.time_selection)
        self.fix_3d_rotation()
        self.fourier_analysis()
        self.demonstrate_harmonics()
        self.wait()
        self.interactive_embed()

    def fix_3d_rotation(self):
        # Camera should be allowed to move more freely -- ManimCE feature improvement incoming?
        frame = self.camera
        for mob in self.mobjects:
            mob.rotate(PI / 2, RIGHT, ORIGIN)
        frame.set_euler_angles(0, PI / 2)
        self.add(frame)

    def plot_audio_waveform(self):
        sample_rate, signal = wavfile.read(self.audio_file)
        time = len(signal) / sample_rate
        signal = signal[:, 0] / np.abs(signal).max()

        signal = signal[:: int(1 / self.sample_density)]

        axes = Axes(
            (0, len(signal), sample_rate * self.sample_density),
            (-1, 1.000001, 0.25),
            x_length=13,
            y_length=6,
            tips=False,
            y_axis_config={"include_numbers": True},
        )
        axes.to_edge(LEFT)
        time_label = Text("Time", font_size=60)
        time_label.next_to(axes.c2p(len(signal) / 2, 0), 3 * DOWN).align_to(
            time_label.get_right(), LEFT
        )
        intensity_label = Text("Intensity", font_size=60)
        intensity_label.next_to(axes.c2p(0, 1), UP * 0.8).align_to(
            intensity_label.get_center(), LEFT
        )
        xs = np.arange(len(signal))
        points = axes.c2p(xs, signal)
        points = points.T
        graph = OpenGLVMobject(
            stroke_width=DEFAULT_STROKE_WIDTH / 2,
            stroke_color=GREEN_E,
            fill_color=PINK,
        )
        graph.should_render = True
        graph.set_points_as_corners(points)
        self.graph = graph
        self.axes = axes
        self.sample_rate = sample_rate
        self.signal = signal
        vt = ValueTracker(0)
        if self.production:
            self.play(FadeIn(self.axes), Write(time_label), Write(intensity_label))
            time_label.add_updater(
                lambda m: m.next_to(
                    axes.c2p(clip(vt.get_value(), len(signal) / 2, len(signal)), 0),
                    3 * DOWN,
                ).align_to(m.get_right(), LEFT)
            )
            self.play(
                Create(
                    self.graph,
                    rate_func=linear,
                ),
                ShowPassingFlash(
                    self.graph.copy().set_stroke(GREEN_B, 3),
                    time_width=0.01,
                    rate_func=linear,
                ),
                vt.animate(rate_func=linear).set_value(len(signal)),
                run_time=time,
            )
            self.play(FadeOut(intensity_label), FadeOut(time_label))
        else:
            axes.set_opacity(0.5)
            self.add(self.axes, self.graph)
            self.remove(time_label, intensity_label)

    def zoom_to_selection(self, graph_point, zoom_rect_dims):
        axes = self.axes
        graph = self.graph
        point = graph.pfp(graph_point)[0] * RIGHT
        zoom_rect = Rectangle(WHITE, *zoom_rect_dims)
        zoom_rect.move_to(point)
        zoom_rect.set_stroke(WHITE, 2)

        graph_snippet = OpenGLVMobject(stroke_color=GREEN_D)
        graph_points = graph.get_anchors()
        lx = zoom_rect.get_left()[0]
        rx = zoom_rect.get_right()[0]
        xs = graph_points[:, 0]
        snippet_points = graph_points[(xs > lx) * (xs < rx)]
        graph_snippet.set_points_as_corners(snippet_points)
        point = graph_snippet.get_center().copy()
        point[1] = axes.get_origin()[1]
        zoom_rect.move_to(point)

        movers = [axes, graph, graph_snippet, zoom_rect]

        frame = self.camera

        new_axes = Axes(
            (
                0,
                len(graph_snippet.points),
                len(graph_snippet.points) * self.sample_density,
            ),
            (-1, 1.00001, 0.25),
            x_length=14.2,
            tips=False,
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_numbers": True},
        )
        self.shift = 7
        new_axes.shift(LEFT * self.shift - new_axes.get_origin())

        height = (
            new_axes.y_axis.submobjects[0].get_top()
            - new_axes.y_axis.submobjects[0].get_bottom()
        )
        width = new_axes.get_right() - new_axes.x_axis.get_left()
        for mover in movers:
            mover.generate_target()
            mover.target.stretch(width[0] / zoom_rect.get_width(), 0, about_point=point)
            mover.target.stretch(
                height[1] / zoom_rect.get_height(), 1, about_point=point
            )
            mover.target.shift(-point)
        graph_snippet.target.set_stroke(width=2)
        zoom_rect.target.set_stroke(opacity=0)
        axes.target.set_stroke(opacity=0)
        graph.target.set_stroke(opacity=0)

        if self.production:
            self.play(Write(zoom_rect))
            self.play(
                *[MoveToTarget(mover) for mover in movers],
                FadeIn(new_axes),
                run_time=4,
            )
        else:
            self.add(zoom_rect, new_axes)
            self.play(*[MoveToTarget(mover) for mover in movers], run_time=1)

        self.remove(graph, axes)

        self.original_graph = graph
        self.original_axes = axes
        self.axes = new_axes
        self.graph = graph_snippet

        return new_axes, graph_snippet

    @staticmethod
    def topk(array, k, axis=-1, sorted=False):
        # Use np.argpartition is faster than np.argsort, but do not return the values in order
        # We use array.take because you can specify the axis
        partitioned_ind = np.argpartition(array, -k, axis=axis).take(
            indices=range(-k, 0), axis=axis
        )
        # We use the newly selected indices to find the score of the top-k values
        partitioned_scores = np.take_along_axis(array, partitioned_ind, axis=axis)

        if sorted:
            # Since our top-k indices are not correctly ordered, we can sort them with argsort
            # only if sorted=True (otherwise we keep it in an arbitrary order)
            sorted_trunc_ind = np.flip(
                np.argsort(partitioned_scores, axis=axis), axis=axis
            )

            # We again use np.take_along_axis as we have an array of indices that we use to
            # decide which values to select
            ind = np.take_along_axis(partitioned_ind, sorted_trunc_ind, axis=axis)
            scores = np.take_along_axis(partitioned_scores, sorted_trunc_ind, axis=axis)
        else:
            ind = partitioned_ind
            scores = partitioned_scores

        return scores, ind

    def fourier_analysis(self):
        t_axes: Axes = self.axes
        graph: OpenGLVMobject = self.graph

        t_max = t_axes.x_range[1]
        ts, values = t_axes.p2c(graph.points[::10]).T
        signal = values[(ts > 0) * (ts < t_max)]
        signal_fft = np.fft.fft(signal)
        signal_fft /= len(signal)
        signal_fft_mag = np.abs(signal_fft)
        signal_fft_phase = np.log(signal_fft).imag

        max_freq = self.sample_rate / signal.size
        freqs = np.fft.fftfreq(signal.size, 1 / max_freq) % max_freq
        f_axes = Axes(
            (0, freqs[-1] / 2, (freqs[-1] + freqs[-1] - freqs[-2]) / 2 / len(values)),
            # (0, freqs[-1] / 2, freqs[-1] / len(values)),
            (0, 1, 1 / 4),
            x_length=15,
            y_length=(round(config.frame_height) - 2) / 2,
            tips=False,
        )
        self.halfway = (freqs[-1] + freqs[-1] - freqs[-2]) / 2
        f_axes.rotate(PI / 2, OUT)
        f_axes.rotate(PI / 2, UP)
        f_axes.shift(t_axes.get_origin() - f_axes.get_origin())

        freq_label = Text("Frequency", font_size=60)
        freq_label.rotate(PI / 2, UP)
        freq_label.rotate(PI / 2, RIGHT)
        freq_label.next_to(
            f_axes.c2p(freqs[len(freqs) // 4], 0), config.frame_height * OUT
        )
        if self.production:
            self.play(Write(f_axes.x_axis), Write(freq_label))
        else:
            self.add(f_axes)
            self.add(freq_label)
        self.freq_label = freq_label
        frame: OpenGLCamera = self.camera
        target = frame.generate_target()
        target.set_euler_angles(0.6, 1.35)
        target.set_height(11)
        target.move_to([3, 2, 0])
        sine_waves = VGroup()
        amps = []
        shift = self.shift / 2
        self.freqs = freqs
        for index in range(1, len(freqs)):
            freq = freqs[index]
            amp = signal_fft_mag[index]
            phase = signal_fft_phase[index]
            wave = t_axes.plot(
                lambda t: 2 * amp * np.cos(TAU * freq / max_freq / 100 * (t + phase)),
                x_range=(0, t_max),
                use_vectorized=True,
            )
            wave.shift(f_axes.c2p(freq, 0) / 2 + [shift, 0, 0])
            wave.set_stroke(opacity=clip(15 * amp, 0.25, 1))
            wave.amp = amp
            wave.freq = freq
            wave.phase = phase
            amps.append(amp)
            sine_waves.add(wave)

        sine_waves.set_submobject_colors_by_gradient(
            RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE
        )
        self.play(
            *[TransformFromCopy(graph, wave) for wave in sine_waves],
            MoveToTarget(frame),
            t_axes.y_axis.submobjects[1].animate.rotate(PI / 2, OUT),
            lag_ratio=0.2,
            run_time=3,
        )
        target.set_euler_angles(PI / 2, PI / 2, 0)
        target.move_to([0, 7.5, 0.5])
        target.set_height(10)

        self.play(MoveToTarget(frame), Unwrite(self.graph))
        self.wait()
        fft_graph = OpenGLVMobject(
            stroke_width=DEFAULT_STROKE_WIDTH / 2,
        )
        fft_graph.set_points_as_corners(
            [f_axes.c2p(wave.freq / 2, 2 * wave.amp) for wave in sine_waves]
        )
        fft_graph.set_stroke(GREEN, 5, 1)
        self.add(fft_graph)
        self.f_axes = f_axes
        self.t_axes = t_axes

        keep_waves = VGroup()
        top_k_mag, top_k_ind = self.topk(signal_fft_mag[1:], 8)
        for k in sorted(top_k_ind):
            keep_waves.add(sine_waves[k])
        for wave in keep_waves:
            sine_waves.remove(wave)
        self.play(FadeOut(sine_waves))
        self.sine_waves = sine_waves
        self.keep_waves = keep_waves
        self.f_label = freq_label

    def demonstrate_harmonics(self):
        frame = self.camera
        frame.generate_target()
        frame.target.set_height(6)
        f_axes = self.f_axes
        keep_waves = self.keep_waves

        f_axes.x_axis.ticks.remove(*f_axes.x_axis.ticks)
        alias_box = Rectangle(
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=1,
            width=15 / 2,
            height=(round(config.frame_height) - 2) / 2,
            opacity=0.5,
        )
        alias_box.rotate(PI / 2, UP).rotate(PI / 2, RIGHT)
        alias_box.shift(self.f_axes.c2p(self.halfway / 2, 0) - alias_box.get_bottom())
        alias_box.shift(OUT * 1.5)
        lines = VGroup()
        for wave in keep_waves[: len(keep_waves) // 2]:
            lines.add(
                Line(
                    f_axes.c2p(wave.freq / 2, 2 * wave.amp),
                    f_axes.c2p(wave.freq / 2, 0),
                    color=wave.color,
                )
            )

        self.play(
            *[Unwrite(wave) for wave in keep_waves],
            MoveToTarget(frame),
            Write(lines),
            lag_ratio=0.5,
            run_time=2,
        )
        self.wait()
        self.play(FadeIn(alias_box), FadeOut(self.f_label))
        self.lines = lines
        fun = Text("Fundamental", font_size=50)
        fun.rotate(PI / 2, UP)
        fun.rotate(PI / 2, RIGHT)
        fun.next_to(
            f_axes.c2p(self.freqs[len(self.freqs) // 8], 0), config.frame_height * OUT
        )
        fun_arrow = Line(fun, lines[0].get_top())
        ot = Text("Overtones", font_size=40)
        ot.rotate(PI / 2, UP)
        ot.rotate(PI / 2, RIGHT)
        ot.next_to(
            f_axes.c2p(self.freqs[len(self.freqs) // 4], 0),
            config.frame_height / 1.5 * OUT,
        )
        ot_arrow0 = Line(ot, lines[1].get_top())
        ot_arrow1 = Line(ot, lines[2].get_top())
        self.play(
            Write(fun),
            Write(fun_arrow),
            Write(ot),
            Write(ot_arrow1),
            Write(ot_arrow0),
        )
        # frame = self.camera
        self.alias_box = alias_box
        # frame.set_euler_angles(0,0,PI/8)


class CameraTest(Scene):
    """For camera debugging"""

    def construct(self):
        self.fix_3d_rotation()
        self.test()
        self.interactive_embed()

    def fix_3d_rotation(self):
        # Camera should be allowed to move more freely -- ManimCE feature improvement incoming?
        frame = self.camera
        for mob in self.mobjects:
            mob.rotate(PI / 2, RIGHT)
        frame.set_euler_angles(0, PI / 2)
        self.add(frame)

    def test(self):
        f_axes = Axes(
            (0, 960, 960 / 100),
            # (0, freqs[-1] / 2, freqs[-1] / len(values)),
            (0, 1, 1 / 4),
            x_length=15,
            y_length=(round(config.frame_height) - 2) / 2,
            tips=False,
            # x_axis_config={"include_ticks": False},
        )
        # f_axes.rotate(PI / 2, LEFT)
        f_axes.rotate(PI / 2, OUT)
        f_axes.rotate(PI / 2, UP)
        self.add(f_axes)
        frame = self.camera
        frame.generate_target()
        frame.target.set_euler_angles(1.2, 1.35)
        frame.target.set_height(10.5)
        frame.target.move_to([1.5, 5.0, 0.7])
        self.play(MoveToTarget(frame))

        self.f = f_axes.x_axis


class ResonanceChapter(Scene):
    def construct(self):
        reso = Tex("Resonance", font_size=60)
        self.play(Write(reso))
        self.wait()


class Discrepancy(Scene):
    def construct(self):
        t = Table(
            [
                ["N", "Tone", "Harmonics", "Partials"],
                ["1", "fundamental tone", "1st harmonic", "1st partial"],
                ["2", "1st overtone", "2nd harmonic", "2nd partial"],
                ["3", "2nd overtone", "3rd harmonic", "3rd partial"],
                ["...", "...", "...", "..."],
            ],
        ).scale(0.5)
        b = t.copy()
        self.play(Write(t, reverse=True), Write(b))
        self.wait()


class DiscrepancyWind(Scene):
    def construct(self):
        t = (
            Table(
                [
                    ["N", "Tone", "Harmonics", "Partials"],
                    ["1", "fundamental tone", "1st harmonic", "1st partial"],
                    ["2", "1st overtone", "2nd harmonic", "2nd partial"],
                    ["3", "2nd overtone", "3rd harmonic", "3rd partial"],
                    ["...", "...", "...", "..."],
                ],
            )
            .scale(0.5)
            .to_edge(UP)
        )
        t_odd = (
            Table(
                [
                    ["N", "Tone", "Harmonics", "Partials"],
                    ["1", "fundamental tone", "1st harmonic", "1st partial"],
                    ["2", "--", "2nd harmonic", "--"],
                    ["3", "1st overtone", "3rd harmonic", "2nd partial"],
                    ["...", "...", "...", "..."],
                ],
            )
            .scale(0.5)
            .to_edge(DOWN)
        )
        flute = Text("Flute").rotate(PI / 2).next_to(t.get_left(), LEFT)
        clarinet = Text("Clarinet").rotate(PI / 2).next_to(t_odd.get_left(), LEFT)
        self.play(
            Write(t, reverse=True),
            Write(t_odd, reverse=True),
            Write(clarinet),
            Write(flute),
        )
        self.add(t, t_odd)
        self.wait()


class HarmonicSeries(CreatureScene):
    def construct(self):
        hs = MathTex(r"\sum_{n=1} ^{\infty} \dfrac{1}{n}")
        self.add(hs)
        self.creature.look_at(hs)


class Recall(Scene):
    def construct(self):
        s = (
            SVGMobject(MEDIA_DIR + "Bubbles_thought_high.svg", stroke_width=2)
            .flip()
            .shift(UP)
            .scale(2.5)
        )
        j = (
            Json("push", fill_color=GREY_BROWN)
            .flip()
            .to_edge(RIGHT, DEFAULT_MOBJECT_TO_EDGE_BUFFER * 2)
            .look_at(s)
        )

        self.add(j)
        self.play(Write(s), j.animate.change_mode("pondering"))

        self.wait()


class RecallBubble(Scene):
    def construct(self):
        s = (
            SVGMobject(MEDIA_DIR + "Bubbles_thought_high.svg", stroke_width=2)
            .flip()
            .shift(UP)
            .scale(2.5)
        )
        self.play(
            Write(s),
        )


class Number3(Scene):
    def construct(self):
        self.add(MathTex("3N"))


class BesselSurface(Surface):
    def __init__(
        self,
        boundary: float,
        order: ValueTracker,
        mode: ValueTracker,
        t: ValueTracker,
    ):
        self.boundary = boundary
        self.order = self.n = order.get_value()
        self.mode = self.k = mode.get_value()
        self.t = t
        zeroes = special.jn_zeros(self.n, self.k)
        self.zero = zeroes[-1]
        # first_zero = 2.40482556  # of order zero (i.e. first partial/fundamental frequency location)
        # freq = zeroes[-1] / first_zero
        # circles = VGroup()
        # for i in range(len(zeroes)):
        #     circles.add(Circle(zeroes[i] / self.zero * 3))

        # lines = VGroup()
        # for i in range(int(self.n)):
        #     line = Line(axes.c2p(0, 1, 0), axes.c2p(0, -1, 0), color=YELLOW).rotate(
        #         PI * (i / self.n), OUT
        #     )
        #     lines.add(line)
        # frequency = (
        #     MathTex(
        #         "f_{" + f"{int(self.n)},{int(self.k)}" + "}",
        #         r"\approx",
        #         f"{round(freq, 3)}",
        #         r"f_{0,1}",
        #     )
        #     .rotate(PI / 2, RIGHT)
        #     .shift(OUT * 2 + 2 * RIGHT)
        # )
        # frequency[0][1].set_color(YELLOW)
        # frequency[0][3].set_color(RED)
        # frequency[2].set_color(ORANGE)
        # self.time_based_updaters = []

        # inharmonic_label = (
        #     Text("Inharmonic", color=ORANGE)
        #     .rotate(PI / 2, RIGHT)
        #     .next_to(frequency[2], 16 * UP)
        # )
        self.axes = ThreeDAxes(
            [-1, 1, 1], [-1, 1, 1], [-1, 1, 1], x_length=6, y_length=6, z_length=4
        )
        axes = ThreeDAxes(
            [-1, 1, 1], [-1, 1, 1], [-1, 1, 1], x_length=6, y_length=6, z_length=4
        )
        print("INIT",self.axes, axes)
    
        super().__init__(lambda u,v: axes.c2p(*self.calc(u, v)), u_range=[0, boundary], v_range=[0, TAU])
        # self.add(lines, circles, frequency, inharmonic_label)

    def drumhead_height(self, r, theta):
        z = (
            np.sin(self.t.get_value())
            * np.cos(self.n * theta)
            * special.jv(self.n, r * self.zero)
        )
        return z

    def calc(self, u, v):
        r, theta = u, v
        print("FUNC", self.axes)
        return (
            r * np.cos(theta),
            r * np.sin(theta),
            self.drumhead_height(r, theta),
        )


class DrumMembrane(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        o = ValueTracker(0)
        m = ValueTracker(1)
        a = always_redraw(lambda: BesselSurface(1, o, m, tracker))
        # self.set_camera_orientation(PI / 3)
        # self.begin_ambient_camera_rotation(.03)
        self.add(a)

        # for i in range(4):
        #     o.set_value(i),
        #     tracker.set_value(0)
        #     for j in range(1, 4):
        #         m.set_value(j),
        #         self.play(
        #             tracker.animate.set_value(2 * PI), run_time=1, rate_func=linear
        #         )
        #         tracker.set_value(0)
        self.interactive_embed()


class ConicalExercise(MusicScene, ClassScene):
    def construct(self):
        self.setup_axes()
        self.ask()

    def setup_axes(self):
        self.axes = Axes(
            x_range=[-PI, PI, PI],
            y_range=[-4, 4, 1],
            x_length=13,
            y_length=5,
            tips=False,
        )
        self.axes.add_coordinates(
            dict(
                zip(
                    [-PI] + [x for x in np.arange(PI, 5 * PI, PI)],
                    [MathTex("-\\pi")]
                    + [
                        MathTex(f"{x}\\pi") if abs(x) > 1 else MathTex("\\pi")
                        for x in range(1, 5)
                    ],
                )
            )
        )

    def ask(self):
        pipe_top = Line(self.axes.c2p(-PI / 2, 3), self.axes.c2p(PI, 3))
        pipe_bot = Line(self.axes.c2p(-PI / 2, 2), self.axes.c2p(PI, 2))
        pipe_blowhole = Line(
            self.axes.c2p(-PI / 2, 3), self.axes.c2p(-PI / 2, 2), color=BLUE_E
        )
        amp = ValueTracker(0.5)
        cone_blowhole = Line(
            self.axes.c2p(-PI / 2, 2 + amp.get_value()),
            self.axes.c2p(-PI / 2, 3 - amp.get_value()),
            color=BLUE_E,
        )
        cone_top = Line(cone_blowhole.get_top(), self.axes.c2p(PI, 3 + amp.get_value()))
        cone_bot = Line(
            cone_blowhole.get_bottom(), self.axes.c2p(PI, 2 - amp.get_value())
        )
        clarinet = VGroup(pipe_top, pipe_blowhole, pipe_bot)
        oboe = VGroup(cone_top, cone_blowhole, cone_bot)

        self.add(clarinet)
        self.creature.look_at(pipe_top.get_right()).change_mode("pondering")
        self.wait()
        self.change_student_modes(
            *["pondering", "puzzled", "plain", "pondering", "erm"],
            look_at_arg=oboe,
            lag_ratio=0.04,
        )
        self.play(
            Transform(clarinet, oboe),
        )
        self.wait()

        cone_l = MathTex(r"\dfrac{1}{r}", r"\sin(\dfrac{\pi r n}{L})").to_edge(UP)
        l = ValueTracker(PI + PI / 2)
        start = ValueTracker(-PI / 2)

        def pressure_func(x: float, n: int):
            harmonic = PI * n * (x - start.get_value())
            c = 1 / (x - start.get_value())
            sin_func = np.sin(harmonic / l.get_value())
            return amp.get_value() * c * sin_func + 2.5

        plots = VGroup()
        for i in range(1, 6):
            plots.add(
                self.axes.plot(
                    lambda x: pressure_func(x, i),
                    x_range=[start.get_value() + 0.001, PI, 0.001],
                    color=GREEN_A,
                    # use_smoothing=False
                )
            )

        plot_inverted = (
            plots.copy().flip(RIGHT, about_point=oboe.get_center()).set_color(GREEN_E)
        )
        self.play(Write(plots[0]), Write(plot_inverted[0]), Write(cone_l))
        for i in range(1, len(plots)):
            self.play(
                Unwrite(plots[i - 1]),
                Unwrite(plot_inverted[i - 1]),
                Write(plots[i]),
                Write(plot_inverted[i]),
                lag_ratio=0.3,
            )
            self.wait()
        sr = SurroundingRectangle(cone_l.submobjects[0])
        self.play(Create(sr))
        self.wait()
        self.play(FadeOut(sr))
        self.play(self.creature.animate.change_mode("happy"))
        self.change_all_student_modes("pondering")
        self.wait()


class Transmission3D(Scene):
    run_time = 10

    def construct(self):
        frame = self.camera
        frame.rotate(PI / 3, OUT + RIGHT)
        target = frame.generate_target()
        frame.rotate(PI / 3, OUT)
        self.show_dots()
        self.planes()
        self.interactive_embed()

    def show_dots(self):
        self.t = ValueTracker(0)
        self.amp = ValueTracker(0.5)
        self.kappa = ValueTracker(1)
        self.omega = ValueTracker(PI)
        self.opacity = ValueTracker(0)
        num_dots = 1000

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
        self.add(self.pf)

        seed = random.seed(0)
        dots = VGroup(
            *[
                Dot().shift(
                    RIGHT * random.uniform(-14, 14) + UP * random.uniform(-2, 2)
                )
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

        [
            dots[i].set_opacity(0.25) if i % 25 else dots[i].set_color(YELLOW)
            for i in range(len(dots))
        ]

    def planes(self):
        def follow_wave(phase=0):
            def create_planes():
                modulo = (
                    self.t.get_value() * self.omega.get_value() / self.kappa.get_value()
                    + phase / self.kappa.get_value()
                ) % (TAU / self.kappa.get_value())
                point = self.pf.get_point_from_function(modulo)
                left_point = self.pf.get_point_from_function(
                    modulo - (TAU / self.kappa.get_value())
                )
                leftest_point = self.pf.get_point_from_function(
                    modulo - (2 * TAU / self.kappa.get_value())
                )
                return VGroup(
                    Circle(2).move_to(leftest_point).rotate(PI / 2, UP),
                    Circle(2).move_to(left_point).rotate(PI / 2, UP),
                    Circle(2).move_to(point).rotate(PI / 2, UP),
                )

            return create_planes

        compression_planes = always_redraw(follow_wave(PI / 2))
        self.add(compression_planes)

        self.play(
            self.t.animate(run_time=self.run_time, rate_func=linear).set_value(
                self.run_time
            ),
            MoveToTarget(
                self.camera, run_time=self.run_time, rate_functions=there_and_back
            ),
        )


class Intensity(Scene):
    def construct(self):
        intensity = MathTex(r"Intensity = \dfrac{1}{r^2}")
        cone = Cone(2, 8, LEFT).set_color_by_gradient(BLUE, BLACK).shift(LEFT * 4)
        frame: OpenGLCamera = self.camera
        target = frame.generate_target()
        frame.rotate(PI / 12, UP)
        self.play(
            Create(cone),
            Write(intensity),
        )
        self.play(MoveToTarget(frame), run_time=4)
        self.interactive_embed()


class Amplitude(Scene):
    def construct(self):
        intensity = MathTex("Intensity", "=", r"\dfrac{1}{r^2}")
        amplitude = MathTex("Amplitude", r"\propto", r"\sqrt{Intensity}").next_to(
            intensity, DOWN
        )
        amplitude_sub = MathTex(
            "Amplitude", r"\propto", r"\sqrt{\dfrac{1}{r^2}}"
        ).next_to(intensity, DOWN)
        amplitude_simplified = MathTex(
            "Amplitude", r"\propto", r"\dfrac{1}{r}"
        ).next_to(intensity, DOWN)
        self.add(intensity)
        self.play(Write(amplitude))
        # self.wait()
        self.play(TransformMatchingTex(amplitude, amplitude_sub))
        self.play(TransformMatchingTex(amplitude_sub, amplitude_simplified))

class Bessel(Surface):
    def __init__(self, n: ValueTracker, k: ValueTracker, t: ValueTracker):
        self.n = n
        self.k = k
        self.t = t
        axes = ThreeDAxes(
            [-1, 1, 1], [-1, 1, 1], [-1, 1, 1], x_length=6, y_length=6, z_length=6
        )
        zeroes = special.jn_zeros(self.n.get_value(), self.k.get_value())
        self.zeroes = zeroes
        self.last_zero = zeroes[-1]
        zero = zeroes[-1]
        super().__init__(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[0, 1],
            v_range=[0, TAU],
            should_make_jagged=True
        )
        first_zero = 2.40482556  # of order zero (i.e. first partial/fundamental frequency location)
        self.freq = self.last_zero / first_zero

        circles = VGroup()
        lines = VGroup()

        for i in range(len(self.zeroes)):
            circles.add(Circle(self.zeroes[i] / self.last_zero * 3))

        for i in range(int(self.n.get_value())):
            line = Line(axes.c2p(0, 1, 0), axes.c2p(0, -1, 0), color=YELLOW)
            if self.n.get_value() % 2 == 0:
                line.rotate(PI * (i / self.n.get_value()) + PI/2/self.n.get_value(), OUT)
            else:
                line.rotate(PI * (i / self.n.get_value()), OUT)
            lines.add(line)

        frequency = self.create_mathtex()

        self.add(circles, lines, frequency)


    def create_mathtex(self):
        a = MathTex(
            "f_{" + f"{int(self.n.get_value())},{int(self.k.get_value())}" + "}",
            r"=" if self.n.get_value() == 0 and self.k.get_value() == 1 else r"\approx",
            f"{round(self.freq, 3)}",
            r"f_{0,1}"
        ).rotate(PI / 2, RIGHT).shift((OUT +RIGHT+UP ) * 2 )
        a[0][1].set_color(YELLOW)
        a[0][3].set_color(RED)
        a[2].set_color(ORANGE)
        return a

    def drumhead_height(self, r, theta):
        return (
            np.sin(self.t.get_value())
            * np.cos(self.n.get_value() * theta)
            * special.jv(self.n.get_value(), r * self.last_zero)
        )

    def func(self, u, v):
        r, theta = u, v
        return (
            r * np.cos(theta),
            r * np.sin(theta),
            self.drumhead_height(r, theta)
        )


class Drum(Scene):
    t = ValueTracker(0)
    n = ValueTracker(0)
    k = ValueTracker(1)
    first_zero = 2.40482556  # of order zero (i.e. first partial/fundamental frequency location)

    def construct(self):
        self.setup_bessel()
        self.vibrate_modes()

    def setup_bessel(self):
        frame:OpenGLCamera = self.camera
        frame.set_euler_angles(phi=PI/3)
        self.axes = ThreeDAxes(
            [-1, 1, 1], [-1, 1, 1], [-1, 1, 1], x_length=6, y_length=6, z_length=6
        )
        surface = always_redraw(
            lambda : Bessel(
                self.n,
                self.k,
                self.t
            )
        )
        self.add(surface)


    def vibrate_modes(self):
        frame: OpenGLCamera = self.camera
        target = frame.generate_target()
        target.set_euler_angles(PI/10,PI/3)
        for i in range(4):
            self.n.set_value(i),
            self.t.set_value(0)
            for j in range(1,5):
                self.k.set_value(j),
                self.play(
                    self.t.animate(rate_func=linear).set_value(2 * PI),
                    MoveToTarget(frame, rate_func=there_and_back),
                    run_time=1,
                )

                self.t.set_value(0)
        
        self.embed()

class DrumFundamental(Scene):
    def construct(self):
        f = MathTex("f_{0,1}","=",r"\dfrac{0.765}{d}", r"\sqrt{\dfrac{T}{\sigma}}")
        diameter = Text("Diameter")
        tension = Text("Tension")
        mass = Text("Mass")
        vg1 = VGroup(tension, mass, diameter).arrange(RIGHT, buff=1).shift(UP)
        D = MathTex("f", "\\propto", r"\dfrac{1}{d}").next_to(diameter, DOWN)
        T = (
            MathTex("f", "\\propto", "\\sqrt{T}")
            .next_to(tension, DOWN)
            .shift(0.3 * DOWN)
        )
        M = (
            MathTex("f", "\\propto", "\\sqrt{\dfrac{1}{\sigma}}")
            .next_to(mass, DOWN)
            .shift(0.05 * DOWN)
        )
        vg2 = VGroup(T, M, D)
        self.add(vg1, vg2)
        self.play(Write(vg1), Write(vg2), lag_ratio=.8)
        self.wait()
        self.play(
            Unwrite(D[1]),
            Unwrite(T[1]),
            Unwrite(M[1]),
            Unwrite(diameter),
            Unwrite(tension),
            Unwrite(mass),
            Transform(D[0], f[0]),
            Transform(T[0], f[0]),
            Transform(M[0], f[0]),
            Write(f[1]),
            Transform(D[2], f[2]),
            Transform(T[2], f[3]),
            Transform(M[2], f[3]),
            run_time=2,
            lag_ratio=0.2,
        )
        self.wait()

class WhatsThePoint(MusicScene):
    def construct(self):
        self.setup_modes()
        self.show_the_point()
        self.wait()
    
    def setup_modes(self):
        self.creature.change_mode("giddy")
        self.change_student_modes(*["puzzled", "pondering", "frustrated", "pondering", "erm"])
        self.wait()
        frustrated_student = self.students[2]
        frustrated_student.generate_target()

        self.add_foreground_mobject(frustrated_student)
        self.rect = Rectangle(BLACK, fill_color=BLACK, fill_opacity=1, width=18, height=18)
        self.play(FadeIn(self.rect))
        self.play(
            frustrated_student.animate.to_edge(DR).look_at(ORIGIN)
        )
        self.clear()
        self.student = frustrated_student
        self.creatures = [self.student]
        self.add(frustrated_student)

        self.wait()


    def show_the_point(self):
        self.x = NumberLine(
            # x_range=[1, 5],
            # length=14.2,
            x_range=[1.301029, 4.301029],
            length=13,
            include_ticks=False,
            scaling=LogBase(10),
        )
        custom_ticks = [20, 200, 2000, 20000]
        self.x.ticks = VGroup()
        for t in custom_ticks:
            self.x.ticks.add(self.x.get_tick(t))
        self.x.add(self.x.get_tick_marks())
        self.x.add_labels(
            dict(
                zip(custom_ticks, custom_ticks),
            )
        )
        self.add(self.x)

        x = self.x
        root = 440
        harmonic_trackers = [ValueTracker(i * root) for i in range(1, 31)]
        dots = VGroup(*[Dot(x.n2p(h.get_value())) for h in harmonic_trackers])
        text_labels = VGroup(*[
            MathTex("f_{"+f"{int(i+1)}"+"}", font_size=28/(i+1)**.5).next_to(dots[i], UP) for i in range(len(harmonic_trackers))
        ])
        self.play(
            AnimationGroup(
            FadeIn(dots), Write(text_labels), 
            lag_ratio=.2),
            self.student.animate.change_mode("pondering").look_at(dots) , run_time=3)
        ocatves = [(1, 2), (2,4)]
        fifths = [(2, 2*2**(7/12)), (4, 4*2**(7/12))]
        fourths = [(3, 3*2**(5/12)), (6, 6*2**(5/12))]
        major_thirds = [(4, 4*2**(4/12)), (8, 8*2**(4/12))]
        major_sixth = [(3, 3*2**(9/12)), (6, 6*2**(9/12))]
        intervals = [ocatves, fifths, fourths, major_thirds, major_sixth]
        labels = ["Octaves", "Fifths", "Fourths", "Major 3rd", "Major 6th"]
        braces = VGroup()
        for interval in intervals:
            grouping = VGroup()
            for instance in interval:
                grouping.add(BraceBetweenPoints(x.n2p(instance[0]*root), x.n2p(instance[1]*root), UP).shift(UP*.4))
            braces.add(grouping)  

        for i in range(len(braces)):
            braces[i].add(Text(labels[i]).next_to(
                (braces[i][0].get_center() + braces[i][1].get_center())/2,
                UP
            ))
        for i in range(len(braces)):
            self.play(
                AnimationGroup(
                    FadeOut(braces[i-1]) if i > 0 else Wait(),
                    Write(braces[i]),lag_ratio=.5
                ),
                self.student.animate.change_mode("puzzled").look_at(braces[i]) if i == 1 else Wait(),
                self.student.animate.change_mode("aha").look_at(braces[i]) if i == 3 else Wait(),
                # text_labels.animate(rate_func=there_and_back_with_pause).set_color(),
                # dots.animate(rate_func=there_and_back_with_pause).set_color(),
            )
            self.wait()
        self.play(
            self.student.animate.change_mode("hooray").look_at(self.creature.eyes),
        )

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

class PendulumApprox(Scene):
    def construct(self):
        opacity = .5
        formula = MathTex(
            "T",
            r"\approx",
            r"2\pi \sqrt{\dfrac{L}{g}}",
            r"\left[ \sum_{n=0}^\infty \left( \dfrac{\left(2n\right)!}{2^{2n} \left(n!\right)^2} \right)^2 \sin^{2n} \left(\dfrac{\theta_0}{2}\right) \right]"
        )
        background_rect = SurroundingRectangle(formula[0:3],color=BLACK, fill_color=BLACK, fill_opacity=1).set_opacity(opacity)
        approx = formula[1] 
        formula[3].set_opacity(0).set_color(RED)
        equal = MathTex("=").move_to(approx)
        self.play(FadeIn(background_rect), Write(formula))

        answer = MathTex(r"\approx", "2.477 seconds", r"\quad L=1.52m,g=9.81\dfrac{m}{s^2}").next_to(formula[2])
        self.wait()
        new_background = SurroundingRectangle(VGroup(formula[0:3], answer), color=BLACK, fill_color=BLACK, fill_opacity=1).set_opacity(opacity)
        self.play(
            Transform(background_rect, new_background),
            Write(answer)
        )
        self.add(answer)
        self.wait()


        # Better approximation for ideal pendulum
        error_label = BraceLabel(formula[3], "Circular Error", label_constructor=Text, brace_config={"color":RED})
        error_label.label.set_color(RED)
        new_background = SurroundingRectangle(formula,color=BLACK, fill_color=BLACK, fill_opacity=1).set_opacity(opacity+.25)
        self.play(FadeOut(answer), Transform(background_rect, new_background), Write(error_label), formula[3].animate.set_opacity(1), Transform(approx, equal))
        self.wait()
    
class Takeaway(Scene):
    def construct(self):
        student = Rest(mode="pondering", color=GREY).to_corner(DR)
        b = SVGMobject(MEDIA_DIR + "Bubbles_thought.svg", stroke_width=2) # Really gotta fix ThoughtBubble class
        small_bub = Circle(color=WHITE).scale(.25).next_to(student.get_center() + 2*LEFT+ UP)
        c = b[-1].scale(5)
        self.add(student,small_bub, c)
        self.wait()
        self.play(student.animate.blink(), rate_func=there_and_back)
        self.wait()