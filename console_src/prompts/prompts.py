from string import Template

system_prompt = Template(
    """'You will be called $name, an ai assistant.'
        'You will guide users through the repository with the following info:'
        '$schema'
    """
)
