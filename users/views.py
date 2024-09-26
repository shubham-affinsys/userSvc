import json
import pprint
import logging
import users.db as db
from django.db import DatabaseError
from utils import rabbitmq_pub,addMeta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger("app")

def all_users(request):	
    try:
        logger.info(f"inside api request is {request}")
        users=db.get_user()
        data =  addMeta.add_metadata(users)
        logger.debug(f"data sent is:====>  {data}")
        return HttpResponse(json.dumps(data),content_type="application/json")
    except ObjectDoesNotExist as e:
        # Handle case when no users are found or invalid query
        logger.error(f"Error: User data not found: {e}")
        return JsonResponse(
            {"error": "No user data found or invalid query."},
            status=404
        )

    except DatabaseError as e:
        # Handle database-related errors
        logger.error(f"Database error while fetching users: {e}")
        return JsonResponse(
            {"error": "Database error. Please try again later."},
            status=500
        )

    except json.JSONDecodeError as e:
        # Handle JSON serialization errors
        logger.error(f"JSON serialization error: {e}")
        return JsonResponse(
            {"error": "Error processing data. Invalid format."},
            status=500
        )

    except Exception as e:
        # Handle any other unexpected exceptions
        logger.error(f"An unexpected error occurred: {e}")
        return JsonResponse(
            {"error": "An unexpected error occurred. Please try again later."},
            status=500
        )

@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            logger.debug(f"Data received inside API: {data}")

            # Call your function to create a user in the database
            db_response = db.create_user(data)  # Assuming `create_user` accepts a dictionary
            
            if db_response == "could not create user":
                return Response({
                    'message': "Could not create user"
                }, status=400)
            
            rabbitmq_pub.publish_message(f"user has been created successfully {request.body} ")
            return Response({
                'message': "User added successfully"
            }, status=201)  # 201 Created
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return Response({
                'message': "Invalid JSON data"
            }, status=400)

        except Exception as e:
            logger.error(f"Could not create user: {str(e)}")
            return Response({
                'message': "Could not create user"
            }, status=500)  # 500 Internal Server Error
    