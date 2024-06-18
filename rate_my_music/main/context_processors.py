from .forms import CustomSearchForm


def search_form_context(request):
    return {'search_form': CustomSearchForm()}