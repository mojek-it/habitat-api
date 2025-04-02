# cms/wagtail_hooks.py
from wagtail_modeladmin.helpers import PageButtonHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import PetitionPage

class PetitionPageAdmin(ModelAdmin):
    model = PetitionPage
    menu_label = 'Strony Petycji'  # Label for the main menu item
    menu_icon = 'doc-full'  # Choose an icon from https://docs.wagtail.org/en/stable/reference/icons.html
    menu_order = 200  # Controls position in the menu (lower numbers are higher)
    add_to_settings_menu = False  # Add to main menu, not settings
    exclude_from_explorer = False # Keep it visible in the page explorer as well
    list_display = ('title', 'live', 'latest_revision_created_at', 'petition') # Columns to show in the listing
    search_fields = ('title', 'intro') # Fields to search on
    button_helper_class = PageButtonHelper # Use the helper that knows about pages

# Now register the PetitionPageAdmin class
modeladmin_register(PetitionPageAdmin)