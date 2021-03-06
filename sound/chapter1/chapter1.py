from manim import *
from sound import *


class NewMarketLogo(GraphScene, MovingCameraScene):
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.axes_color = BLACK
        self.x_min = -3
        self.x_max = 3
        self.y_min = -3
        self.y_max = 3
        self.x_axis_width = 6
        self.y_axis_height = 6
        self.graph_origin = np.array([0, 0, 0])
        self.x_axis_label = ""
        self.y_axis_label = ""
        self.camera_frame.save_state()
        self.setup_axes(animate=False)

        def stock_curve(x):
            return (x - 0.125) ** 4 * (x + 1.875)

        graph = self.get_graph(stock_curve, color=BLUE, x_min=-4, x_max=3)
        deriv_graph = self.get_derivative_graph(graph)
        dolly = self.get_graph(stock_curve, color=BLACK, x_min=-3, x_max=0)

        def candlesticks(x):
            coord = self.input_to_graph_point(x, graph)
            before_coord = self.input_to_graph_point(x - 0.45, graph)
            after_coord = self.input_to_graph_point(x + 0.45, graph)
            deriv_coord = self.input_to_graph_point(x, deriv_graph)
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
        self.camera_frame.scale(0.5).move_to(moving_dot)
        self.add(self.camera_frame)

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera_frame.add_updater(update_curve)
        candles = VGroup(*sticks)
        logo = SVGMobject("newmarket.svg").scale(0.5).move_to(0.5 * UP)
        logo.submobjects[0].set(stroke_width=0)
        logo.submobjects[1].set(stroke_width=0)
        self.play(
            AnimationGroup(
                MoveAlongPath(moving_dot, dolly, rate_func=smooth, run_time=3),
                Write(graph, run_time=2.5, rate_func=rush_into),
                Write(candles, run_time=4),
            ),
            Write(logo, run_time=3, rate_func=rush_into),
        )
        self.camera_frame.remove_updater(update_curve)

        self.play(
            AnimationGroup(
                Uncreate(graph),
                Uncreate(candles),
                logo.animate.shift(0.15 * DOWN),
                logo.submobjects[2].animate.set_fill(BLACK).shift(0.15 * DOWN),
            ),
            self.camera_frame.animate.scale(0.005),
        )
        self.wait()


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

        l1 = Line(LEFT, RIGHT, stroke_width=8).scale(6).move_to(line, RIGHT)
        l2 = Line(LEFT, RIGHT, stroke_width=8).scale(6).move_to(line1, RIGHT)
        l3 = Line(LEFT, RIGHT, stroke_width=8).scale(6).move_to(line2, RIGHT)
        l4 = Line(LEFT, RIGHT, stroke_width=8).scale(6).move_to(line3, RIGHT)
        l5 = Line(LEFT, RIGHT, stroke_width=8).scale(6).move_to(line4, RIGHT)
        colored_words = VGroup(l1, l2, l3, l4, l5).move_to(ORIGIN)
        self.play(ReplacementTransform(quote, colored_words))
        self.play(colored_words.animate.set(width=frame.frame_width).shift(DOWN))


