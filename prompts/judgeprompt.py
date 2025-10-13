def judgeprompt(text: str) -> str:
    return f"""
    ### You are an AI assistant that helps to generate concise level number reply only in integer!!.
    Given the following text, extract the key points and generate a set of clear, step-by-step instructions that summarize the main actions.

    Text:
    {text}

    Assign an escalation level from 1 to 3 based on the severity of the situation described in the text.
    level is 1 when user is politely asking for identification, purpose of visit.
    level is 2, when user is repeatedly asking the same question and being rude.
    level is 3, when user is misbehaving and threatening to tamper the system .

    """