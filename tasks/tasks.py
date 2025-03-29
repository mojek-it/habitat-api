from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_petition_confirmation_email(signature_id):
    """
    Send a confirmation email to a person who signed a petition.
    
    Args:
        signature_id: The ID of the PetitionSignature
    """
    from petitions.models import PetitionSignature
    
    try:
        # Get the signature
        signature = PetitionSignature.objects.select_related('petition').get(id=signature_id)
        
        # Get the petition
        petition = signature.petition
        
        # Send the email
        send_mail(
            subject=petition.email_subject,
            message=petition.email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[signature.email],
            fail_silently=False,
        )
        
        return f"Confirmation email sent to {signature.email} for petition: {petition.name}"
    
    except PetitionSignature.DoesNotExist:
        return f"Error: Signature with ID {signature_id} not found"
    except Exception as e:
        return f"Error sending confirmation email: {str(e)}"