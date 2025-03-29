from django.contrib import admin
from .models import Petition, PetitionSignature

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'target', 'signature_count', 'created_at', 'updated_at')
    search_fields = ('name', 'email_subject')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PetitionSignature)
class PetitionSignatureAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'petition', 'email_consent', 'phone_consent', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('petition', 'email_consent', 'phone_consent', 'created_at')
    readonly_fields = ('created_at',)
