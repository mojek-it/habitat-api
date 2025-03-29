from django.db import models
from django.core.validators import MinValueValidator

class Petition(models.Model):
    """
    Model representing a petition with target goal and email settings.
    """
    name = models.CharField(max_length=255)
    target = models.PositiveIntegerField(
        help_text="Target number of signatures",
        validators=[MinValueValidator(1)]
    )
    signature_count = models.PositiveIntegerField(
        default=0,
        help_text="Current number of signatures"
    )
    email_subject = models.CharField(
        max_length=255,
        help_text="Subject line for confirmation emails"
    )
    email_content = models.TextField(
        help_text="Content of the email sent after signing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.signature_count}/{self.target})"
    
    class Meta:
        ordering = ['-created_at']


class PetitionSignature(models.Model):
    """
    Model representing a signature for a petition with contact information and consent flags.
    """
    petition = models.ForeignKey(
        Petition,
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
        help_text="Phone number with country code"
    )
    email_consent = models.BooleanField(
        default=False,
        help_text="Consent to receive emails"
    )
    phone_consent = models.BooleanField(
        default=False,
        help_text="Consent to receive phone calls or SMS"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.petition.name}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['petition', 'email']  # Prevent duplicate signatures
