import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ContactInquiry


@csrf_exempt
@require_http_methods(["POST"])
def submit_contact_inquiry(request):
    try:
        data = json.loads(request.body)

        required_fields = ["first_name", "last_name", "email", "subject", "message"]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {"status": "error", "message": f"{field} is required"},
                    status=400,
                )

        inquiry = ContactInquiry.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data.get("phone", ""),
            subject=data["subject"],
            message=data["message"],
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "Contact inquiry submitted successfully",
                "inquiry_id": inquiry.id,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON data"}, status=400
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": f"An error occurred while processing your request: {str(e)}",
            },
            status=500,
        )
