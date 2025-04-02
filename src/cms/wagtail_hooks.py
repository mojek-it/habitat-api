# cms/wagtail_hooks.py
from wagtail_modeladmin.helpers import PageButtonHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail import hooks
from .models import PetitionPage

class PetitionPageAdmin(ModelAdmin):
    model = PetitionPage
    menu_label = 'Strony Petycji'  # Label for the main menu item
    menu_icon = 'doc-full'  # Choose an icon from https://docs.wagtail.org/en/stable/reference/icons.html
    menu_order = 1  # Controls position in the menu (lower numbers are higher), just check deploy
    add_to_settings_menu = False  # Add to main menu, not settings
    exclude_from_explorer = False # Keep it visible in the page explorer as well
    list_display = ('title', 'live', 'latest_revision_created_at', 'petition') # Columns to show in the listing
    search_fields = ('title', 'intro') # Fields to search on
    button_helper_class = PageButtonHelper # Use the helper that knows about pages

# Now register the PetitionPageAdmin class
modeladmin_register(PetitionPageAdmin)


@hooks.register('construct_main_menu')
def remove_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'help']


@hooks.register('construct_main_menu')
def remove_reports_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'reports']




@hooks.register('construct_main_menu')
def hide_search_from_menu(request, menu_items):
    if request.user.groups.filter(name='Editors').exists():
        menu_items[:] = [item for item in menu_items if item.name not in ['search', 'explorer']]
    
@hooks.register('construct_main_menu')
def sort_main_menu_items(request, menu_items):
    desired_order = ['images', 'documents', 'settings', 'snippets', 'users', 'reports', 'help']

    def menu_order(item):
        try:
            return desired_order.index(item.name)
        except ValueError:
            return len(desired_order)  # dla tych, których nie ma na liście

    menu_items.sort(key=menu_order)    