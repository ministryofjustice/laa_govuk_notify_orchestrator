class EmailRouter:
    """
    These values are used to document the email endpoint in Swagger and Redocly.
    """

    summary = "Send email to GOV.UK Notify"

    description = """Will queue your email to be sent to GOV.UK Notify,
                if their service is down the email will be held in an encrypted queue until a response is recieved.
                If after two weeks no response is recieved your email be deleted.
                """