class Introduction(MusicScene):
    def __init__(self):
        super().__init__(GREY_BROWN)

    def construct(self):
        self.show_series()
        # self.show_many_facts()
        # self.create_music()

    def show_series(self):
        words = Tex("Welcome to \\\\", "Essentials of Music")
        words.set_color_by_tex("Essentials of Music", YELLOW)
        self.teacher.change_mode("happy")
        self.play(
            Blink(self.get_teacher()),
        )
        self.teacher_says(words, target_mode="hooray")
        essence_words = words.get_part_by_tex("Essentials").copy()
        self.play(
            AnimationGroup(
                FadeOut(self.teacher.bubble),
                FadeOut(self.teacher.bubble.content),
                essence_words.animate.move_to(ORIGIN+UP),
                lag_ratio=.2
            )
        )

        series = VideoSeries(num_videos=5)
        series.to_edge(UP)
        this_video = series[0]
        this_video.set_color(YELLOW)
        this_video.save_state()
        this_video.set_fill(opacity=0)
        this_video.center()
        this_video.set(height=config.frame_height)
        self.this_video = this_video
        self.play(
            FadeIn(series, run_time=2),
        )
        self.change_student_modes(
            *["hooray"] * 4,
            look_at_arg=series[1].get_left(),
            added_anims=[
                ApplyMethod(this_video.restore, run_time=3),
            ]
        )
        self.play(
            *[
                ApplyMethod(
                    video.shift,
                    0.5 * video.height * DOWN,
                    run_time=3,
                    rate_func=squish_rate_func(there_and_back, alpha, alpha + 0.3),
                )
                for video, alpha in zip(series, np.linspace(0, 0.7, len(series)))
            ]
        )

        self.play(
            *[ApplyMethod(pi.change_mode, "pondering") for pi in self.get_creatures()]
        )
        self.wait()

        self.series = series
        self.essence_words = essence_words

    # def show_many_facts(self):
    #     myTemplate = TexTemplate()
    #     myTemplate.add_to_preamble(r"\usepackage{musicography}")
    #     cof = ImageMobject("assets/Circle_of_fifths_deluxe_4.png")
    #     timesig = TexMobject(r"\musMeter{4}{4}", ",",
    #                         r"\musMeter{6}{8}", ",",
    #                         r"\musMeter{15}{16}", ",",
    #                         r"\musMeter{7}{12}", tex_template= myTemplate)
    #     doremi = TextMobject("Do", ", ", "Re", ", ", "Mi...")
    #     audio = SVGMobject("assets/Audio.svg", fill_opacity=0, stroke_width=10).set_fill()
    #     audio.submobjects[0].set_fill(opacity=1)
    #     rules = [timesig, doremi, cof, audio]
    #     video_indices = [3, 1, 2, 4]
    #     for rule in rules:
    #         rule.next_to(self.teacher.get_corner(UP+LEFT), UP)
    #         rule.shift_onto_screen()
    #     cof.shift
    #     student_index = 1
    #     student = self.get_students()[student_index]
    #     self.change_student_modes(
    #         "pondering", "sassy", "pondering",
    #         look_at_arg = self.teacher.eyes,
    #         added_anims = [
    #             self.teacher.change_mode, "plain"
    #         ]
    #     )
    #     self.wait()
    #     self.play(
    #         FadeIn(rules[0]),
    #         self.teacher.change_mode, "raise_right_hand",
    #     )
    #     self.wait()
    #     alt_rules_list = list(rules[1:]) + [VectorizedPoint(self.teacher.eyes.get_top())]
    #     for last_rule, rule, video_index in zip(rules, alt_rules_list, video_indices):
    #         video = self.series[video_index]
    #         if (type(rule) == TexMobject or type(rule) == TextMobject):
    #             self.play(
    #                 last_rule.move_to, video,
    #                 Write(rule, run_time=3),
    #             )
    #         else:
    #             self.play(
    #                 last_rule.move_to, video,
    #                 FadeIn(rule),
    #             )

    #         self.wait()

    # def create_music(self):
    #     student = self.get_students()[1]
    #     students = self.get_students()
    #     students.remove(student)
    #     student_copies = students.copy()
    #     self.remove(students)
    #     self.add(student_copies)

    #     music = VGroup(*self.essence_words[-len("music"):])
    #     music.generate_target()
    #     create = TextMobject("Create")
    #     create_music = VGroup(create, music.target)
    #     create_music.arrange(RIGHT, buff = MED_SMALL_BUFF)
    #     create_music.next_to(student, UP, 1.5*LARGE_BUFF)
    #     create_music.shift(RIGHT)

    #     fader = Rectangle(
    #         width = config["frame_width"],
    #         height = config["frame_height"],
    #         stroke_width = 0,
    #         fill_color = BLACK,
    #         fill_opacity = 0.5,
    #     )

    #     self.play(
    #         FadeIn(fader),
    #         Animation(student),
    #         Animation(music)
    #     )
    #     self.play(
    #         Write(create),
    #         MoveToTarget(music),
    #         student.change_mode, "erm",
    #         student.look_at, music
    #     )
    #     arrow = Arrow(music, student)
    #     arrow.set_color(color=YELLOW_C)
    #     self.play(ShowCreation(arrow))
    #     self.wait(2)


# class WhatsInStore(Scene):
#     def construct(self):
#             frame = Rectangle(height = 9, width = 16, color = WHITE)
#             frame.set_height(1.5*config["frame_y_radius"])

