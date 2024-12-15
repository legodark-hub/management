from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from users.models import CustomUser
from users.serializers import RoleChangeSerializer


class ChangeUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_update = CustomUser.objects.get(id=user_id)

        if not request.user.is_superuser and request.user.role != "admin":
            raise PermissionDenied("Вы не можете менять роли пользователей.")

        serializer = RoleChangeSerializer(
            user_to_update, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Роль успешно обновлена.", "user": user_to_update.username, "role": user_to_update.role})
