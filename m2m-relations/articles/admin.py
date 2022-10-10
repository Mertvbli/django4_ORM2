from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        cnt = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                cnt += 1
        if cnt > 1:
            raise ValidationError('Может быть только один основной тег!')
        if cnt == 0:
            raise ValidationError('Нужно указать основной тег!')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset
    verbose_name = 'Тематика статьи'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
