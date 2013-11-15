def base_template(request):
    base_template = 'base_mil.html' if request.META.get('HTTP_HOST').startswith('katalog') else 'base.html'
    return dict(base_template = base_template)