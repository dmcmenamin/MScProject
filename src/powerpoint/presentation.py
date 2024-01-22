from pptx import Presentation
import re


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
    """ PowerPointPresentation class to handle all PowerPoint Presentation API calls
    """

    def __init__(self, presentation_string=None):
        """ Constructor for PowerPointPresentation class
        :param presentation_string: The presentation string
        """
        if presentation_string:
            self.presentation = Presentation()
            self.populate_presentation(presentation_string)
        else:
            self.presentation = Presentation()

    # Return a string representation of the class
    def __str__(self):
        """ Returns the string representation of the PowerPointPresentation class
        :return: The string representation of the PowerPointPresentation class
        """

        return f"PowerPointPresentation(presentation={self.presentation})"

    def _slice_presentation(self, presliced_presentation):
        """ Private Method - returns a sliced presentation
        :param presliced_presentation: The presentation to slice
        :return: The sliced presentation
        :raises ValueError: If the presentation is empty
        """
        if not presliced_presentation:
            raise ValueError("Presentation cannot be empty.")
        else:
            sliced_presentation = []

            for presentation_line in presliced_presentation.splitlines():
                if presentation_line.startswith("Slide"):
                    # If the presentation line starts with Slide, then it is the start of a new slide
                    # Add the line to the sliced presentation as a new slide, including a new line, so it can be
                    # formatted correctly. Done via regex to replace "Slide x:" with "Title:"
                    slide_title = re.sub(r"Slide \d+:", "TITLE:", presentation_line)
                    sliced_presentation.append(slide_title + "\n")
                elif len(sliced_presentation) != 0:
                    # Otherwise, it is part of the previous slide
                    # Add the line to the previous slide, including a new line, so it can be formatted correctly
                    sliced_presentation[-1] += presentation_line + "\n"
                else:
                    # Otherwise, it doesn't start with Slide, but is the first line of the presentation
                    # This may happen on the first slide of the presentation
                    # So set it as the first line in the sliced presentation
                    sliced_presentation.append(presentation_line + "\n")

            return sliced_presentation

    def _get_slide_content(self, slide_pages):
        """ Private Method - returns a title, subtitle, content and notes for each slide - if they exist
        :param slide_pages: The slide pages
        :return: A title, subtitle, content and notes for each slide
        :raises ValueError: If the slide pages are empty
        """
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
                    if section.startswith("TITLE:"):
                        slide_title = section.replace("TITLE:", "").strip()
                    elif section.startswith("SUBTITLE:"):
                        slide_subtitle = section.replace("SUBTITLE:", "").strip()
                    elif section.startswith("CONTENT:"):
                        # If the slide content is "Content:", then set the slide content to the section, without the
                        # "Content:" prefix and the "-" suffix, and strip any whitespace
                        # This is done to ensure that the slide content is not set to "Content:"
                        slide_content = section.replace("CONTENT:", "").replace("-", "") + "\n"
                        # If the slide content is "(No content ", then set the slide content to an empty string
                        # This is done to ensure that the slide content is not set to "(No content required)"
                        if "(No content" in slide_content.lower():
                            slide_content = ""
                        last_section = "Content"
                    elif section.startswith("NOTES"):
                        slide_notes = section.replace("NOTES:", "").strip() + " \n"
                        last_section = "Notes"
                    elif section.startswith("Image:"):
                        slide_image += section.replace("Image:", "").strip()
                    elif last_section == "Content":
                        slide_content += section.replace("-", "").strip() + "\n"
                    elif last_section == "Notes":
                        slide_notes += section.strip() + "\n"
            return slide_title, slide_subtitle, slide_content, slide_notes, slide_image

    def _set_layouts(self, title, subtitle, content, image, notes):
        """ Private Method - returns the best slide layout for the presentation
        :param title: The title of the slide
        :param subtitle: The subtitle of the slide
        :param content: The content of the slide
        :param image: The image of the slide
        :param notes: The notes of the slide
        :return: The best slide layout for the presentation
        """

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

    def populate_presentation(self, input_presentation):
        """ Returns a populated presentation
        :param input_presentation: The input presentation
        :return: The populated presentation
        """
        sliced_presentation = self._slice_presentation(input_presentation)
        for section in sliced_presentation:

            if len(section) == 0:
                continue
            title, subtitle, content, notes, image = self._get_slide_content(section)
            self.add_slide(title=title, subtitle=subtitle, text=content, notes=notes, image=image)

    def add_slide(self, title=None, subtitle=None, text=None, image=None, notes=None):
        """ Returns the created slide
        :param title: The title of the slide
        :param subtitle: The subtitle of the slide
        :param text: The text of the slide
        :param image: The image of the slide
        :param notes: The notes of the slide
        :return: The created slide
        """

        slide_layout = self._set_layouts(title, subtitle, text, image, notes)
        print(slide_layout)
        print(title)
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

    def save(self, filename):
        """ Returns the saved presentation
        :param filename: The filename of the presentation
        :return: The saved presentation
        :raises ValueError: If the filename is empty or does not end with .pptx
        """
        if not filename:
            raise ValueError("Filename cannot be empty.")
        elif not filename.endswith(".pptx"):
            raise ValueError("Filename must end with .pptx")
        else:
            return self.presentation.save(filename)

    def get_slide_layout(self, slide_layout):
        """ Returns the slide layout
        :param slide_layout: The slide layout
        :return: The slide layout
        :raises ValueError: If the slide layout is not between 0 and 8 or not an integer
        """
        if slide_layout not in range(0, 9):
            raise ValueError("Slide layout must be between 0 and 8.")
        elif not isinstance(slide_layout, int):
            raise ValueError("Slide layout must be an integer.")
        else:
            return self.presentation.slide_layouts[slide_layout]

    def get_slide(self, slide_number):
        """ Returns the slide specified by the slide number
        :param slide_number: The slide number
        :return: The slide
        :raises ValueError: If the slide number is not between 0 and the number of slides in the presentation or not
        an integer
        """

        if not isinstance(slide_number, int):
            raise ValueError("Slide number must be an integer.")
        elif slide_number < 0 or slide_number > len(self.presentation.slides):
            raise ValueError("Slide number must be between 0 and the number of slides in the presentation.")
        else:
            return self.presentation.slides[slide_number]

    def get_slides(self):
        """ Returns all slides in the presentation
        :return: All slides in the presentation
        """

        return self.presentation.slides