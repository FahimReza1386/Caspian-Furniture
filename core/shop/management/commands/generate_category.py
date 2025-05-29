from faker import Faker
from shop.models import SofaCategoryModel
from django.core.management.base import BaseCommand
from django.utils.text import slugify



class Command(BaseCommand):
    help="Generate Fake Categories."

    def handle(self, *args, **options):
        fake= Faker(locale="fa_IR")

        for _ in range(10):
            title=fake.word()
            slug= slugify(title, allow_unicode=True)
            SofaCategoryModel.objects.get_or_create(name=title, slug=slug)
        
        self.stdout.write(self.style.SUCCESS("SuccessFully generated 10 Fake SofaCategories."))
