from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=False)

    user = relationship('User', back_populates='referral_code')

    def is_active(self) -> bool:
        """Checks if the referral code is active."""

        return datetime.now(tz=timezone.utc) < self.expiry_date

    def extend_expiry(self, days: int) -> None:
        """
        Extend the validity period of the code for the
        specified number of days.
        """

        self.expiry_date += timedelta(days=days)

    def deactivate(self) -> None:
        """
        Deactivates the code by setting expiry_date
        to the current date.
        """

        self.expiry_date = datetime.now(tz=timezone.utc)
