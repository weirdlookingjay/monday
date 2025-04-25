from django.core.management.base import BaseCommand
from automation.models import AutomationCategory, AutomationTemplate
from boards.models import Board
from accounts.models import User

class Command(BaseCommand):
    help = 'Seeds the database with a default automation category, template, and board for testing.'

    def handle(self, *args, **options):
        # Get or create a user (assume user with id=2 exists)
        user = User.objects.get(id=2)

        # Delete all current templates
        AutomationTemplate.objects.all().delete()
        self.stdout.write(self.style.WARNING('Deleted all existing AutomationTemplates.'))

        # Create categories
        basic_cat, _ = AutomationCategory.objects.get_or_create(name="Basic", slug="basic", icon="icon-basic")
        notify_cat, _ = AutomationCategory.objects.get_or_create(name="Notifications", slug="notifications", icon="icon-notify")
        due_cat, _ = AutomationCategory.objects.get_or_create(name="Due Dates", slug="due-dates", icon="icon-due")

        # Create a Custom template for blank automations
        custom_cat, _ = AutomationCategory.objects.get_or_create(name="Custom", slug="custom", icon="icon-custom")
        custom_template, _ = AutomationTemplate.objects.get_or_create(
            category=custom_cat,
            name="Custom",
            defaults={
                "description": "A blank template for building custom automations from scratch.",
                "supports_subitems": False,
                "config_schema": {},
                "default_conditions": []
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Custom template ID: {custom_template.id}"))

        # Create 3 meaningful templates
        t1 = AutomationTemplate.objects.create(
            category=basic_cat,
            name="When status changes to Done, notify manager",
            description="Automatically notifies the manager when a task's status is set to Done.",
            supports_subitems=False,
            config_schema={},
            default_conditions=[{"field": "status", "operator": "equals", "value": "Done"}]
        )
        t2 = AutomationTemplate.objects.create(
            category=notify_cat,
            name="When item is created, assign to team lead",
            description="Assigns new items to the team lead upon creation.",
            supports_subitems=False,
            config_schema={},
            default_conditions=[{"field": "event", "operator": "equals", "value": "created"}]
        )
        t3 = AutomationTemplate.objects.create(
            category=due_cat,
            name="When due date arrives, notify assignee",
            description="Sends a notification to the assignee when the due date is reached.",
            supports_subitems=False,
            config_schema={},
            default_conditions=[{"field": "due_date", "operator": "arrives", "value": "today"}]
        )
        self.stdout.write(self.style.SUCCESS(f"Created templates: {t1.name}, {t2.name}, {t3.name}"))

        # Create or get a board
        board, created_board = Board.objects.get_or_create(
            name="Test Board",
            defaults={'created_by': user}
        )
        self.stdout.write(self.style.SUCCESS(f"Board ID: {board.id}"))

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
