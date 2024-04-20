from unittest import TestCase

from src.powerpoint.presentation import PowerPointPresentation
from src.powerpoint.slide_enum import SlideEnum

title = "Test Title"
subtitle = "Test Subtitle"
text = "Test Text"
notes = "Test Notes"
picture = "./tests/unit/powerpointTests/img.png"


# Test Class for PowerPointPresentation
class Test(TestCase):
    # Set up the test class - runs at the start of every test
    def setUp(self):
        self.presentation = PowerPointPresentation()
        self.test_title = title
        self.test_subtitle = subtitle
        self.test_text = text
        self.test_notes = notes
        self.test_picture = picture

    # Clear down at the end of every test
    def tearDown(self):
        self.presentation = None
        self.test_title = None
        self.test_text = None
        self.test_notes = None
        self.test_image = None

    # Test the Constructor
    def test_constructor(self):
        self.assertIsNotNone(self.presentation)

    # Test the Constructor with no theme
    def test_constructor_with_no_theme(self):
        presentation = PowerPointPresentation("test")
        self.assertIsNotNone(presentation)

    # Test the __str__ method
    def test_str(self):
        self.assertEqual(str(self.presentation), "PowerPointPresentation")

    # Test the _slice_presentation method
    def test__slice_presentation_with_no_input(self):
        with self.assertRaises(ValueError):
            self.presentation._slice_presentation("")

    def test__slice_presentation_without_keyword(self):
        output = self.presentation._slice_presentation("This is a test line")
        expected_output = ["This is a test line\n"]
        self.assertEqual(output, expected_output)

    # Test the _slice_presentation method
    def test__slice_presentation(self):
        output = self.presentation._slice_presentation("slide 1: This is a test line")
        expected_output = ["TITLE: This is a test line\n"]
        self.assertEqual(output, expected_output)

        output = self.presentation._slice_presentation("slide 1: This is a test line\n This is another test line")
        expected_output = ["TITLE: This is a test line\nThis is another test line\n"]
        self.assertEqual(output, expected_output)

        output = self.presentation._slice_presentation("slide 1: This is a test line\n This is another test line\n"
                                                       "slide 2: This is a test line\n This is another test line")
        expected_output = ["TITLE: This is a test line\nThis is another test line\n",
                           "TITLE: This is a test line\nThis is another test line\n"]
        self.assertEqual(output, expected_output)

        output = self.presentation._slice_presentation("Slide 1: This is a test line\n This is another test line\n")
        expected_output = ["TITLE: This is a test line\nThis is another test line\n"]
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method with no input
    def test__get_slide_content_with_no_input(self):
        with self.assertRaises(ValueError):
            self.presentation._get_slide_content("")

    # Test the _get_slide_content method for title
    def test__get_slide_content_for_title(self):
        output = self.presentation._get_slide_content("TITLE: Test Title\n")
        expected_output = "Test Title", "", "", "", ""
        self.assertEqual(output, expected_output)

        output = self.presentation._get_slide_content("Title: Test Title\n - Test Title 2")
        expected_output = "Test Title", "", "", "", ""
        self.assertEqual(output, expected_output)

        output = self.presentation._get_slide_content("Title Test Title\n - Test Title 2\n")
        expected_output = "Test Title", "", "", "", ""
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method for subtitle
    def test__get_slide_content_for_subtitle(self):
        output = self.presentation._get_slide_content("SUBTITLE: Test Subtitle\n")
        expected_output = "", "Test Subtitle", "", "", ""
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method for content
    def test__get_slide_content_for_content(self):
        output = self.presentation._get_slide_content("CONTENT: Test Content")
        expected_output = "", "", "Test Content\n", "", ""
        self.assertEqual(output, expected_output)

        output = self.presentation._get_slide_content("CONTENT: (no content")
        expected_output = "", "", "", "", ""
        self.assertEqual(output, expected_output)

        output = self.presentation._get_slide_content("Content: Test Content\n - Test Content 2")
        expected_output = "", "", "Test Content\nTest Content 2\n", "", ""
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method for notes
    def test__get_slide_content_for_notes(self):
        output = self.presentation._get_slide_content("NOTES: Test Notes")
        expected_output = "", "", "", "Test Notes\n", ""
        self.assertEqual(output, expected_output)

        output = self.presentation._get_slide_content("Notes: Test Notes\n - Test Notes 2")
        expected_output = "", "", "", "Test Notes\nTest Notes 2\n", ""
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method for image
    def test__get_slide_content_for_image(self):
        output = self.presentation._get_slide_content("IMAGE: img.png")
        expected_output = "", "", "", "", "img.png"
        self.assertEqual(output, expected_output)

    # Test the _get_slide_content method for references
    def test__get_slide_content_for_references(self):
        output = self.presentation._get_slide_content("references test information")
        expected_output = "", "", "test information\n", "", ""
        self.assertEqual(output, expected_output)

        # Test the _get_slide_content method for title, subtitle, content, notes and image

    def test__get_slide_content(self):
        output = self.presentation._get_slide_content("TITLE: Test Title\nSUBTITLE: Test Subtitle\n"
                                                      "CONTENT: Test Content\nNOTES: Test Notes\nIMAGE: img.png")
        expected_output = "Test Title", "Test Subtitle", "Test Content\n", "Test Notes\n", "img.png"
        self.assertEqual(output, expected_output)

    # Test the _set_layouts method for title
    def test__set_layouts_title_only(self):
        slide = self.presentation._set_layouts("TITLE: Test Title\n", "", "", "", "")
        self.assertEqual(slide, SlideEnum.SLIDE_TITLE_ONLY_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_AND_CONTENT_LAYOUT.value)

    # Test the _set_layouts method for title and subtitle
    def test__set_layouts_title_and_subtitle(self):
        slide = self.presentation._set_layouts("TITLE: Test Title\n",
                                               "SUBTITLE: Test Subtitle\n", "", "", "")
        self.assertEqual(slide, SlideEnum.SLIDE_TITLE_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_AND_CONTENT_LAYOUT.value)

    # Test the _set_layouts method for picture with caption
    def test__set_layouts_picture_with_caption(self):
        slide = self.presentation._set_layouts("", "", "", "img.png", "")
        self.assertEqual(slide, SlideEnum.SLIDE_PICTURE_WITH_CAPTION_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_AND_CONTENT_LAYOUT.value)

        slide = self.presentation._set_layouts("TITLE: Test Title\n", "SUBTITLE: Test Subtitle\n",
                                               "", "img.png", "img.png")
        self.assertEqual(slide, SlideEnum.SLIDE_PICTURE_WITH_CAPTION_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_LAYOUT.value)

    # Test the _set_layouts method for content and title
    def test__set_layouts_content_and_title(self):
        slide = self.presentation._set_layouts("TITLE: Test Title\n", "",
                                               "CONTENT: Test Content\n", "", "")
        self.assertEqual(slide, SlideEnum.SLIDE_TITLE_AND_CONTENT_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_LAYOUT.value)

    def test__set_layouts_content_only(self):
        slide = self.presentation._set_layouts("", "", "CONTENT: Test Content\n", "", "")
        self.assertEqual(slide, SlideEnum.SLIDE_CONTENT_WITH_CAPTION_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_LAYOUT.value)

    # Test the _set_layouts method for comparison
    def test__set_layouts_notes(self):
        slide = self.presentation._set_layouts("", "", "", "", "Test Notes")
        self.assertEqual(slide, SlideEnum.SLIDE_BLANK_LAYOUT.value)
        self.assertNotEqual(slide, SlideEnum.SLIDE_TITLE_LAYOUT.value)

    # Test the title slide layout, to match the title
    def test_add_slide_with_title(self):
        slide = self.presentation.add_slide(title)
        self.assertEqual(slide.shapes.title.text, self.test_title)

    # Test the title and subtitle slide layout, to match the title and subtitle
    def test_add_slide_with_title_and_subtitle(self):
        slide = self.presentation.add_slide(title=title, subtitle=subtitle)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.placeholders[1].text, self.test_subtitle)

    # Test the title and content slide layout, to match the content
    def test_add_slide_with_text(self):
        slide = self.presentation.add_slide(title=title, text=text)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.placeholders[1].text, self.test_text)

    # Test adding a slide with notes, to match the notes
    def test_add_slide_with_notes(self):
        slide = self.presentation.add_slide(title=title, notes=notes)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.notes_slide.notes_text_frame.text, self.test_notes)

    # Test adding a slide with picture, to match the picture
    def test_add_slide_with_picture(self):
        slide = self.presentation.add_slide(title=title, image=picture, text=text)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.placeholders[2].text, self.test_text)
        self.assertNotEqual(slide.placeholders[2].text, self.test_title)

    # Test adding a slide with a non-existent picture
    def test_add_slide_with_non_existent_picture(self):
        with self.assertRaises(FileNotFoundError):
            self.presentation.add_slide(title=title, image="non_existent_picture.png")

    # Test creating presentation with invalid name
    def test_save_with_invalid_filename(self):
        with self.assertRaises(ValueError):
            self.presentation.save("")

    # Test creating presentation with invalid name type
    def test_save_with_valid_filename(self):
        self.presentation.save("test.pptx")
        self.assertIsInstance(self.presentation, PowerPointPresentation)

    # Test slide layout retrieval
    def test_get_slide_layout(self):
        layout = self.presentation.get_slide_layout(SlideEnum.SLIDE_TITLE_AND_CONTENT_LAYOUT.value)
        self.assertEqual(layout.name, "Title and Content")

    # Test slide layout retrieval with invalid layout
    def test_get_slide_layout_with_invalid_layout(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide_layout(-1)

    # Test slide layout retrieval with invalid layout type
    def test_get_slide_layout_with_invalid_layout_type(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide_layout("string")

    # Test slide retrieval
    def test_get_slide(self):
        slide = self.presentation.add_slide(title)
        retrieved_slide = self.presentation.get_slide(0)
        self.assertEqual(retrieved_slide, slide)

    # Test slide retrieval with invalid slide number
    def test_get_slide_with_invalid_slide_number(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide(-1)

    # Test slide retrieval with invalid slide number type
    def test_get_slide_with_invalid_slide_number_type(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide("string")

    # Test slide retrieval with slide number out of range
    def test_get_slide_with_slide_number_out_of_range(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide(2)

    # Test slide retrieval with slide number out of range type
    def test_get_slide_with_slide_number_out_of_range_type(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide(2.5)

    # Test slide length
    def test_get_slides(self):
        self.presentation.add_slide(title)
        self.presentation.add_slide(title="Slide 2")
        slides = self.presentation.get_slides()
        self.assertEqual(len(slides), 2)

    # Test slide length with no slides
    def test_get_slides_with_no_slides(self):
        slides = self.presentation.get_slides()
        self.assertEqual(len(slides), 0)

    # Test slide length with invalid slide number
    def test_get_slides_with_invalid_information(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide(-1)

        with self.assertRaises(ValueError):
            self.presentation.get_slide("string")
