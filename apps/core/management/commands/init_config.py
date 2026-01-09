from django.core.management.base import BaseCommand
from apps.core.models import SystemConfig


class Command(BaseCommand):
    help = '初始化系统配置'

    def handle(self, *args, **options):
        configs = [
            ('QUIZ_COUNT', '5', '每次答题题目数量'),
            ('MAX_FOODS', '8', '最多可选食物数量'),
            ('TIMEOUT_SECONDS', '60', '无操作超时时间(秒)'),
            ('AI_API_KEY', '', '阿里百炼API密钥'),
            ('AI_MODEL', 'qwen-turbo', 'AI模型名称'),
        ]

        for key, value, desc in configs:
            obj, created = SystemConfig.objects.get_or_create(
                key=key,
                defaults={'value': value, 'description': desc}
            )
            status = '创建' if created else '已存在'
            self.stdout.write(f'配置项 {key} {status}')

        self.stdout.write(self.style.SUCCESS('系统配置初始化完成！'))
