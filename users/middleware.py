# from rest_framework.response import Response
# from django.http import JsonResponse

# def custom_auth_middleware(get_response):
#     print("Authentication Middleware Gateway ..... 🏰")

#     def wrapper(request):

#         user = request.user

#         if request.path.startswith("/api/token/"):
#             response = get_response(request)
#             print(response)
#             return response

        
#         # if not user.is_authenticated:
#         #     print("Access Blocked..... ❌❌")
#         #     return JsonResponse({"Unauthorized" : "This route is unauthorized. . . "},status=401) 
        
#         print("Authentication Middleware Passed . . . .✅ ✅")

#         response = get_response(request)
#         return response
    
    #return wrapper
