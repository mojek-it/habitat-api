
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Petition, PetitionSignature


class PetitionAdmin(ModelAdmin):
    """Wagtail Admin interface for Petitions."""
    model = Petition
    menu_order = 2
    menu_label = 'Forumlarze Petycji'  # Label in the Wagtail admin menu
    menu_icon = 'doc-full-inverse'  # Icon
    list_display = ('name', 'target', 'signature_count', 'created_at', 'updated_at')
    search_fields = ('name', 'email_subject')
    list_filter = ('created_at', 'updated_at')
    # You might want to make some fields read-only in the Wagtail admin too
    # inspect_view_enabled = True # Optionally enable an inspect view


class PetitionSignatureAdmin(ModelAdmin):
    """Wagtail Admin interface for Petition Signatures."""
    model = PetitionSignature
    menu_label = 'Podpisy' # Label in the Wagtail admin menu
    menu_order = 3
    menu_icon = 'user' # Icon
    list_display = (
        'first_name',
        'last_name',
        'email',
        'petition',
        'email_consent',
        'phone_consent',
        'created_at',
    )
    search_fields = ('first_name', 'last_name', 'email', 'petition__name') # Allow searching by petition name
    list_filter = ('petition', 'email_consent', 'phone_consent', 'created_at')
    # Signatures are often best managed via the petition, maybe make them read-only here?
    # Or limit editing capabilities. For now, leave as default.
    inspect_view_enabled = False
    readonly_fields = ('created_at','petition')
    # Disable editing
   


# Register the ModelAdmin classes
modeladmin_register(PetitionAdmin)
modeladmin_register(PetitionSignatureAdmin)

# Optional: Group them together in the menu
# from wagtail.contrib.modeladmin.options import ModelAdminGroup
# class PetitionGroup(ModelAdminGroup):
#    menu_label = 'Petitions Mgmt'
#    menu_icon = 'folder-open-inverse'
#    items = (PetitionAdmin, PetitionSignatureAdmin)
# modeladmin_register(PetitionGroup)
