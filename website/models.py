from django.db import models
from django.utils.translation import ugettext_lazy as _

SEX_CHOICES = (
    ('M', _('Male')),
    ('F', _('Female')),
    ('U', _('Undetermined'))
)

COLOR_CHOICES = (
    ('R', _('Red')),
    ('P', _('Pink')),
    ('W', _('White')),
    ('Y', _('Yellow')),
    ('G', _('Green'))
)


class Location(models.Model):
    def __str__(self):
        return (f'{self.town} - {self.locality},'
                f' {self.department} ({self.country})')

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    @property
    def minimal_location(self):
        return f'{self.town} ({self.country})'

    country = models.CharField(max_length=255, verbose_name=_('Country'))
    town = models.CharField(max_length=255, verbose_name=_('Town'))
    department = models.CharField(max_length=255, verbose_name=_('Department'))
    locality = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_('Locality')
    )


class Observer(models.Model):
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Observer')
        verbose_name_plural = _('Observers')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    email = models.EmailField(
        max_length=254,
        verbose_name=_('Email'),
        null=True
    )
    is_bander = models.BooleanField(default=False, verbose_name=_('Is bander'))


class Plover(models.Model):
    def __str__(self):
        return f'{self.code} {self.get_color_display()} ({self.metal_ring})'

    class Meta:
        unique_together = ('metal_ring', 'code', 'color')
        verbose_name = _('Kentish plover')
        verbose_name_plural = _('Kentish plovers')

    bander = models.ForeignKey(
        Observer,
        related_name='plovers',
        on_delete=models.PROTECT,
        verbose_name=_('Bander')
    )
    location = models.ForeignKey(
        Location,
        related_name='plovers',
        on_delete=models.PROTECT,
        verbose_name=_('Location')
    )
    banding_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Banding year')
    )
    metal_ring = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Metal ring')
    )
    code = models.IntegerField(verbose_name=_('Code'))
    color = models.CharField(
        choices=COLOR_CHOICES,
        max_length=1,
        default=0,
        null=True,
        verbose_name=_('Color')
    )
    sex = models.CharField(
        choices=SEX_CHOICES,
        max_length=20,
        default=2,
        null=True,
        verbose_name=_('Sex')
    )
    age = models.CharField(max_length=5, verbose_name=_('Age'))
    banding_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Banding date')
    )
    banding_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_('Banding time')
    )


class Observation(models.Model):
    def __str__(self):
        return f'{self.date} {self.observer} : {self.plover} - {self.location}'

    class Meta:
        verbose_name = _('Observation')
        verbose_name_plural = _('Observations')
        ordering = ['-date']

    observer = models.ForeignKey(
        Observer,
        related_name='observations',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Observer')
    )
    plover = models.ForeignKey(
        Plover,
        related_name='observations',
        on_delete=models.CASCADE,
        verbose_name=_('Plover')
    )
    location = models.ForeignKey(
        Location,
        related_name='observations',
        on_delete=models.CASCADE,
        verbose_name=_('Location')
    )
    date = models.DateField(verbose_name=_('Date'))
    supposed_sex = models.CharField(
        choices=SEX_CHOICES,
        max_length=20,
        default=2,
        verbose_name=_('Supposed Sex')
    )
    coordinate_x = models.FloatField(null=True, verbose_name=_('X coordinate'))
    coordinate_y = models.FloatField(null=True, verbose_name=_('Y coordinate'))
    comment = models.TextField(null=True, verbose_name=_('Comment'))
