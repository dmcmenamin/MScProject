from unittest import TestCase
from src.powerpoint.presentation import *


title = "Test Title"
text = "Test Text"
notes = "Test Notes"
picture = "img.png"


# Test Class for PowerPointPresentation
class Test(TestCase):
    # Set up the test class - runs at the start of every test
    def setUp(self):
        self.presentation = PowerPointPresentation()
        self.test_title = title
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

    # Test the title slide layout, to match the title
    def test_add_slide_with_title(self):
        slide = self.presentation.add_slide(SLIDE_TITLE_LAYOUT, title)
        self.assertEqual(slide.shapes.title.text, self.test_title)

    # Test the title and content slide layout, to match the content
    def test_add_slide_with_text(self):
        slide = self.presentation.add_slide(SLIDE_TITLE_AND_CONTENT_LAYOUT, title, text)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.placeholders[1].text, self.test_text)

    # Test the picture with caption slide layout
    # TODO: clean up this test case
    # def test_add_slide_with_image(self, image=picture):
    #     slide = self.presentation.add_slide(SLIDE_PICTURE_WITH_CAPTION_LAYOUT, image)
    #     self.assertEqual(slide.slide_layout.name, self.test_image)

    # Test the picture with caption slide layout with no image
    def test_add_slide_with_no_image(self):
        with self.assertRaises(ValueError):
            self.presentation.add_slide(SLIDE_PICTURE_WITH_CAPTION_LAYOUT)

    # Test adding a slide with notes, to match the notes
    def test_add_slide_with_notes(self):
        slide = self.presentation.add_slide(SLIDE_TITLE_LAYOUT, title=title, notes=notes)
        self.assertEqual(slide.shapes.title.text, self.test_title)
        self.assertEqual(slide.notes_slide.notes_text_frame.text, self.test_notes)

    # Test slide layout retrieval
    def test_get_slide_layout(self):
        layout = self.presentation.get_slide_layout(SLIDE_TITLE_AND_CONTENT_LAYOUT)
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
        slide = self.presentation.add_slide(SLIDE_TITLE_LAYOUT, title)
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
        self.presentation.add_slide(SLIDE_TITLE_LAYOUT, title)
        self.presentation.add_slide(SLIDE_TITLE_LAYOUT, title="Slide 2")
        slides = self.presentation.get_slides()
        self.assertEqual(len(slides), 2)

    # Test slide length with no slides
    def test_get_slides_with_no_slides(self):
        slides = self.presentation.get_slides()
        self.assertEqual(len(slides), 0)

    # Test slide length with invalid slide number
    def test_get_slides_with_invalid_slide_number(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide(-1)

    # Test slide length with invalid slide number type
    def test_get_slides_with_invalid_slide_number_type(self):
        with self.assertRaises(ValueError):
            self.presentation.get_slide("string")

    # Test creating slide with invalid layout
    def test_add_slide_with_invalid_layout(self):
        with self.assertRaises(ValueError):
            self.presentation.add_slide(-1, title)

    # Test creating slide with invalid layout type
    def test_add_slide_with_invalid_layout_type(self):
        with self.assertRaises(ValueError):
            self.presentation.add_slide("string", title)

    # Test creating presentation with invalid name
    def test_save_with_invalid_filename(self):
        with self.assertRaises(ValueError):
            self.presentation.save("")

    # Test creating presentation with missing extension
    def test_save_with_filename_wit_missing_extension(self):
        with self.assertRaises(ValueError):
            self.presentation.save("missing_extension")


