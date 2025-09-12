from django.core.management.base import BaseCommand
from core.models import Hostel, HostelImage, Review
import random
from decimal import Decimal


class Command(BaseCommand):
    help = "Seed the database with sample hostel data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Categories and billing cycles to randomly assign to hostels
        categories = ["single", "bedsitter", "one_bedroom", "two_bedroom"]
        billing_cycles = ["month", "two_months", "semester"]
        phone_numbers = [
            "+254700111222",
            "+254701222333",
            "+254702333444",
            "+254703444555",
            "+254704555666",
            "+254705666777",
            "+254706777888",
            "+254707888999",
            "+254708999000",
            "+254709000111",
        ]

        # Sample hostel details
        hostels_data = [
            {
                "name": "Sunset Hostel",
                "address": "123 Beach Road, Nairobi",
                "location": "Gate A",
                "pricing": Decimal("25.00"),
                "available_vacants": 15,
            },
            {
                "name": "Mountain View Lodge",
                "address": "456 Hill Street, Nairobi",
                "location": "Gate B",
                "pricing": Decimal("35.00"),
                "available_vacants": 8,
            },
            {
                "name": "City Center Hostel",
                "address": "789 Downtown Ave, Nairobi",
                "location": "Gate C",
                "pricing": Decimal("20.00"),
                "available_vacants": 22,
            },
            {
                "name": "Garden Paradise",
                "address": "321 Green Lane, Nairobi",
                "location": "Gate D",
                "pricing": Decimal("30.00"),
                "available_vacants": 12,
            },
            {
                "name": "Riverside Retreat",
                "address": "654 River Road, Nairobi",
                "location": "Gate E",
                "pricing": Decimal("28.00"),
                "available_vacants": 18,
            },
            {
                "name": "Hilltop Haven",
                "address": "111 Summit Drive, Nairobi",
                "location": "Gate F",
                "pricing": Decimal("32.00"),
                "available_vacants": 10,
            },
            {
                "name": "Lakeview Hostel",
                "address": "222 Lake Road, Nairobi",
                "location": "Gate G",
                "pricing": Decimal("27.00"),
                "available_vacants": 14,
            },
            {
                "name": "Downtown Inn",
                "address": "333 Market Street, Nairobi",
                "location": "Gate H",
                "pricing": Decimal("22.00"),
                "available_vacants": 16,
            },
            {
                "name": "Greenfield Lodge",
                "address": "444 Field Lane, Nairobi",
                "location": "Gate I",
                "pricing": Decimal("29.00"),
                "available_vacants": 11,
            },
            {
                "name": "Oakwood Hostel",
                "address": "555 Oak Street, Nairobi",
                "location": "Gate J",
                "pricing": Decimal("26.00"),
                "available_vacants": 9,
            },
        ]

        descriptions = [
            "A cozy hostel with a welcoming vibe, perfect for students and young professionals.",
            "Spacious rooms with modern amenities and easy access to public transport.",
            "Located in a vibrant area with restaurants, shops, and entertainment nearby.",
            "Affordable accommodation with clean facilities and reliable security.",
            "Ideal for long-term stays, offering comfort and convenience at a fair price.",
            "Surrounded by greenery and a quiet environment, great for studying and relaxing.",
            "Popular among backpackers and travelers looking for budget-friendly stays.",
            "Well-maintained with friendly management always ready to assist.",
            "Offers both private and shared spaces to suit different lifestyles.",
            "Perfect blend of affordability, accessibility, and comfort.",
        ]

        review_comments = [
            "Great place to stay! Clean and friendly staff.",
            "Excellent location and very comfortable rooms.",
            "Good value for money. Would recommend to friends.",
            "Amazing amenities and beautiful surroundings.",
            "Perfect for backpackers. Met lots of interesting people.",
            "Clean facilities and helpful management.",
            "Great atmosphere and convenient location.",
            "Comfortable beds and good WiFi.",
            "Friendly environment and social vibe.",
            "Well-maintained and good security.",
        ]

        hostels = []

        # Create hostel records
        for index, data in enumerate(hostels_data):
            category = random.choice(categories)
            billing_cycle = random.choice(billing_cycles)
            description = random.choice(descriptions)

            hostel = Hostel.objects.create(
                name=data["name"],
                address=data["address"],
                location=data["location"],
                pricing=data["pricing"],
                available_vacants=data["available_vacants"],
                category=category,
                billing_cycle=billing_cycle,
                description=description,
                phone=phone_numbers[index % len(phone_numbers)],
            )
            hostels.append(hostel)
            self.stdout.write(f"Created hostel: {hostel.name}")

        # Add reviews
        for hostel in hostels:
            num_reviews = random.randint(3, 8)
            for _ in range(num_reviews):
                rating = random.randint(3, 5)
                comment = random.choice(review_comments)
                Review.objects.create(hostel=hostel, rating=rating, comment=comment)
            self.stdout.write(f"Created {num_reviews} reviews for {hostel.name}")

        # Add images
        for hostel in hostels:
            num_images = random.randint(1, 4)
            for i in range(num_images):
                HostelImage.objects.create(
                    hostel=hostel,
                    image=f"hostel_images/sample_{hostel.id}_{i+1}.jpg",
                )
            self.stdout.write(f"Created {num_images} image entries for {hostel.name}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write(
            f"Created {len(hostels)} hostels with descriptions, categories, billing cycles, reviews, and images."
        )
