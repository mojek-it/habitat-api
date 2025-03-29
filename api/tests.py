import pytest
from django.urls import reverse

from petitions.models import Petition, PetitionSignature
from api.schemas.petitions import (
    PetitionBase,
    PetitionCreate,
    PetitionUpdate,
    PetitionResponse,
    PetitionSignatureBase,
    PetitionSignatureCreate,
    PetitionSignatureResponse,
)


@pytest.mark.django_db
class TestAPISchemas:
    """Tests for API schemas"""

    def test_petition_schema_validation(self):
        """Test validation for petition schemas"""
        # Valid data
        valid_data = {
            "name": "Test Petition",
            "target": 100,
            "email_subject": "Thank you for signing",
            "email_content": "Thank you for supporting our cause.",
        }

        # Create a PetitionCreate instance
        petition_create = PetitionCreate(**valid_data)
        assert petition_create.name == "Test Petition"
        assert petition_create.target == 100
        assert petition_create.email_subject == "Thank you for signing"
        assert petition_create.email_content == "Thank you for supporting our cause."

        # Invalid data - name too short
        with pytest.raises(ValueError):
            PetitionCreate(
                name="AB",  # Too short (min_length=3)
                target=100,
                email_subject="Thank you for signing",
                email_content="Thank you for supporting our cause.",
            )

        # Invalid data - target must be > 0
        with pytest.raises(ValueError):
            PetitionCreate(
                name="Test Petition",
                target=0,  # Invalid (gt=0)
                email_subject="Thank you for signing",
                email_content="Thank you for supporting our cause.",
            )

    def test_petition_signature_schema_validation(self):
        """Test validation for petition signature schemas"""
        # Valid data
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "email_consent": True,
            "phone_consent": False,
        }

        # Create a PetitionSignatureCreate instance
        signature_create = PetitionSignatureCreate(**valid_data)
        assert signature_create.first_name == "John"
        assert signature_create.last_name == "Doe"
        assert signature_create.email == "john.doe@example.com"
        assert signature_create.phone_number == "+1234567890"
        assert signature_create.email_consent is True
        assert signature_create.phone_consent is False

        # Invalid data - invalid email
        with pytest.raises(ValueError):
            PetitionSignatureCreate(
                first_name="John",
                last_name="Doe",
                email="not-an-email",  # Invalid
                phone_number="+1234567890",
            )

        # Invalid data - phone number too short
        with pytest.raises(ValueError):
            PetitionSignatureCreate(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone_number="123",  # Too short (min_length=5)
            )
