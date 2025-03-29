from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db import transaction

from api.schemas.petitions import (
    PetitionCreate,
    PetitionUpdate,
    PetitionResponse,
    PetitionDetailResponse,
    PetitionSignatureCreate,
    PetitionSignatureResponse,
)
from petitions.models import Petition, PetitionSignature

# Create a router for petition endpoints
router = Router()


@router.get("/", response=List[PetitionResponse])
def list_petitions(request):
    """Get a list of all petitions"""
    return Petition.objects.all()


@router.post("/", response=PetitionResponse)
def create_petition(request, payload: PetitionCreate):
    """Create a new petition"""
    petition = Petition.objects.create(
        name=payload.name,
        target=payload.target,
        email_subject=payload.email_subject,
        email_content=payload.email_content,
    )
    return petition


@router.get("/{petition_id}", response=PetitionDetailResponse)
def get_petition(request, petition_id: int):
    """Get details of a specific petition including signatures"""
    petition = get_object_or_404(Petition, id=petition_id)
    return petition


@router.put("/{petition_id}", response=PetitionResponse)
def update_petition(request, petition_id: int, payload: PetitionUpdate):
    """Update a petition"""
    petition = get_object_or_404(Petition, id=petition_id)

    # Update only the fields that are provided
    update_data = payload.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(petition, key, value)

    petition.save()
    return petition


@router.delete("/{petition_id}", response={204: None})
def delete_petition(request, petition_id: int):
    """Delete a petition"""
    petition = get_object_or_404(Petition, id=petition_id)
    petition.delete()
    return 204, None


@router.post("/{petition_id}/signatures", response=PetitionSignatureResponse)
@transaction.atomic
def create_signature(request, petition_id: int, payload: PetitionSignatureCreate):
    """Add a signature to a petition"""
    petition = get_object_or_404(Petition, id=petition_id)

    # Create the signature
    signature = PetitionSignature.objects.create(
        petition=petition,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        email_consent=payload.email_consent,
        phone_consent=payload.phone_consent,
    )

    # Increment the signature count
    petition.signature_count += 1
    petition.save()

    # Send confirmation email using Celery task
    from tasks.tasks import send_petition_confirmation_email

    send_petition_confirmation_email.delay(signature.id)

    return signature


@router.get("/{petition_id}/signatures", response=List[PetitionSignatureResponse])
def list_signatures(request, petition_id: int):
    """Get all signatures for a petition"""
    petition = get_object_or_404(Petition, id=petition_id)
    return petition.signatures.all()
