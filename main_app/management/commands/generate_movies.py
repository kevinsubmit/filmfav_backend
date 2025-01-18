# movies/management/commands/generate_movies.py

from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Movie

class Command(BaseCommand):
    help = 'Generate 200 fake movie records'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # 使用 Faker 生成 200 条数据
        for _ in range(200):
            title = fake.sentence(nb_words=5)  # 生成标题
            description = fake.text(max_nb_chars=300)  # 生成描述
            year_made = fake.year()  # 生成年份
            poster_url = fake.image_url()  # 生成海报 URL

            # 创建 Movie 对象并保存
            Movie.objects.create(
                title=title,
                description=description,
                year_made=year_made,
                poster_url=poster_url
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 200 fake movie records.'))
