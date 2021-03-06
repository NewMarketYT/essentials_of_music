from manim import *

all = ["Video", "VideoSeries"]


class Video(SVGMobject):
    def __init__(self, file_name=r"..\assets\video_icon.svg", color=WHITE):
        super().__init__(file_name)
        self.center()
        self.set(width=5)
        self.set_color(color)


class VideoSeries(VGroup):
    def __init__(self, num_videos=11, color=BLUE):
        videos = [Video(color=color) for i in range(num_videos)]
        super().__init__()
        self.add(*videos)
        self.arrange()
        self.set(width=frame.frame_width - MED_LARGE_BUFF)
