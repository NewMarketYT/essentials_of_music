from manim import *

all = ["Video", "VideoSeries"]


class Video(SVGMobject):
    def __init__(self, file_name=r"..\assets\video_icon.svg"):
        super().__init__(file_name)
        self.center()
        self.set(width=5, stroke_color=WHITE, stroke_width=0, fill_color=WHITE)


class VideoSeries(VGroup):
    def __init__(self, num_videos=11):
        videos = [Video() for i in range(num_videos)]
        super().__init__()
        self.add(*videos)
        self.arrange()
        width = frame.frame_width - MED_LARGE_BUFF
