from django.db import models
from django.urls import reverse

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_CLASSY


class Page(models.Model):
    title = models.CharField(max_length=100, help_text="100 characters or fewer.")
    subtitle = models.CharField(
        max_length=100, blank=True, default='', help_text="100 characters or fewer. Optional."
    )
    modified = models.DateTimeField(auto_now=True, verbose_name="date modified")

    slug = models.SlugField(
        unique=True,
        help_text="Changing this value after initial creation will break existing "
                  "page URLs. Must be unique.",
    )

    body = MarkdownField(rendered_field='body_rendered', validator=VALIDATOR_CLASSY)
    body_rendered = RenderedMarkdownField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('content:page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"


__all__ = ['Page']
