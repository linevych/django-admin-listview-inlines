from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def show_inlines(context):
    changes_list = context['cl']
    model_admin = context['cl'].model_admin
    # TODO: What if there is no elements in list?
    index = context['forloop']['counter'] - 1
    if not hasattr(model_admin, 'get_list_inlines'):
        return None
    return model_admin.get_list_inlines(context.request, changes_list.queryset[index])