#             colors = iter(color_gradient([BLUE, YELLOW], 3))
#             titles = [
#                 TextMobject("Chapter %d:"%d, s).to_edge(UP).set_color(next(colors))
#                 for d, s in [
#                     (2, "Divisions of Sound"),
#                     (3, "Harmony and Unharmony"),
#                     (4, "Limits"),
#                 ]
#             ]
#             title = titles[0]

#             frame.next_to(title, DOWN)

#             self.add(frame, title)
#             self.wait(3)
#             for next_title in titles[1:]:
#                 self.play(Transform(title, next_title))
#                 self.wait(3)

# class Keyboard(VGroup):
#     def __init__(self, number_of_keys, start, **kwargs):
#         VGroup.__init__(self, **kwargs)
#         if (number_of_keys <=0):
#             raise Exception("Number of keys must be positive")
#         self.number_of_keys = int(number_of_keys)
#         keys_to_start_index = {"c": 0,
#                                "c#": 1,
#                                "dflat": 1,
#                                "d": 2,
#                                "d#": 3,
#                                "eflat": 3,
#                                "e": 4,
#                                "fflat": 4,
#                                "e#": 5,
#                                "f": 5,
#                                "f#": 6,
#                                "gflat": 6,
#                                "g": 7,
#                                "g#": 8,
#                                "aflat": 8,
#                                "a": 9,
#                                "a#": 10,
#                                "bflat": 10,
#                                "b": 11,
#                                "b#": 0,
#                                }
#         self.start = keys_to_start_index[start.lower()]
#         white_keys = set([0,2,4,5,7,9,11])
#         black_keys = set([1,3,6,8,10])
#         prev_white_key = Point()
#         counter = 0
#         black_keys = []
#         while True:
#             rectangle = None
#             if ((counter+self.start)%12 in white_keys):
#                 big_rectangle = Rectangle(height = 1, width=.2, stroke_opacity=1).next_to(prev_white_key, .1*RIGHT).set_fill(WHITE, 1)
#                 prev_white_key = big_rectangle
#                 self.add(prev_white_key)
#             else:
#                 black_key = None
#                 if(type(prev_white_key) == Point):
#                     black_key = Rectangle(height=2/3., width=.125, color=BLACK, stroke_opacity=1)\
#                     .move_to(prev_white_key.get_center()+.02*RIGHT + .25*UP - 1/12.*UP)\
#                     .set_fill(BLACK, 1)
#                 else:
#                     black_key = Rectangle(height=2/3., width=.125, color=BLACK, stroke_opacity=1)\
#                     .move_to(prev_white_key.get_center()+.1125*RIGHT + .25*UP - 1/12.*UP)\
#                     .set_fill(BLACK, 1)
#                 black_keys.append(black_key)
#             if counter >= self.number_of_keys:
#                 break
#             counter += 1
#         self.add(*black_keys)
#         self.center()
#         background = Rectangle(width=self.get_width(), height=1.1, color=GREY,stroke_opacity=0).set_fill(GREY, 1)
#         self.get_width()
#         self.submobjects.insert(0, background)

# class MindAndHand(Scene):
#     CONFIG={
#         "theta1": PI/2,
#         "theta2": PI/2
#         }
#     def construct(self):

