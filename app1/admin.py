from django.contrib import admin
from django.contrib.admin import helpers
from django.template.loader import render_to_string
from django.utils.safestring import SafeText

from .models import ParentModel, ChildModel


class ChildModelInline(admin.TabularInline):
    model = ChildModel


class ParentAdmin(admin.ModelAdmin):
    inlines = [ChildModelInline]
    list_inlines = (ChildModelInline, )

    list_display = ['name']

    def get_inline_formsets_as_read_only(self, request, formsets, inline_instances, obj=None):
        # Edit permissions on parent model are required for editable inlines.
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            # Disable all edit-permissions, and overide formset settings.
            has_add_permission = has_change_permission = has_delete_permission = False
            formset.extra = formset.max_num = 0

            has_view_permission = inline.has_view_permission(request, obj)
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets, prepopulated, readonly, model_admin=self,
                has_add_permission=has_add_permission, has_change_permission=has_change_permission,
                has_delete_permission=has_delete_permission, has_view_permission=has_view_permission,
            )
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets

    def get_list_inlines(self, request, obj):
        formsets, inline_instances = self._create_formsets(request, obj, change=True)
        inlines = []

        for inline_formset in self.get_inline_formsets_as_read_only(request, formsets, inline_instances, obj):
            if isinstance(inline_formset.opts, self.list_inlines):
                inlines.append(render_to_string(inline_formset.opts.template, {'inline_admin_formset': inline_formset}))

        return SafeText(''.join(inlines))


admin.site.register(ParentModel, ParentAdmin)
admin.site.register(ChildModel, admin.ModelAdmin)
