class Slide:

    def __init__(self, slide_layout):
        pass

    def __str__(self):
        return (f"Slide: ")

    def __repr__(self):
        return super().__repr__()

    def create_slide(self, slide_layout):
        pass

    def add_text(self, text):
        pass

    def add_title(self, title):
        pass

    def add_subtitle(self, subtitle):
        pass

    def add_image(self, image_url):
        pass

    def add_chart(self, chart):
        pass

    def add_table(self, table):
        pass

    def add_video(self, video_url):
        pass

    def add_audio(self, audio_url):
        pass

    def add_shape(self, shape):
        pass


slide = Slide()
print(slide)

