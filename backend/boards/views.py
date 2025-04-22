from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item, Group
from .serializers import TaskStatsSerializer, ItemSerializer, SimpleUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    User = get_user_model()
    users = User.objects.all()
    serializer = SimpleUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    groups = Group.objects.all().values('id', 'name')
    return Response(list(groups))

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=404)
    name = request.data.get('name')
    color = request.data.get('color')
    updated = False
    if name:
        group.name = name
        updated = True
    if color:
        group.color = color
        updated = True
    if updated:
        group.save()
    return Response({'id': group.id, 'name': group.name, 'color': group.color, 'board': group.board.id})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=404)
    group.delete()
    return Response({'success': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_boards(request):
    
    from .models import Board
    # Return all fields needed for the frontend kanban
    boards = Board.objects.filter(workspace__team__members=request.user).select_related('assignee').values(
        'id', 'name', 'description', 'status', 'created_at', 'updated_at',
        'assignee', 'assignee__first_name', 'assignee__last_name', 'assignee__email'
    )
    return Response(list(boards))

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_board(request, board_id):
    from .models import Board, Item
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found.'}, status=404)
    # Check if any open (not done) tasks exist in this board
    open_tasks = Item.objects.filter(group__board=board).exclude(status='done').exists()
    if open_tasks:
        return Response({'error': 'Cannot delete board with open tasks. Please complete or remove all open tasks first.'}, status=400)
    board.delete()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board(request):
    from .models import Board
    from accounts.models import User
    name = request.data.get('name')
    description = request.data.get('description', '')
    assignee_id = request.data.get('assignee')
    workspace = request.user.workspace_set.first()
    if not name:
        return Response({'error': 'Name is required'}, status=400)
    assignee = None
    if assignee_id:
        try:
            assignee = User.objects.get(id=assignee_id)
        except User.DoesNotExist:
            return Response({'error': 'Assignee not found'}, status=400)
    else:
        assignee = request.user
    board = Board.objects.create(name=name, description=description, workspace=workspace, created_by=request.user, assignee=assignee)
    return Response({'id': board.id, 'name': board.name, 'description': board.description, 'assignee': board.assignee.id if board.assignee else None}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    from .models import Group, Board
    name = request.data.get('name')
    board_id = request.data.get('board')
    if not name or not board_id:
        return Response({'error': 'Name and board are required'}, status=400)
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found'}, status=404)
    group = Group.objects.create(name=name, board=board)
    return Response({'id': group.id, 'name': group.name, 'board': board.id}, status=201)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task(request, item_id):
    from .models import Item, Group
    from .serializers import ItemSerializer
    from activity.models import ActivityLog
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=404)

    data = request.data.copy()
    changed_fields = []
    # Allow updating values (name, description, due_date, assignee, etc.)
    if 'values' in data:
        item.values.update(data['values'])
        changed_fields.append('values')
    if 'status' in data:
        item.status = data['status']
        changed_fields.append('status')
    if 'group' in data:
        try:
            group = Group.objects.get(id=data['group'])
            item.group = group
            changed_fields.append('group')
        except Group.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=404)
    item.save()
    # Log activity
    if changed_fields:
        ActivityLog.objects.create(
            user=request.user,
            action='updated',
            task=item,
            details=f"Task updated: {', '.join(changed_fields)}"
        )
    return Response(ItemSerializer(item).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create a new task (Item) in a board group."""
    from .models import Item, Group
    from activity.models import ActivityLog
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
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action='created',
        task=item,
        details=f"Task '{values.get('name', '')}' created in group '{group.name}'"
    )
    from .serializers import ItemSerializer
    return Response(ItemSerializer(item).data, status=201)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_board(request, board_id):
    from .models import Board
    from accounts.models import User
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found.'}, status=404)
    data = request.data
    updated = False
    if 'status' in data:
        board.status = data['status']
        updated = True
    if 'name' in data:
        board.name = data['name']
        updated = True
    if 'description' in data:
        board.description = data['description']
        updated = True
    if 'assignee' in data:
        assignee_id = data['assignee']
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                board.assignee = assignee
                updated = True
            except User.DoesNotExist:
                return Response({'error': 'Assignee not found'}, status=400)
        else:
            board.assignee = None
            updated = True
    if updated:
        board.save()
    return Response({'id': board.id, 'status': board.status, 'name': board.name, 'description': board.description, 'assignee': board.assignee.id if board.assignee else None})

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
