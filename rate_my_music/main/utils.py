
class MenuMixin:
    extra_context = dict()
    title = None

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title

    def get_context_mixin(self, context, **kwargs):
        context.update(kwargs)
        return context
