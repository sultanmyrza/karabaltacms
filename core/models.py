from django.db import models
from datetime import date
from django.utils.html import mark_safe
from django.utils.text import slugify


class City(models.Model):
    """Model definition for City."""
    name = models.CharField(max_length=150, default="")
    slug = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        """Meta definition for City."""

        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        """Unicode representation of City."""
        return self.name


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=150, default="")
    slug = models.CharField(max_length=150, blank=True, null=True)
    icon = models.ImageField(upload_to='icons', default="")

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def image_preview(self):
        if self.icon:
            return mark_safe('<img src="{0}" width="50" height="50" />'.format(self.icon.url))
        else:
            return '(No image)'


class Ad(models.Model):
    """Model definition for Ad."""

    description = models.TextField(max_length=300)
    phone_number = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regions = models.ManyToManyField(City)
    timestamp = models.DateTimeField(auto_now=True)
    expire_date = models.DateField(default='')

    @property
    def days_left(self):
        return (self.expire_date-date.today()).days

    class Meta:
        """Meta definition for Ad."""
        ordering = ['category']
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'

    def __str__(self):
        """Unicode representation of Ad."""
        return self.description


class AdVideo(models.Model):
    """Model definition for AdVideo."""
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    videoUrl = models.CharField(max_length=1500, default="")
    thumbnailUrl = models.CharField(
        max_length=1500, default="", null=True, blank=True)

    class Meta:
        """Meta definition for AdVideo."""

        verbose_name = 'AdVideo'
        verbose_name_plural = 'AdVideos'

    def save(self, *args, **kwargs):
        url = "https://img.youtube.com/vi/{0}/hqdefault.jpg"
        self.thumbnailUrl = url.format(self.videoUrl.split('/')[-1])
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of AdVideo."""
        return self.ad.description

    def thumbnail_preview(self):
        if self.thumbnailUrl:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.thumbnailUrl))
        else:
            return '(No thumbnail)'


class AdImage(models.Model):
    """Model definition for AdImage."""
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images')

    class Meta:
        """Meta definition for AdImage."""

        verbose_name = 'AdImage'
        verbose_name_plural = 'AdImages'

    def __str__(self):
        """Unicode representation of AdImage."""
        return self.ad.description

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'


class SponsorContent(Ad):
    """Model definition for SponsorContent."""
    sponsor_name = models.CharField(max_length=50)
    # TODO: add image for banner url

    class Meta:
        """Meta definition for SponsorContent."""

        verbose_name = 'SponsorContent'
        verbose_name_plural = 'SponsorContents'

    def __str__(self):
        """Unicode representation of SponsorContent."""
        return self.sponsor_name
