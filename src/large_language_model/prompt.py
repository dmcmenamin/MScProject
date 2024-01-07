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

    return ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
            "The presentation will last {presentation_length} minutes. At the end of the presentation, "
            "the audience will be expected to {audience_outcome}. Create a slide deck for {presenter_name} to use, "
            "which should include title and content. Also include notes for {presenter_name} for each slide. "
            "Ensure that each title slide, content and notes are clearly labelled. Also provide some image "
            "suggestions on a new line on the relevant slides throughout the presentation, identified by keyword "
            "IMAGE_SUGGESTION at the start of the line. In the notes section for each slide, provide a detailed "
            "explanation on what that slide contains, ensuring it covers the full content on what the presenter should "
            "talk about. Please also provide information on the time that the presenter should spend on each slide, "
            "and ensure that the total time adds up to {presentation_length}."
            "For the final slide, provide a summary of the presentation, and also provide a list of references that "
            "the presenter can use to find out more information on the topic.").format(
        presenter_name=presenter_name,
        topic=topic,
        audience_size=audience_size,
        presentation_length=presentation_length,
        audience_outcome=audience_outcome)