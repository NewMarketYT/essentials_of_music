from manim import *

all = ["Video", "VideoSeries"]


class Video(SVGMobject):
    def __init__(self):
        super().__init__(self)
        src = "video_icon.svg"
        SVGMobject(src)
        self.center()
        self.set(width=5, stroke_color=WHITE, stroke_width=0, fill_color=WHITE)


class VideoSeries(VGroup):
    def __init__(self, num_videos=11, gradient_colors=[RED, RED_B], **kwargs):
        videos = [Video() for x in range(self.num_videos)]
        super().__init__(self, *videos, **kwargs)
        self.arrange()
        self.set_width(config.FRAME_WIDTH - config.MED_LARGE_BUFF)
        self.set_color_by_gradient(*self.gradient_colors)
