from src.orchestration.orchestrator import Orchestrator


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
                            "gpt-3.5-turbo")

slide_presentation = orchestrator.call_large_language_model().get_presentation_slides("Talend", 250, 15)

print(slice_presentation(slide_presentation))
