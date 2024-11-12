from pydantic import BaseModel, ConfigDict, Field


class TokenResponseSchema(BaseModel):
    access_token: str = Field(..., description='Access token for authentication')
    refresh_token: str = Field(..., description='Refresh token for generating a new access token')
    token_type: str = Field(default='bearer', description='Type of the token')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                'refresh_token': 'dGhpcy1pcy1hLXRva2VuUzI1NiIsInRLXRv1...',
                'token_type': 'bearer',
            }
        }
    )
