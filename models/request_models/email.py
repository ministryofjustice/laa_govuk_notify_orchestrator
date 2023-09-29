from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class Email(BaseModel):
    email_address: EmailStr = Field(title="The email address of the reciever.")
    template_id: str = Field(title="The GOV.UK Notify template ID of your email.", min_length=1)
    personalisation: dict = Field(title="Object containing the personalisation fields for your GOV.UK Notify template.", default=None)
