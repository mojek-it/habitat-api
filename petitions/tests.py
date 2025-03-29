import pytest
from django.core import mail
from django.db.utils import IntegrityError
from unittest.mock import patch

from .models import Petition, PetitionSignature


@pytest.mark.django_db
class TestPetitionModel:
    """Tests for the Petition model"""

    def test_petition_creation(self):
        """Test creating a petition"""
        petition = Petition.objects.create(
            name="Test Petition",
            target=100,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )
        assert petition.name == "Test Petition"
        assert petition.target == 100
        assert petition.signature_count == 0
        assert petition.email_subject == "Thank you for signing"
        assert petition.email_content == "Thank you for supporting our cause."

    def test_petition_str_representation(self):
        """Test the string representation of a petition"""
        petition = Petition.objects.create(
            name="Test Petition",
            target=100,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )
        assert str(petition) == "Test Petition (0/100)"

        # Update signature count
        petition.signature_count = 50
        petition.save()
        assert str(petition) == "Test Petition (50/100)"


@pytest.mark.django_db
class TestPetitionSignatureModel:
    """Tests for the PetitionSignature model"""

    @pytest.fixture
    def petition(self):
        """Create a petition for testing"""
        return Petition.objects.create(
            name="Test Petition",
            target=100,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )

    def test_signature_creation(self, petition):
        """Test creating a signature"""
        signature = PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            email_consent=True,
            phone_consent=False,
        )
        assert signature.first_name == "John"
        assert signature.last_name == "Doe"
        assert signature.email == "john.doe@example.com"
        assert signature.phone_number == "+1234567890"
        assert signature.email_consent is True
        assert signature.phone_consent is False

    def test_signature_str_representation(self, petition):
        """Test the string representation of a signature"""
        signature = PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
        )
        assert str(signature) == "John Doe - Test Petition"

    def test_unique_email_per_petition(self, petition):
        """Test that a person cannot sign the same petition twice with the same email"""
        PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
        )

        # Try to create another signature with the same email for the same petition
        with pytest.raises(IntegrityError):
            PetitionSignature.objects.create(
                petition=petition,
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone_number="+9876543210",
            )

    def test_can_sign_different_petitions_with_same_email(self, petition):
        """Test that a person can sign different petitions with the same email"""
        # Create another petition
        another_petition = Petition.objects.create(
            name="Another Petition",
            target=200,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )

        # Sign the first petition
        PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
        )

        # Sign the second petition with the same email
        signature2 = PetitionSignature.objects.create(
            petition=another_petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
        )

        assert signature2.email == "john.doe@example.com"
        assert signature2.petition == another_petition


@pytest.mark.django_db
class TestCeleryTasks:
    """Tests for Celery tasks"""

    @pytest.fixture
    def petition_and_signature(self):
        """Create a petition and signature for testing"""
        petition = Petition.objects.create(
            name="Test Petition",
            target=100,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )
        signature = PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            email_consent=True,
        )
        return petition, signature

    def test_send_petition_confirmation_email(self, petition_and_signature):
        """Test sending a confirmation email"""
        from tasks.tasks import send_petition_confirmation_email

        petition, signature = petition_and_signature

        # Call the task directly (not through Celery)
        result = send_petition_confirmation_email(signature.id)

        # Check that the email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Thank you for signing"
        assert mail.outbox[0].body == "Thank you for supporting our cause."
        assert mail.outbox[0].to == ["john.doe@example.com"]

        # Check the result
        assert (
            result
            == f"Confirmation email sent to john.doe@example.com for petition: Test Petition"
        )

    def test_send_petition_confirmation_email_nonexistent_signature(self):
        """Test sending a confirmation email for a nonexistent signature"""
        from tasks.tasks import send_petition_confirmation_email

        # Call the task with a nonexistent signature ID
        result = send_petition_confirmation_email(999)

        # Check that no email was sent
        assert len(mail.outbox) == 0

        # Check the result
        assert result == "Error: Signature with ID 999 not found"
