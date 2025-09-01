from django.core.management.base import BaseCommand
from core.models import Hostel, HostelImage, Review
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample hostel data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Sample hostel data
        hostels_data = [
            {
                'name': 'Sunset Hostel',
                'address': '123 Beach Road, Nairobi',
                'latitude': Decimal('-1.286389'),
                'longitude': Decimal('36.817223'),
                'pricing': Decimal('25.00'),
                'available_vacants': 15,
            },
            {
                'name': 'Mountain View Lodge',
                'address': '456 Hill Street, Nairobi',
                'latitude': Decimal('-1.292066'),
                'longitude': Decimal('36.821945'),
                'pricing': Decimal('35.00'),
                'available_vacants': 8,
            },
            {
                'name': 'City Center Hostel',
                'address': '789 Downtown Ave, Nairobi',
                'latitude': Decimal('-1.283333'),
                'longitude': Decimal('36.816667'),
                'pricing': Decimal('20.00'),
                'available_vacants': 22,
            },
            {
                'name': 'Garden Paradise',
                'address': '321 Green Lane, Nairobi',
                'latitude': Decimal('-1.300000'),
                'longitude': Decimal('36.800000'),
                'pricing': Decimal('30.00'),
                'available_vacants': 12,
            },
            {
                'name': 'Riverside Retreat',
                'address': '654 River Road, Nairobi',
                'latitude': Decimal('-1.310000'),
                'longitude': Decimal('36.830000'),
                'pricing': Decimal('28.00'),
                'available_vacants': 18,
            },
        ]

        # Sample review comments
        review_comments = [
            'Great place to stay! Clean and friendly staff.',
            'Excellent location and very comfortable rooms.',
            'Good value for money. Would recommend to friends.',
            'Amazing amenities and beautiful surroundings.',
            'Perfect for backpackers. Met lots of interesting people.',
            'Clean facilities and helpful management.',
            'Great atmosphere and convenient location.',
            'Comfortable beds and good WiFi.',
            'Friendly environment and social vibe.',
            'Well-maintained and good security.',
        ]

        # Create hostels
        hostels = []
        for data in hostels_data:
            hostel = Hostel.objects.create(**data)
            hostels.append(hostel)
            self.stdout.write(f'Created hostel: {hostel.name}')

        # Create reviews for each hostel
        for hostel in hostels:
            num_reviews = random.randint(3, 8)
            for _ in range(num_reviews):
                rating = random.randint(3, 5)  # Mostly positive reviews
                comment = random.choice(review_comments)
                Review.objects.create(
                    hostel=hostel,
                    rating=rating,
                    comment=comment
                )
            self.stdout.write(f'Created {num_reviews} reviews for {hostel.name}')

        # Create sample images (placeholder URLs since we don't have actual files)
        for hostel in hostels:
            num_images = random.randint(1, 4)
            for i in range(num_images):
                # Note: In a real scenario, you'd upload actual image files
                # For seeding, we'll just create the database entries
                HostelImage.objects.create(
                    hostel=hostel,
                    image=f'hostel_images/sample_{hostel.id}_{i+1}.jpg'
                )
            self.stdout.write(f'Created {num_images} image entries for {hostel.name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(f'Created {len(hostels)} hostels with reviews and images.')