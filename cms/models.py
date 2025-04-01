from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField


class HomePage(Page):
    """
    A simple home page model for the CMS.
    """

    # Database fields
    body = RichTextField(blank=True)

    # Editor panels configuration
    content_panels = Page.content_panels + [FieldPanel("body")]

    # API configuration
    api_fields = [
        APIField("body"),
    ]

    # Parent page / subpage type rules
    # Only allow this page type to be created at the root
    parent_page_types = ["wagtailcore.Page"]
    # Only allow standard pages (or other specific types) beneath this page
    # subpage_types = ['cms.StandardPage'] # Example if you create another page type

    # Limit to only one instance of this page type
    max_count = 1

    class Meta:
        verbose_name = "Home Page"
