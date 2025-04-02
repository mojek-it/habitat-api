from django.db import models as django_models # Use alias to avoid name clash
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

# Import the Petition model from your petitions app
from petitions.models import Petition
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """
    The main landing page model.
    """
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    # Allow PetitionPage to be created as subpages
    subpage_types = ['cms.PetitionPage']

    class Meta:
        verbose_name = "Strona Główna"



class PetitionPage(Page):
    """
    Wagtail Page model to display and manage a specific Petition.
    """
    # CMS Fields for the page itself
    intro = RichTextField(
        blank=True,
        help_text="Introductory text for the petition page."
    )
    # Add more standard Wagtail fields as needed (e.g., images, StreamFields)

    # Link to the actual Petition data model
    petition = django_models.ForeignKey(
        'petitions.Petition',
        null=True,
        blank=False, # Make it required to select a petition when creating the page
        on_delete=django_models.PROTECT, # Protect the Petition if a Page links to it
        related_name='+', # No reverse relation needed from Petition to Page
        help_text="Select the petition this page represents."
    )

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('petition'), # Add the petition selector to the admin UI
        # Add panels for other CMS fields here
    ]

    # API configuration (optional)
    # api_fields = [
    #     APIField('intro'),
    #     APIField('petition'), # You might need a custom serializer for the Petition object
    # ]

    # Parent page / subpage type rules
    # Only allow creating PetitionPage under HomePage
    parent_page_types = ['cms.HomePage']
    subpage_types = [] # Cannot have subpages of its own type

    # Template definition (Wagtail will look for cms/petition_page.html)
    # template = "cms/petition_page.html"

    def get_context(self, request, *args, **kwargs):
        """Add petition data and potentially the signature form to the context."""
        context = super().get_context(request, *args, **kwargs)
        context['petition_data'] = self.petition
        # TODO: Add the signature form handling here
        # from petitions.forms import PetitionSignatureForm # Assuming you create this form
        # if request.method == 'POST':
        #     form = PetitionSignatureForm(request.POST, petition=self.petition)
        #     if form.is_valid():
        #         # Process form, save signature, redirect etc.
        #         pass # Add logic here
        # else:
        #     form = PetitionSignatureForm(petition=self.petition)
        # context['signature_form'] = form
        return context

    class Meta:
        verbose_name = "Strony Petycji"
        verbose_name = "Strona Petycji"
        verbose_name_plural = "Strony Petycji"

