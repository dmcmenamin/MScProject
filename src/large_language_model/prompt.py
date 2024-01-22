def prompt_for_llm(presenter_name, topic, audience_size, presentation_length, audience_outcome):
    """ Generates a prompt for the large language model to generate a presentation
    :param presenter_name: The name of the presenter
    :param topic: The topic of the presentation
    :param audience_size: The number of people the presentation will be given to
    :param presentation_length: The length of the presentation in minutes
    :param audience_outcome: A description of what you expect the audience to
                                know or be able to do after the presentation
    :return: A prompt for the large language model to generate a presentation
    """

    # TODO: Clean up Prompt so that TITLE, CONTENT, NOTES are clearly labelled, without proceeding text

    return ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
            "The presentation will last for {presentation_length} minutes. At the end of the presentation, "
            "the audience of {audience_type} will be expected to {audience_outcome}. "
            "Please create a Slide Deck for {presenter_name} to use. "
            "The first page should have a title that is labelled using keyword TITLE: at the start of the line; "
            "which is the title of the topic, and a subtitle that is labelled using keyword SUBTITLE: at the start "
            "of the line, which is the Outcome of the presentation, followed by the presenters name. "
            "Each following Slide should have a clear title, which is identified by the keyword TITLE: at the start "
            "of the line and content which is labelled using the keyword CONTENT: at the start of the line. "
            "Each slide should also have a notes section, which is labelled using the keyword NOTES: at the start "
            "of the line. The notes section should include information on how long to spend on that slide; "
            "where the total at the end of the presentation should add up to {presentation_length}. "
            "In addition the notes section should provide {presenter_name} with a full script on what to talk about "
            "on that slide. Please ensure there is enough content, with a maximum of 3 minutes spend on each slide. "
            "Please also include {no_of_images} image suggestions for the entire presentation, on the slide where that "
            "image would be most relevant. Make sure that the image suggestion is clearly labelled by the keyword "
            "IMAGE_SUGGESTION: at the start of the line, followed by the image suggestion on the same line. "
            "The CONTENT: section of the 2nd last slide should have a small summary of the entire presentation. "
            "And the CONTENT: section of the last slide should have a list of references that were used by "
            "{LLM} to create the presentation.").format(
        presenter_name=presenter_name,
        topic=topic,
        audience_size=audience_size,
        presentation_length=presentation_length,
        audience_outcome=audience_outcome,
        audience_type="a group of medical professionals",
        no_of_images=3,
        LLM="GPT")
