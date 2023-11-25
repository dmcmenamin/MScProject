import re

from pptx import Presentation

# Define constants for slide layouts
SLIDE_TITLE_LAYOUT = 0
SLIDE_TITLE_AND_CONTENT_LAYOUT = 1
SLIDE_SECTION_HEADER_LAYOUT = 2
SLIDE_TWO_CONTENT_LAYOUT = 3
SLIDE_COMPARISON_LAYOUT = 4
SLIDE_TITLE_ONLY_LAYOUT = 5
SLIDE_BLANK_LAYOUT = 6
SLIDE_CONTENT_WITH_CAPTION_LAYOUT = 7
SLIDE_PICTURE_WITH_CAPTION_LAYOUT = 8


# PowerPointPresentation class
# This class is used to create a PowerPoint presentation
# It uses the python-pptx library to create a presentation
# The class has methods to add slides, save the presentation and get slides
# The class also has methods to get a slide layout, and get a slide by slide number
class PowerPointPresentation:

    # Initialise the class
    def __init__(self, presentation_string=None):
        if presentation_string:
            self.presentation = Presentation()
            self.populate_presentation(presentation_string)
        else:
            self.presentation = Presentation()

    # Return a string representation of the class
    def __str__(self):
        return f"PowerPointPresentation(presentation={self.presentation})"

    # Private Method to slice a presentation into slides
    # Inputs: presentation
    # presentation is a string - Raises ValueError if presentation is empty
    # Returns a list of slides
    def __slice_presentation(self, presliced_presentation):
        if not presliced_presentation:
            raise ValueError("Presentation cannot be empty.")
        else:
            sliced_presentation = []

            for presentation_line in presliced_presentation.splitlines():
                if presentation_line.startswith("Slide"):
                    # If the presentation line starts with Slide, then it is the start of a new slide
                    # Add the line to the sliced presentation as a new slide, including a new line, so it can be
                    # formatted correctly. Done via regex to replace "Slide x:" with "Title:"
                    slide_title = re.sub(r"Slide \d+:", "Title:", presentation_line)
                    sliced_presentation.append(slide_title + "\n")
                else:
                    # Otherwise, it is part of the previous slide
                    # Add the line to the previous slide, including a new line, so it can be formatted correctly
                    sliced_presentation[-1] += presentation_line + "\n"

            return sliced_presentation

    # Private Method to get slide content
    # Inputs: slide_pages
    # slide_pages is a list of slides - Raises ValueError if slide_pages is empty
    # Returns a title, subtitle, content and notes for each slide
    def __get_slide_content(self, slide_pages):
        if not slide_pages:
            raise ValueError("Slide pages cannot be empty.")
        else:
            slide_title = ""
            slide_subtitle = ""
            slide_content = ""
            slide_notes = ""
            slide_image = ""
            last_section = ""
            for section in slide_pages.splitlines():
                if len(section) >= 1:
                    if section.startswith("Title:"):
                        slide_title = section.replace("Title:", "").strip()
                    elif section.startswith("Subtitle:"):
                        slide_subtitle = section.replace("Subtitle:", "").strip()
                    elif section.startswith("Content:"):
                        slide_content = section.replace("Content:", "").replace("-", "").strip() + "\n"
                        if "(No content required)".lower() in slide_content.lower():
                            slide_content = ""
                        last_section = "Content"
                    elif section.startswith("Notes"):
                        slide_notes = section.strip() + " \n"
                        last_section = "Notes"
                    elif section.startswith("Image:"):
                        slide_image += section.replace("Image:", "").strip()
                    elif last_section == "Content":
                        slide_content += section.replace("-", "").strip() + "\n"
                    elif last_section == "Notes":
                        slide_notes += section.strip() + "\n"
            return slide_title, slide_subtitle, slide_content, slide_notes, slide_image

    # Private Method to set the slide layouts
    # Inputs: None
    # Returns the best slide layout for the presentation
    def __set_layouts(self, title, subtitle, content, image, notes):
        if title and subtitle:
            return SLIDE_TITLE_LAYOUT
        elif image:
            return SLIDE_PICTURE_WITH_CAPTION_LAYOUT
        elif title and content:
            return SLIDE_TITLE_AND_CONTENT_LAYOUT
        elif title:
            return SLIDE_TITLE_ONLY_LAYOUT
        elif content:
            return SLIDE_CONTENT_WITH_CAPTION_LAYOUT
        else:
            return SLIDE_BLANK_LAYOUT

    # Populate the presentation with content
    # Inputs: title, subtitle, content, image, notes
    # title is a string - defaults to None
    # subtitle is a string - defaults to None
    # content is a string - defaults to None
    # image is a string - defaults to None
    # notes is a string - defaults to None
    # Returns the populated presentation
    def populate_presentation(self, input_presentation):
        sliced_presentation = self.__slice_presentation(input_presentation)
        for section in sliced_presentation:

            if len(section) == 0:
                continue
            title, subtitle, content, notes, image = self.__get_slide_content(section)
            self.add_slide(title=title, subtitle=subtitle, text=content, notes=notes, image=image)

    # Add a slide to the presentation
    # Inputs: slide_layout, title, text, image, notes
    # slide_layout is an integer between 0 and 8 - Raises ValueError if slide_layout is not between 0 and 8
    #               or not an integer
    # title is a string - defaults to None
    # text is a string - defaults to None
    # image is a string - defaults to None - Raises ValueError if image is not provided for picture with caption layout
    # notes is a string - defaults to None
    # Returns the created slide
    def add_slide(self, title=None, subtitle=None, text=None, image=None, notes=None):
        # if slide_layout not in range(0, 9):
        #     raise ValueError("Slide layout must be between 0 and 8.")
        # elif not isinstance(slide_layout, int):
        #     raise ValueError("Slide layout must be an integer.")

        slide_layout = self.__set_layouts(title, subtitle, text, image, notes)

        created_slide = self.presentation.slides.add_slide(self.presentation.slide_layouts[slide_layout])
        if slide_layout == SLIDE_PICTURE_WITH_CAPTION_LAYOUT:
            if image:
                # created_slide.shapes.add_picture(image, top=50, left=50, height=300, width=300)
                # created_slide.shapes.add_textbox(left=50, top=350, width=300, height=50).text = text
                created_slide.placeholders[1].insert_picture(image)
            else:
                raise ValueError("Image must be provided for picture with caption layout.")
            if title:
                created_slide.shapes.title.text = title
            if text:
                created_slide.placeholders[2].text = text
        else:
            if title:
                created_slide.shapes.title.text = title
            if subtitle:
                created_slide.placeholders[1].text = subtitle
            if text:
                created_slide.placeholders[1].text = text
        if notes:
            created_slide.notes_slide.notes_text_frame.text = notes
        return created_slide

    # Save the presentation
    # Inputs: filename
    # filename is a string - Raises ValueError if filename is empty or does not end with .pptx
    # Returns the saved presentation
    def save(self, filename):
        if not filename:
            raise ValueError("Filename cannot be empty.")
        elif not filename.endswith(".pptx"):
            raise ValueError("Filename must end with .pptx")
        else:
            return self.presentation.save(filename)

    # Get a slide layout
    # Inputs: slide_layout
    # slide_layout is an integer between 0 and 8 - Raises ValueError if slide_layout is not between 0 and 8 or not an
    #               integer
    # Returns the slide layout
    def get_slide_layout(self, slide_layout):
        if slide_layout not in range(0, 9):
            raise ValueError("Slide layout must be between 0 and 8.")
        elif not isinstance(slide_layout, int):
            raise ValueError("Slide layout must be an integer.")
        else:
            return self.presentation.slide_layouts[slide_layout]

    # Get a slide by slide number
    # Inputs: slide_number
    # slide_number is an integer - Raises ValueError if slide_number is not an integer
    # Returns the slide
    def get_slide(self, slide_number):
        if not isinstance(slide_number, int):
            raise ValueError("Slide number must be an integer.")
        elif slide_number < 0 or slide_number > len(self.presentation.slides):
            raise ValueError("Slide number must be between 0 and the number of slides in the presentation.")
        else:
            return self.presentation.slides[slide_number]

    # Get all slides in the presentation
    # Returns all slides in the presentation
    def get_slides(self):
        return self.presentation.slides


if __name__ == '__main__':
    ppt = PowerPointPresentation()
    ppt.add_slide(SLIDE_TITLE_LAYOUT, "Slide 1", "Slide 1 Text", notes="This is presenter notes")
    ppt.add_slide(SLIDE_TITLE_AND_CONTENT_LAYOUT, "Slide 2", "Slide 2 Text")
    ppt.add_slide(SLIDE_PICTURE_WITH_CAPTION_LAYOUT, image="D:\\Code\\Python\\MScProject"
                                                           "\\tests\\unit\\powerpointTests\\img.png")
    ppt.save('../../test.pptx')
