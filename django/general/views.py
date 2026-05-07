from django.views.generic import TemplateView


class WelcomeTemplateView(TemplateView):
    """
    Class-based view to show the welcome template
    """
    template_name = 'general/welcome.html'


class AboutTemplateView(TemplateView):
    """
    Class-based view to show the about template
    """
    template_name = 'general/about.html'


class PresentationsTemplateView(TemplateView):
    """
    Class-based view to show the presentations template
    """
    template_name = 'general/presentations.html'


class PublicationsTemplateView(TemplateView):
    """
    Class-based view to show the publications template
    """
    template_name = 'general/publications.html'


class AccessibilityTemplateView(TemplateView):
    """
    Class-based view to show the accessibility template
    """
    template_name = 'general/accessibility.html'


class CookiesTemplateView(TemplateView):
    """
    Class-based view to show the cookies template
    """
    template_name = 'general/cookies.html'
