"""APP-003 protects project status with the current server-side account role."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app import security

router = APIRouter()


def _project_status(request):
    """Share a small project summary without runtime paths or account/session data."""
    return {
        "project": request.app.state.brand()["name"],
        "status": "Local learning project",
        "available": ["Branded homepage", "Member accounts", "Server-enforced roles"],
        "planned": "Budgeting tools remain concepts.",
    }


@router.get("/api/admin")
def admin_status(request: Request):
    """Direct requests must pass authorization before receiving project status."""
    security.require_admin(request)
    return _project_status(request)


@router.get("/admin", include_in_schema=False)
def admin_page(request: Request):
    """Redirect anonymous browsers and show members an actual forbidden response."""
    try:
        user = security.require_admin(request)
    except HTTPException as error:
        if error.status_code == 401:
            return RedirectResponse("/login", status_code=303)
        if error.status_code != 403:
            raise
        return request.app.state.templates.TemplateResponse(
            request=request, name="forbidden.html", context={}, status_code=403
        )
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"user": user, "project_status": _project_status(request)},
    )
