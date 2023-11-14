from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation

# prompt = ("f Frank is preparing to give a presentation on {topic} to {audience_size} people. The presentation will "
#           "last {time} minutes. At the end of the presentation, wants the audience to be able to {audience_outcome}. "
#           "Please create a slide deck for Frank to use, which should include title and content. Please also include "
#           "image recommendations in square brackets, along with a recommendation if the image should be a background "
#           "image or not. Please also include notes for Frank for each slide. Please also include a title slide and "
#           "a thank you slide. Please also include a slide with a list of references.")

prompt = ("f Frank is preparing to give a presentation on {topic} to {audience_size} people. The presentation will "
          "last {time} minutes. At the end of the presentation, wants the audience to be able to {audience_outcome}. "
          "Please create a slide deck for Frank to use, which should include title and content. Please also include "
          "notes for Frank for each slide. Please also include a title slide and "
          "a thank you slide, and ensure that there is content to cover the entire duration. "
          "Finally please also include a slide with a list of references.")


# prompt = prompt.format(topic="Talend", audience_size=250, time=15, audience_outcome="understand the basics of Talend")
# print(prompt)


def slice_presentation(presentation):
    slide_pages = []
    current_slide = []

    for line in presentation.splitlines():
        if line.startswith("Slide"):
            slide_pages.append(current_slide)
            current_slide = []
        else:
            current_slide.append(line)

    return slide_pages


if __name__ == "__main__":
    topic = input("What do you want a presentation on? ")
    audience_size = input("How many people will be in the audience? ")
    time = input("How many minutes will the presentation be? ")
    audience_outcome = input("What do you want the audience to be able to do at the end of the presentation? ")

    prompt = prompt.format(topic=topic, audience_size=audience_size, time=time, audience_outcome=audience_outcome)

    orchestrator = Orchestrator("chat", "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",
                                "gpt-3.5-turbo-1106")

    slide_presentation = slice_presentation(orchestrator.call_large_language_model().get_presentation_slides(prompt))

    # print(slide_presentation)
    powerpoint_presentation = PowerPointPresentation()

    for sections in slide_presentation:
        # Check if there are enough sections before accessing them
        # if len(sections) >= 4:
        if len(sections) >= 1:
            title = sections[0].replace('-', '').strip()
            text = ""
            for line in sections[1: len(sections) - 2]:
                text += line.replace('-', '').strip("") + "\n"
            notes = sections[len(sections) - 2].replace('-', '').strip("")

            powerpoint_presentation.add_slide(1, title=title, text=text, notes=notes)
    # else:
    #     print(f"Skipping incomplete slide data: {sections}")

    # powerpoint_presentation.add_slide(1, title=sections[0], text=sections[1], notes=sections[3])
    # for slide in slide_presentation:
    #     powerpoint_presentation.add_slide(5, slide[0], slide[1], slide[2], slide[3])
    #
    powerpoint_presentation.save("presentation.pptx")
