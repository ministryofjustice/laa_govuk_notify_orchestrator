from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class Email(BaseModel):
    """
    This is the email request model which defines the structure of a valid request sent to the email endpoint.
    """

    email_address: EmailStr = Field(title="The email address of the reciever.")
    template_id: str = Field(title="The GOV.UK Notify template ID of your email.", min_length=1)
    personalisation: dict = Field(
        title="Object containing the personalisation fields for your GOV.UK Notify template.", default=None
    )
