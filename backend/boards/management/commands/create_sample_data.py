from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from boards.models import Board, Group, Item
from workspace.models import Workspace
from accounts.models import Team, TeamMember
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()

        # Create team
        team, created = Team.objects.get_or_create(
            name='Test Team'
        )
        TeamMember.objects.get_or_create(
            team=team,
            user=user,
            defaults={'role': 'admin'}
        )

        # Create workspace
        workspace, created = Workspace.objects.get_or_create(
            name='Test Workspace',
            defaults={
                'created_by': user,
                'team': team
            }
        )

        # Create board
        board, created = Board.objects.get_or_create(
            name='Test Board',
            workspace=workspace,
            defaults={
                'created_by': user,
                'description': 'A test board with sample tasks'
            }
        )

        # Create groups
        groups = []
        for name, color in [
            ('To Do', '#ff4444'),
            ('In Progress', '#ffbb33'),
            ('Done', '#00C851')
        ]:
            group, created = Group.objects.get_or_create(
                board=board,
                name=name,
                defaults={
                    'color': color,
                    'position': len(groups)
                }
            )
            groups.append(group)

        # Create sample tasks
        statuses = ['not_started', 'in_progress', 'done', 'stuck']
        task_names = [
            'Design new landing page',
            'Implement user authentication',
            'Write API documentation',
            'Fix navigation bug',
            'Update dependencies',
            'Add dark mode support',
            'Optimize database queries',
            'Write unit tests',
            'Deploy to staging',
            'Code review'
        ]

        # Clear existing items
        Item.objects.filter(group__board=board).delete()

        # Create new items
        for i, task_name in enumerate(task_names):
            status = random.choice(statuses)
            group = groups[1] if status == 'in_progress' else groups[2] if status == 'done' else groups[0]
            
            created_at = datetime.now() - timedelta(days=random.randint(0, 14))
            
            Item.objects.create(
                group=group,
                created_by=user,
                status=status,
                position=i,
                values={'name': task_name},
                created_at=created_at
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
