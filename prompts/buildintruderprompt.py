def buildintruderprompt(level:int, text:str=None):
    return f"""
    An unrecognized person has entered.
    Escalation level: {level}   
    Unrecognized person says: {text}

    respond to the query of the intruder appropriately based on the escalation level. 
    If the escalation level is 1, respond politely asking for identification, purpose of visit be very polite do not detect any harm.
    If the escalation level is 2, respond firmly asking for waiting till the user responds as the user will be notified, mentioning that security has been alerted.
    If the escalation level is 3, respond in a very stern manner asking the intruder to leave immediately, mentioning that a security breach has been detected.


    DO NOT escalate to a higher level unless explicitly instructed. 
    Respond only according to the given level.
"""