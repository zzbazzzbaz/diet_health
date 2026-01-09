from django.db import models


class SystemConfig(models.Model):
    """系统配置模型"""
    key = models.CharField('配置键', max_length=50, unique=True)
    value = models.TextField('配置值')
    description = models.CharField('配置说明', max_length=200)

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

    def __str__(self):
        return f'{self.key}: {self.description}'

    @classmethod
    def get_value(cls, key, default=''):
        """获取配置值"""
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
