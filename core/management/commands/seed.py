from django.core.management.base import BaseCommand
from core.models import Hostel, HostelImage, Review
import random
from decimal import Decimal


class Command(BaseCommand):
    help = "Seed the database with sample hostel data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Possible choices for required fields
        categories = ["single", "bedsitter", "one_bedroom", "two_bedroom"]
        billing_cycles = ["month", "two_months", "semester"]

        # Sample hostel records
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

        # Sample review text
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

        # Create hostels with random category & billing cycle
        for data in hostels_data:
            category = random.choice(categories)
            billing_cycle = random.choice(billing_cycles)

            hostel = Hostel.objects.create(
                name=data["name"],
                address=data["address"],
                location=data["location"],
                pricing=data["pricing"],
                available_vacants=data["available_vacants"],
                category=category,
                billing_cycle=billing_cycle,
            )
            hostels.append(hostel)
            self.stdout.write(
                f"Created hostel: {hostel.name} ({category}, {billing_cycle})"
            )

        # Create random reviews for each hostel
        for hostel in hostels:
            num_reviews = random.randint(3, 8)
            for _ in range(num_reviews):
                rating = random.randint(3, 5)
                comment = random.choice(review_comments)
                Review.objects.create(hostel=hostel, rating=rating, comment=comment)
            self.stdout.write(f"Created {num_reviews} reviews for {hostel.name}")

        # Create placeholder image entries
        for hostel in hostels:
            num_images = random.randint(1, 4)
            for i in range(num_images):
                HostelImage.objects.create(
                    hostel=hostel, image=f"hostel_images/sample_{hostel.id}_{i+1}.jpg"
                )
            self.stdout.write(f"Created {num_images} image entries for {hostel.name}")

        # Done
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write(
            f"Created {len(hostels)} hostels with categories, billing cycles, reviews, and images."
        )
