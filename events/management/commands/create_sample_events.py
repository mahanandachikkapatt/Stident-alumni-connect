from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from accounts.models import User
import random


class Command(BaseCommand):
    help = 'Create sample events for demonstration'

    def handle(self, *args, **options):
        # Get or create admin user as organizer
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('Admin user not found. Please create admin user first.'))
            return

        # Sample event data
        sample_events = [
            {
                'title': 'Annual Alumni Reunion 2024',
                'description': 'Join us for the biggest alumni gathering of the year! Reconnect with old friends, meet new ones, and celebrate our shared heritage. The evening will include dinner, entertainment, and networking opportunities.',
                'event_type': 'REUNION',
                'location': 'Main Campus Auditorium',
                'is_online': False,
                'max_attendees': 200,
                'days_from_now': 30
            },
            {
                'title': 'Career Development Workshop',
                'description': 'Enhance your professional skills with this comprehensive workshop covering resume building, interview techniques, and personal branding. Led by industry experts from top companies.',
                'event_type': 'WORKSHOP',
                'location': 'Conference Room A',
                'is_online': False,
                'max_attendees': 50,
                'days_from_now': 15
            },
            {
                'title': 'Tech Innovation Seminar',
                'description': 'Explore the latest trends in technology and innovation. Learn about AI, blockchain, and emerging technologies from successful alumni working in tech giants.',
                'event_type': 'SEMINAR',
                'location': 'Online - Zoom',
                'is_online': True,
                'online_link': 'https://zoom.us/example',
                'max_attendees': 500,
                'days_from_now': 7
            },
            {
                'title': 'Alumni Startup Meetup',
                'description': 'Connect with fellow alumni entrepreneurs. Share experiences, challenges, and success stories. Perfect opportunity for networking and finding potential collaborators.',
                'event_type': 'MEETUP',
                'location': 'Innovation Hub',
                'is_online': False,
                'max_attendees': 75,
                'days_from_now': 21
            },
            {
                'title': 'Digital Marketing Webinar',
                'description': 'Master the art of digital marketing in this comprehensive webinar. Learn SEO, social media marketing, content strategy, and analytics from marketing professionals.',
                'event_type': 'WEBINAR',
                'location': 'Online - Microsoft Teams',
                'is_online': True,
                'online_link': 'https://teams.microsoft.com/example',
                'max_attendees': 300,
                'days_from_now': 10
            },
            {
                'title': 'Alumni vs Students Cricket Match',
                'description': 'A friendly cricket match between alumni and current students. Come to play or cheer! Refreshments will be provided. Let the games begin!',
                'event_type': 'OTHER',
                'location': 'Sports Ground',
                'is_online': False,
                'max_attendees': 100,
                'days_from_now': 45
            }
        ]

        # Clear existing events
        Event.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing events'))

        # Create sample events
        created_count = 0
        for event_data in sample_events:
            event_date = timezone.now() + timedelta(days=event_data['days_from_now'])
            
            event = Event.objects.create(
                title=event_data['title'],
                description=event_data['description'],
                event_type=event_data['event_type'],
                date=event_date,
                end_date=event_date + timedelta(hours=3),
                location=event_data['location'],
                is_online=event_data['is_online'],
                online_link=event_data.get('online_link', ''),
                organizer=admin_user,
                max_attendees=event_data['max_attendees'],
                is_published=True
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample events!')
        )