#         hand = SVGMobject("Hand.svg")
#         mind = SVGMobject("Mind.svg")
#         self.add(mind)
#         self.play(DrawBorderThenFill(mind))
#         self.wait()
#         self.add(hand)
#         hand.scale(3)
#         hand.shift(LEFT*.30, UP*.5)
#         self.play(FadeIn(hand))
#         self.wait()
#         self.remove(hand,mind)
#         theta1 = ValueTracker(self.theta1)
#         theta2 = ValueTracker(self.theta2)
#         minute_hand = Line(ORIGIN, UP*2, color=YELLOW)
#         hour_hand = Line(ORIGIN, UP*1.5, color=BLUE)
#         self.add(minute_hand, hour_hand)
#         self.play(AnimationGroup(
#             FadeOut(hand),
#             FadeIn(hour_hand),
#             ReplacementTransform(mind, minute_hand),
#             ))
#         self.wait()
#         keyboard = Keyboard(24,"d#").scale(2)
#         minute_hand.add_updater(lambda m: m.set_angle(theta1.get_value()))
#         hour_hand.add_updater(lambda m: m.set_angle(theta2.get_value()))
#         self.play(theta1.increment_value, -48*PI,
#                   theta2.increment_value, -4*PI,
#                   minute_hand.set_opacity, 0,
#                   rate_func = rush_into,
#                   run_time = 10)
#         hour_hand.clear_updaters()
#         self.remove(minute_hand)
#         self.add(keyboard.set_opacity(0))
#         self.play(AnimationGroup(Transform(hour_hand, keyboard),
#                   DrawBorderThenFill(keyboard.set_opacity(1))),
#                   lag_ratio=.5)
#         self.remove(hour_hand)
#         self.wait()
#         self.play(FadeOut(keyboard))
#         self.remove(keyboard)
#         you = quarter_creature.Quarter()
#         self.add(you)
#         self.play(FadeIn(you))
#         self.wait()
#         self.play(creature_animations.Blink(you))
#         self.wait()
#         self.play(you.change,"pondering")

# def inverse_power_law(maxint, scale, cutoff, exponent):
#     return (lambda r: maxint * (cutoff / (r / scale + cutoff))**exponent)

# def inverse_square(maxint, scale, cutoff):
#     return inverse_power_law(maxint, scale, cutoff, 2)

# class SoundIndicator(VMobject):
#     CONFIG = {
#         "radius": 0.5,
#         "intensity": 0,
#         "opacity_for_unit_intensity": 1,
#         "precision": 3,
#         "measurement_point": ORIGIN,
#         "sound_source": None
#     }

#     def generate_points(self):
#         self.background = Circle(color=GREEN, radius = self.radius)
#         self.background.set_fill(opacity=1.0)
#         self.foreground = Circle(color=ORANGE, radius = self.radius)
#         self.foreground.set_stroke(color=WHITE,width=.5)
#         self.add(self.background, self.foreground)

#     def set_intensity(self, new_int):
#         self.intensity = new_int
#         new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
#         self.foreground.set_fill(opacity=new_opacity)
#         ChangeDecimalToValue(self.reading, new_int).update(1)
#         return self

#     def get_measurement_point(self):
#         if self.measurement_point != None:
#             return self.measurement_point
#         else:
#             return self.get_center()

#     def measured_intensity(self):
#         distance = get_norm(self.get_measurement_point() -
#             self.sound_source.get_source_point())
#         intensity = self.sound_source.opacity_function(distance) / self.opacity_for_unit_intensity
#         return intensity

#     def update_mobjects(self):
#         if self.sound_source == None:
#             print("Indicator cannot update, reason: no sound source found")
#         self.set_intensity(self.measured_intensity())

# class Restore(ApplyMethod):
#     def __init__(self, mobject, **kwargs):
#         super().__init__(mobject.restore, **kwargs)


# class EmitWaveAtPoint(Animation):
#     CONFIG = {
#         "small_radius": 0.0,
#         "big_radius": 5,
#         "start_stroke_width": 8,
#         "color": BLUE,
#         "lag_ratio": .1,
#         "rate_func": linear,
#     }
#     def __init__(self, source, **kwargs):
#         digest_config(self, kwargs)
#         self.source = source
#         self.mobject = Circle(
#             radius=self.big_radius,
#             stroke_color=self.color,
#             stroke_width=self.start_stroke_width,
#         )
#         self.mobject.move_to(source)
#         def spawn_at_point(mobj, dt):
#             mobj.move_to(self.source)
#             # self.mobject.clear_updaters()

#         self.mobject.add_updater(spawn_at_point)

#     def interpolate_mobject(self, alpha):
#         self.mobject.become(self.starting_mobject)
#         self.mobject.set_width(alpha*self.big_radius)
#         self.mobject.set_stroke(width=(1-alpha)*self.start_stroke_width)


# class EmitWaves(LaggedStart):
#     CONFIG = {
#         "small_radius": 0.0,
#         "big_radius": 5,
#         "n_circles": 2,
#         "start_stroke_width": 8,
#         "color": WHITE,
#         "remover": True,
#         "lag_ratio": 0.6,
#         "run_time": 1,
#         "remover": True,
#     }

