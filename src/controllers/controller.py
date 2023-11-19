from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation

# prompt = ("f Frank is preparing to give a presentation on {topic} to {audience_size} people. The presentation will "
#           "last {time} minutes. At the end of the presentation, wants the audience to be able to {audience_outcome}. "
#           "Please create a slide deck for Frank to use, which should include title and content. Please also include "
#           "image recommendations in square brackets, along with a recommendation if the image should be a background "
#           "image or not. Please also include notes for Frank for each slide. Please also include a title slide and "
#           "a thank you slide. Please also include a slide with a list of references.")

prompt = ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
          "The presentation will last {time} minutes. At the end of the presentation, the audience will be expected to "
          "{audience_outcome}. Create a slide deck for {presenter_name} to use, which should "
          "include title and content. Also include notes for {presenter_name} for each slide. "
          "Ensure that each title slide, content and notes are clearly labelled. In the notes section, define how long"
          "the presenter should spend on that slide, ensuring the total time adds up to {time}. Finally please also "
          "include a slide with a list of references.")

if __name__ == "__main__":
    presenter_name = "Darren McMenamin"
    topic = "The importance of Python as a programming language"
    audience_size = "100"
    time = "15"
    audience_outcome = "Understand the importance of Python as a programming language"
    # presenter_name = input("What is the name of the presenter? ")
    # topic = input("What do you want a presentation on? ")
    # audience_size = input("How many people will be in the audience? ")
    # time = input("How many minutes will the presentation be? ")
    # audience_outcome = input("What do you want the audience to be able to do at the end of the presentation? ")

    prompt = prompt.format(presenter_name=presenter_name,
                           topic=topic, audience_size=audience_size, time=time, audience_outcome=audience_outcome)

    orchestrator = Orchestrator("chat", "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",
                                "gpt-3.5-turbo-1106")

    powerpoint_presentation = PowerPointPresentation(
        orchestrator.call_large_language_model().get_presentation_slides(prompt))

    # Save the returns as a text file for debugging purposes
    with open(topic + ".txt", "w") as f:
        f.write(powerpoint_presentation.presentation)

    powerpoint_presentation.save(topic + ".pptx")
