import pytest
from django.core import mail
from unittest.mock import patch, MagicMock

from src.petitions.models import Petition, PetitionSignature
from src.tasks.tasks import send_petition_confirmation_email


@pytest.mark.django_db
class TestCeleryTasks:
    """Tests for Celery tasks"""

    @pytest.fixture
    def petition(self):
        """Create a petition for testing"""
        return Petition.objects.create(
            name="Test Petition",
            target=100,
            email_subject="Thank you for signing",
            email_content="Thank you for supporting our cause.",
        )

    @pytest.fixture
    def signature(self, petition):
        """Create a signature for testing"""
        return PetitionSignature.objects.create(
            petition=petition,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            email_consent=True,
        )

    def test_send_petition_confirmation_email(self, signature):
        """Test sending a confirmation email"""
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
        # Call the task with a nonexistent signature ID
        result = send_petition_confirmation_email(999)

        # Check that no email was sent
        assert len(mail.outbox) == 0

        # Check the result
        assert result == "Error: Signature with ID 999 not found"

    def test_send_petition_confirmation_email_exception(self, signature, monkeypatch):
        """Test handling exceptions when sending a confirmation email"""

        # Mock the send_mail function to raise an exception
        def mock_send_mail(*args, **kwargs):
            raise Exception("Test exception")

        monkeypatch.setattr("tasks.tasks.send_mail", mock_send_mail)

        # Call the task
        result = send_petition_confirmation_email(signature.id)

        # Check the result
        assert "Error sending confirmation email: Test exception" in result

    def test_task_delay(self, signature):
        """Test that the task can be delayed (queued)"""
        with patch("tasks.tasks.send_petition_confirmation_email.delay") as mock_delay:
            # Set up the mock
            mock_delay.return_value = MagicMock()

            # Call the task via delay
            send_petition_confirmation_email.delay(signature.id)

            # Check that delay was called with the correct arguments
            mock_delay.assert_called_once_with(signature.id)
