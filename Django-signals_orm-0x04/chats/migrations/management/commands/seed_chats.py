from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from chats.models import User, Conversation, Message
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample data for chats application'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()
        self.user_count = 20
        self.conversation_count = 10
        self.messages_per_conversation = (5, 30)  # min, max

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.flush_data()
            
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        # Create groups and permissions
        groups = self.create_groups_and_permissions()
        
        # Create users
        users = self.create_users(groups)
        
        # Create conversations with participants
        conversations = self.create_conversations(users)
        
        # Create messages
        self.create_messages(conversations, users)
        
        self.stdout.write(self.style.SUCCESS(f'''
            Database seeding completed successfully!
            - Users: {len(users)}
            - Conversations: {len(conversations)}
            - Messages: {Message.objects.count()}
        '''))

    def flush_data(self):
        self.stdout.write(self.style.WARNING('Flushing existing data...'))
        models = [User, Group, Conversation, Message]
        for model in models:
            model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data flushed.'))

    def create_groups_and_permissions(self):
        self.stdout.write('Creating groups and permissions...')
        
        groups = {
            'admin': Group.objects.get_or_create(name='Admins')[0],
            'premium': Group.objects.get_or_create(name='Premium Users')[0],
            'regular': Group.objects.get_or_create(name='Regular Users')[0]
        }
        
        # Create custom permissions
        content_type = ContentType.objects.get_for_model(User)
        
        permissions = [
            Permission.objects.get_or_create(
                codename='can_chat_unlimited',
                name='Can chat without restrictions',
                content_type=content_type
            )[0],
            Permission.objects.get_or_create(
                codename='can_create_group_chats',
                name='Can create group chats',
                content_type=content_type
            )[0],
            Permission.objects.get_or_create(
                codename='can_delete_messages',
                name='Can delete messages',
                content_type=content_type
            )[0]
        ]
        
        # Assign permissions to groups
        groups['admin'].permissions.add(*permissions)
        groups['premium'].permissions.add(permissions[0], permissions[1])
        
        return groups

    def create_users(self, groups):
        self.stdout.write(f'Creating {self.user_count} users...')
        
        # Create admin user
        admin = User.objects.create_superuser(
            username='Admin',
            email='admin@jmc.com',
            password='admin123',
            first_name='Khalfani',
            last_name='Athman',
            phone_number='+254712345678',
            is_active=True,
            is_staff=True
        )
        admin.groups.add(groups['admin'])
        
        users = [admin]
        
        # Create regular users
        for i in range(1, self.user_count):
            is_premium = random.random() < 0.3  # 30% chance of being premium
            
            user = User.objects.create_user(
                username=self.faker.unique.user_name(),
                email=self.faker.unique.email(),
                password='password123',
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                phone_number=self.faker.phone_number(),
                is_active=True
            )
            
            if is_premium:
                user.groups.add(groups['premium'])
            else:
                user.groups.add(groups['regular'])
            
            users.append(user)
            
            if i % 5 == 0:
                self.stdout.write(f'Created {i} users...')
        
        return users

    def create_conversations(self, users):
        self.stdout.write(f'Creating {self.conversation_count} conversations...')
        
        conversations = []
        
        for i in range(self.conversation_count):
            # Determine conversation type (1:1 or group)
            is_group = random.random() < 0.4  # 40% chance of being a group chat
            participant_count = random.randint(2, 8) if is_group else 2
            
            participants = random.sample(users, participant_count)
            conversation_name = None
            
            if is_group:
                conversation_name = self.faker.catch_phrase()
            
            conversation = Conversation.objects.create(
                name=conversation_name
            )
            conversation.participants.add(*participants)
            conversations.append(conversation)
            
            if i % 2 == 0:
                self.stdout.write(f'Created {i} conversations...')
        
        return conversations
    def create_messages(self, conversations, users):
        self.stdout.write('Creating messages...')
        total_messages = 0
        
        for conversation in conversations:
            participants = list(conversation.participants.all())
            message_count = random.randint(*self.messages_per_conversation)
            
            for i in range(message_count):
                sender = random.choice(participants)
                sent_at = timezone.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                # Create message with conversation reference
                message = Message.objects.create(
                    conversation=conversation,  # This is required
                    message_body=self.faker.text(max_nb_chars=random.randint(10, 500)),
                    sent_at=sent_at,
                    sender=sender
                )
                # Remove the M2M add since it's not needed
                # conversation.messages.add(message)  # This line should be removed
            
            total_messages += message_count
            self.stdout.write(f'Created {total_messages} messages...', ending='\r')
        
        self.stdout.write('')
    # def create_messages(self, conversations, users):
    #     self.stdout.write('Creating messages...')
        
    #     total_messages = 0
        
    #     for conversation in conversations:
    #         participants = list(conversation.participants.all())
    #         message_count = random.randint(*self.messages_per_conversation)
            
    #         for i in range(message_count):
    #             sender = random.choice(participants)
    #             sent_at = timezone.now() - timedelta(
    #                 days=random.randint(0, 30),
    #                 hours=random.randint(0, 23),
    #                 minutes=random.randint(0, 59)
    #             )
                
    #             # Create message without conversation reference
    #             message = Message.objects.create(
    #                 message_body=self.faker.text(max_nb_chars=random.randint(10, 500)),
    #                 sent_at=sent_at,
    #                 sender=sender
    #             )
                
    #             # Add message to conversation through M2M
    #             conversation.messages.add(message)
            
    #         total_messages += message_count
    #         self.stdout.write(f'Created {total_messages} messages...', ending='\r')
        
    #     self.stdout.write('') 