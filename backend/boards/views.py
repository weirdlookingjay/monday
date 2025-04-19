from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item, Group
from .serializers import TaskStatsSerializer, ItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    groups = Group.objects.all().values('id', 'name')
    return Response(list(groups))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create a new task (Item) in a board group."""
    from .models import Item, Group
    group_id = request.data.get('group')
    values = request.data.get('values', {})
    status = request.data.get('status', 'not_started')
    # Automatically determine the next available position in the group
    from django.db.models import Max
    if not group_id:
        return Response({'error': 'Group is required.'}, status=400)
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=404)
    max_position = Item.objects.filter(group=group).aggregate(Max('position'))['position__max']
    next_position = (max_position or 0) + 1
    item = Item.objects.create(
        group=group,
        created_by=request.user,
        values=values,
        status=status,
        position=next_position
    )
    from .serializers import ItemSerializer
    return Response(ItemSerializer(item).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_stats(request):
    """Get task statistics for the authenticated user's workspace."""
    # Get all items from boards in user's teams
    user_items = Item.objects.filter(
        group__board__workspace__team__members=request.user
    )

    # Calculate statistics
    total_tasks = user_items.count()
    tasks_in_progress = user_items.filter(status='in_progress').count()
    completed_tasks = user_items.filter(status='done').count()

    # Get tasks by status
    tasks_by_status = user_items.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    # Get 5 most recent tasks
    recent_tasks = user_items.order_by('-created_at')[:5]

    stats = {
        'total_tasks': total_tasks,
        'tasks_in_progress': tasks_in_progress,
        'completed_tasks': completed_tasks,
        'tasks_by_status': {
            item['status']: item['count'] 
            for item in tasks_by_status
        },
        'recent_tasks': ItemSerializer(recent_tasks, many=True).data
    }

    serializer = TaskStatsSerializer(stats)
    return Response(serializer.data)
