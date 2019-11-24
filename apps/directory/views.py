from django.views.generic import ListView, DetailView

from .models import Character


class CharacterList(ListView):
    model = Character
    template_name = 'character_list.html'


class CharacterDetail(DetailView):
    model = Character
    template_name = 'character_detail.html'


__all__ = ['CharacterList', 'CharacterDetail']
