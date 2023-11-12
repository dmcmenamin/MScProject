from src.orchestration.orchestrator import Orchestrator

prompt = ("f Frank is preparing to give a presentation on {topic} to {audience_size} people. The presentation will "
          "last {time} minutes. At the end of the presentation, wants the audience to be able to {audience_outcome}. "
          "Please create a slide deck for Frank to use, which should include title and content. Please also include "
          "image recommendations in square brackets, along with a recommendation if the image should be a background "
          "image or not. Please also include notes for Frank for each slide. Please also include a title slide and "
          "a thank you slide. Please also include a slide with a list of references.")

prompt = prompt.format(topic="Talend", audience_size=250, time=15, audience_outcome="understand the basics of Talend")
print(prompt)


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


orchestrator = Orchestrator("chat", "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",
                            "gpt-3.5-turbo-1106")

slide_presentation = orchestrator.call_large_language_model().get_presentation_slides(prompt)

print(slice_presentation(slide_presentation))
