from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.core.files.storage import FileSystemStorage, default_storage
# Ensure this path is correct
from api.ml_model.Cr_Couting import counting


@api_view(["GET", "POST", "DELETE"])
def get_crowd(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        # return Response({"status": "GET request processed"})

    elif request.method == "POST":
        # return Response({"status": "POST request processed"})
        if "image" not in request.FILES:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = request.FILES["image"]
            fs = FileSystemStorage()
            filename = default_storage.save(image.name, image)
            uploaded_file_url = fs.path(filename)
            crowd_count = counting(uploaded_file_url)
            user = User(image=uploaded_file_url, crowd_count=crowd_count)
            user.save()
            time = user.time
            return Response({"status": "Image uploaded", "Crowd_Size": crowd_count, "Time": time}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            User.objects.all().delete()
            return Response({"status": "All images deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
