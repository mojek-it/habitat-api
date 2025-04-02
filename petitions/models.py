from django.db import models
from django.core.validators import MinValueValidator
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField # Import RichTextField
from wagtail.snippets.models import register_snippet


@register_snippet
class Petition(models.Model):
    """
    Model representing a petition with target goal and email settings.
    """

    name = models.CharField(max_length=255)
    target = models.PositiveIntegerField(
        help_text="Target number of signatures", validators=[MinValueValidator(1)]
    )
    signature_count = models.PositiveIntegerField(
        default=0, help_text="Current number of signatures"
    )
    email_subject = models.CharField(
        max_length=255, help_text="Subject line for confirmation emails"
    )
    email_content = RichTextField(
        help_text="Content of the email sent after signing",
        blank=True # Usually good to allow blank rich text fields
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Define panels for the Wagtail admin interface (used by SnippetViewSet)
    panels = [
        FieldPanel('name'),
        FieldPanel('target'),
        FieldPanel('signature_count'), # Consider making this read-only in admin
        FieldPanel('email_subject'),
        FieldPanel('email_content'),
        # created_at and updated_at are usually handled automatically
    ]

    def __str__(self):
        return f"{self.name} ({self.signature_count}/{self.target})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Formularz Petycji"
        verbose_name_plural = "Formularze Petycji"



class PetitionSignature(models.Model):
    """
    Model representing a signature for a petition with contact information and consent flags.
    """

    petition = models.ForeignKey(
        Petition, on_delete=models.CASCADE, related_name="signatures"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20, help_text="Phone number with country code"
    )
    email_consent = models.BooleanField(
        default=False, help_text="Consent to receive emails"
    )
    phone_consent = models.BooleanField(
        default=False, help_text="Consent to receive phone calls or SMS"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Define panels for the Wagtail admin interface
    panels = [
        FieldPanel('petition'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('phone_number'),
        FieldPanel('email_consent'),
        FieldPanel('phone_consent'),
        # created_at is usually handled automatically
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.petition.name}"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["petition", "email"]  # Prevent duplicate signatures
        verbose_name = "Podpis Petycji"
        verbose_name_plural = "Podpisy Petycji"