#     def __init__(self, focal_point, **kwargs):
#         digest_config(self, kwargs)
#         self.focal_point = focal_point
#         animations = [EmitWaveAtPoint(focal_point) for x in range(self.n_circles)]
#         super().__init__(*animations, **kwargs)


# class IntroduceSound(Scene):
#     def construct(self):
#         sound = Tex("Sound", color=YELLOW)
#         self.add(sound)
#         self.play(
#             FadeIn(sound),
#             EmitWaves(sound)
#         )

#         what_is = Tex("What is")
#         sound.generate_target()
#         question = Tex("?")
#         wis = VGroup(what_is, sound.target)
#         wis.arrange(RIGHT, buff = MED_SMALL_BUFF)
#         wisq = VGroup(wis, question)
#         wisq.arrange(RIGHT, buff = SMALL_BUFF)
#         self.play(
#             LaggedStart(
#                 MoveToTarget(sound),
#                 FadeIn(what_is),
#                 FadeIn(question),
#                 lag_ratio = .25
#             ),
#             EmitWaves(sound),
#         )

# class ShiftAndRotate(Animation):
#     CONFIG = {
#         "axis": OUT,
#         "run_time": 5,
#         "rate_func": smooth,
#         "about_point": None,
#         "about_edge": None,
#     }
#     def __init__(self, mobject, direction, radians,**kwargs):
#         assert(isinstance(mobject, Mobject))
#         digest_config(self, kwargs)
#         self.mobject = mobject
#         self.direction = direction
#         self.radians = radians

#     def interpolate_mobject(self, alpha):
#         self.mobject.become(self.starting_mobject)
#         self.mobject.shift(alpha*self.direction)
#         self.mobject.rotate(
#             alpha * self.radians,
#             axis=self.axis,
#             about_point=self.about_point,
#             about_edge=self.about_edge,
#         )

# class RotationAndMove(Scene):
#     def construct(self):
#         square1, square2 = VGroup(
#                 Square(color=RED), Square(color=BLUE)
#             ).scale(0.5).set_x(-5)

#         reference = DashedVMobject(Line(LEFT*5,RIGHT*5,color=GRAY))
#         self.add(square1,square2,reference)

#         self.play(
#                 # Red square
#                 square1.rotate,3*PI,
#                 square1.move_to, [5,0,0],
#                 # Blue square
#                 ShiftAndRotate(square2, RIGHT*10, 3*PI),
#                 run_time=4
#             )
#         self.wait()

# def get_path_pending(path,proportion,dx=0.001):
#     if proportion < 1:
#         coord_i = path.point_from_proportion(proportion)
#         coord_f = path.point_from_proportion(proportion+dx)
#     else:
#         coord_i = path.point_from_proportion(proportion-dx)
#         coord_f = path.point_from_proportion(proportion)
#     line = Line(coord_i,coord_f)
#     angle = line.get_angle()
#     return angle

# class ShiftAndRotateAlongPath(Animation):
#     CONFIG = {
#         "run_time": 5,
#         "rate_func": smooth,
#         "dx":0.01
#     }
#     def __init__(self, mobject, path,**kwargs):
#         assert(isinstance(mobject, Mobject))
#         digest_config(self, kwargs)
#         self.mobject = mobject
#         self.path = path

#     def interpolate_mobject(self, alpha):
#         self.mobject.become(self.starting_mobject)
#         self.mobject.move_to(
#             self.path.point_from_proportion(alpha)
#         )
#         angle = get_path_pending(self.path,alpha,self.dx)
#         self.mobject.rotate(
#             angle,
#             about_point=self.mobject.get_center(),
#         )

# class MoveAlongPathWithAngle2(Scene):
#     def construct(self):
#         path = Line(LEFT*5, RIGHT*5, stroke_opatity=0.5)
#         path.points[1] += UP * 4
#         path.points[2] += DOWN * 4
#         start_angle = get_path_pending(path, 0)

#         triangle = Triangle().set_height(0.5)
#         triangle.move_to(path.get_start())
#         triangle.rotate(- PI / 2)

#         self.add(triangle,path)
#         self.play(
#                 ShiftAndRotateAlongPath(triangle,path),
#                 run_time=4
#             )
#         self.wait()
