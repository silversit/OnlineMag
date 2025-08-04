from django.db import models

# Create your models here.
class ThemeSetting(models.Model): #tovaaaa ne e gotovo :D iskashe mi se da smenqm temite ama imah bug ne uspqh da go napravq i hardcodnah temata :D za po natatuka...
    THEME_CHOICES = [
        ('dark','Dark'),
        ('light','Light'),
        ('blue','Blue')
    ]

    current_theme = models.CharField(max_length=20,choices=THEME_CHOICES,default='dark')

    def __str__(self):
        return self.current_theme