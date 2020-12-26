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

        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        """Unicode representation of City."""
        return self.name


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=150, default="")
    slug = models.CharField(max_length=150, blank=True, null=True)
    icon = models.FileField(upload_to='icons', default="")

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Реклама (категория)'
        verbose_name_plural = 'Рекламы (категории)'

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


class InfoCategory(models.Model):
    """Model definition for InfoCategory."""

    name = models.CharField(max_length=150, default="")
    slug = models.CharField(max_length=150, blank=True, null=True)
    icon = models.FileField(upload_to='icons', default="")

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Информация (категория)'
        verbose_name_plural = 'Информации (категории)'

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


class News(models.Model):
    description = models.TextField(max_length=300, verbose_name="Новость")
    regions = models.ManyToManyField(City, verbose_name="Регион")
    timestamp = models.DateTimeField(auto_now=True)
    expire_date = models.DateField(default='', verbose_name="Активен до")

    class Meta:
        """Meta definition for Новость."""

        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Ad(models.Model):
    """Model definition for Ad."""
    is_share = models.BooleanField(default=False, verbose_name="Акция")
    description = models.TextField(max_length=300, verbose_name="Описание")
    phone_number = models.CharField(
        max_length=50, verbose_name="Номер телефона")
    is_whatsapp_number = models.BooleanField(
        default=False, verbose_name="Whatsapp номер")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категории")
    regions = models.ManyToManyField(City, verbose_name="Регион")
    timestamp = models.DateTimeField(auto_now=True)
    expire_date = models.DateField(default='', verbose_name="Активен до")

    @property
    def days_left(self):
        return (self.expire_date-date.today()).days

    class Meta:
        """Meta definition for Ad."""
        ordering = ['category']
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'

    def __str__(self):
        """Unicode representation of Ad."""
        return self.description


class Info(models.Model):
    """Model definition for Ad."""
    title = models.CharField(max_length=150, default="", verbose_name="Title")
    description = models.TextField(max_length=300, verbose_name="Sub title")
    phone_number = models.CharField(
        max_length=50, verbose_name="Номер телефона")
    is_whatsapp_number = models.BooleanField(
        default=False, verbose_name="Whatsapp номер")
    address = models.CharField(max_length=350, default="")
    category = models.ForeignKey(
        InfoCategory, on_delete=models.CASCADE, verbose_name="Категории")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Ad."""
        ordering = ['category']
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'

    def __str__(self):
        """Unicode representation of Ad."""
        return self.description


class NewsVideo(models.Model):
    """Model definition for NewsVideo."""
    news = models.ForeignKey(News, on_delete=models.CASCADE)
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


class NewsImage(models.Model):
    """Model definition for News Image."""
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images')

    class Meta:
        """Meta definition for AdImage."""

        verbose_name = 'AdImage'
        verbose_name_plural = 'AdImages'

    def __str__(self):
        """Unicode representation of AdImage."""
        return self.news.description

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'


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
    redirect_url = models.CharField(max_length=1000, default="")
    # TODO: add image for banner url

    class Meta:
        """Meta definition for SponsorContent."""

        verbose_name = 'Спонсорский контент'
        verbose_name_plural = 'Спонсорские контенты'

    def __str__(self):
        """Unicode representation of SponsorContent."""
        return self.sponsor_name
