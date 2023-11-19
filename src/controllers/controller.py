from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation

# prompt = ("f Frank is preparing to give a presentation on {topic} to {audience_size} people. The presentation will "
#           "last {time} minutes. At the end of the presentation, wants the audience to be able to {audience_outcome}. "
#           "Please create a slide deck for Frank to use, which should include title and content. Please also include "
#           "image recommendations in square brackets, along with a recommendation if the image should be a background "
#           "image or not. Please also include notes for Frank for each slide. Please also include a title slide and "
#           "a thank you slide. Please also include a slide with a list of references.")

prompt = ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
          "The presentation will last {time} minutes. At the end of the presentation, wants the audience to be "
          "able to {audience_outcome}. Please create a slide deck for {presenter_name} to use, which should "
          "include title and content. Please also include notes for {presenter_name} for each slide. "
          "Please also ensure that each title slide, content and notes are clearly labelled. Finally please also "
          "include a slide with a list of references.")


def slice_presentation(presentation):
    slide_pages = []
    current_slide = []

    for presentation_line in presentation.splitlines():
        if presentation_line.startswith("Slide"):
            slide_pages.append(current_slide)
            current_slide = []
        else:
            current_slide.append(presentation_line)

    return slide_pages


def get_slide_sections(slide_sections):
    slide_title = ""
    slide_subtitle = ""
    slide_content = ""
    slide_notes = ""
    last_section = ""
    for section in slide_sections:
        if len(section) >= 1:
            if section.startswith("Title:"):
                slide_title = section.replace("Title:", "").strip()
            elif section.startswith("Subtitle:"):
                slide_subtitle = section.replace("Subtitle:", "").strip()
            elif section.startswith("Content:"):
                slide_content = section.replace("Content:", "").replace("-", "").strip() + "\n"
                last_section = "Content"
            elif section.startswith("Notes"):
                slide_content = slide_content.strip() + " \n"
                last_section = "Notes"
            elif last_section == "Content":
                slide_content += section.replace("-", "").strip() + "\n"
            elif last_section == "Notes":
                slide_notes += section.strip() + "\n"
    return slide_title, slide_subtitle, slide_content, slide_notes


if __name__ == "__main__":
    presenter_name = input("What is the name of the presenter? ")
    topic = input("What do you want a presentation on? ")
    audience_size = input("How many people will be in the audience? ")
    time = input("How many minutes will the presentation be? ")
    audience_outcome = input("What do you want the audience to be able to do at the end of the presentation? ")

    prompt = prompt.format(presenter_name=presenter_name,
                           topic=topic, audience_size=audience_size, time=time, audience_outcome=audience_outcome)

    orchestrator = Orchestrator("chat", "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",
                                "gpt-3.5-turbo-1106")

    slide_presentation = slice_presentation(orchestrator.call_large_language_model().get_presentation_slides(prompt))

    # output slide_presentation to a file
    with open(topic + '.txt', 'w') as f:
        for item in slide_presentation:
            f.write("%s\n" % item)

    print(slide_presentation)
    powerpoint_presentation = PowerPointPresentation()

    for sections in slide_presentation:

        if len(sections) == 0:
            continue
        title, subtitle, content, notes = get_slide_sections(sections)

        if title and subtitle:
            powerpoint_presentation.add_slide(0, title=title, text=subtitle, notes=notes)
        elif title and content:
            powerpoint_presentation.add_slide(1, title=title, text=content, notes=notes)
        elif title:
            powerpoint_presentation.add_slide(0, title=title, notes=notes)
        elif content:
            powerpoint_presentation.add_slide(1, text=content, notes=notes)
        else:
            powerpoint_presentation.add_slide(0, title="Slide", notes=notes)

    powerpoint_presentation.save(topic + ".pptx")
