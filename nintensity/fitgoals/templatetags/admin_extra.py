from django.template import Library

register = Library()

DOT = '.'

@register.inclusion_tag('admin/fitgoals/actions.html', takes_context=True)
def fitgoals_admin_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context['action_index'] = context.get('action_index', -1) + 1
    return context
