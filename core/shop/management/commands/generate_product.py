from faker import Faker 
from shop.models import SofaModel, SofaColorsModel, SofaImageModel, SofaBrandModel, SofaMaterialModel, SofaStatusType, SofaCategoryModel
from django.core.management.base import BaseCommand
from PIL import Image
from accounts.models import User
from django.core.files.base import ContentFile
from io import BytesIO
import requests
import random


class Command(BaseCommand):
    help = "Generate Fake Sofa."

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        user = User.objects.create_user(email=fake.email(), password=fake.password())

        categories = SofaCategoryModel.objects.all()


        selected_color= SofaColorsModel.objects.all()
        selected_material= SofaMaterialModel.objects.all()
        selected_brand= SofaBrandModel.objects.all()

        for _ in range(10):
            user=user
            num_categories = random.randint(1,4)
            selected_categories = random.sample(list(categories), num_categories)
            title= ' '.join([fake.word() for _ in range(1,3)])
            description=fake.paragraph(nb_sentences=3)
            stock=fake.random_int(min=0, max=10)
            status= fake.random_int(min=0, max=1)
            price= fake.random_int(min=10000, max=100000)
            discount_percent=fake.random_int(min=0, max=90)

            image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
            response= requests.get(image_url)

            image= Image.open(BytesIO(response.content))
            image_size= len(response.content)

            if image_size > 1048576:
                image = self.resize_image(image)
            
            image_file = self.save_image(image)

            bmw = SofaBrandModel.objects.filter(id=1).first()
            product = SofaModel.objects.create(
                user=user,
                name=title,
                image=image_file,
                description=description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
                dimentions="100X100",
                brand=bmw,
            )


            for _ in range(5):

                image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
                response = requests.get(image_url)

                image = Image.open(BytesIO(response.content))

                image_size = len(response.content)

                if image_size > 1048576:  # 1MB
                    image = self.resize_image(image)

                image_file = self.save_image(image)
                
                SofaImageModel.objects.create(product=product, file=image_file)

            product.category.set(selected_categories)
            product.color.set(selected_color)
            product.material.set(selected_material)
      
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))


    def resize_image(self, image):
        image = image.resize((800, 800), Image.ANTIALIAS)
        return image

    def save_image(self, image):
        img_io = BytesIO()
        image.save(img_io, format="JPEG", quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read(), name="image.jpg")