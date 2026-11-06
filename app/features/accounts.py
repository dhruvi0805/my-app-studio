"""APP-002 HTML and REST accounts share the prepared security services."""

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()


def _render(request, name, context=None, status=200):
    """Render a form with the synchronizer token and its corresponding cookie."""
    cookie = Response()
    token = security.csrf_token(request, cookie)
    response = request.app.state.templates.TemplateResponse(
        request=request,
        name=name,
        context={"csrf": token, **(context or {})},
        status_code=status,
    )
    for key, value in cookie.raw_headers:
        if key == b"set-cookie":
            response.raw_headers.append((key, value))
    return response


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response):
    """Start or reuse a same-origin session for state-changing requests."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post("/api/signup", response_model=PublicUser, status_code=201)
def api_signup(request: Request, credentials: SignupInput):
    """Create only members through the same service used by the HTML form."""
    security.require_csrf(request, request.headers.get("x-csrf-token"))
    security.limit_signup(request)
    return security.signup(request.app.state.settings, **credentials.model_dump())


@router.post("/api/login", response_model=PublicUser)
def api_login(request: Request, response: Response, credentials: LoginInput):
    """Return public identity while keeping the signed token in an HttpOnly cookie."""
    security.require_csrf(request, request.headers.get("x-csrf-token"))
    return security.login(request, response, **credentials.model_dump())


@router.get("/api/me", response_model=PublicUser)
def api_me(request: Request):
    """Require both a valid token and a current unrevoked database session."""
    return security.require_user(request)


@router.post("/api/logout")
def api_logout(request: Request):
    """Revoke on the server before clearing the browser cookie."""
    security.require_csrf(request, request.headers.get("x-csrf-token"))
    response = JSONResponse({"detail": "Logged out."})
    security.logout(request, response)
    return response


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Offer a bounded member signup form."""
    return _render(request, "account.html", {"mode": "signup"})


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """Offer login without disclosing whether a username exists."""
    return _render(request, "account.html", {"mode": "login"})


def _submit(request, mode, form):
    """Validate forms and run the same guarded services as JSON requests."""
    username = ""
    try:
        security.require_csrf(request, form.get("csrf_token"))
        pairs = list(form.multi_items())
        if len(pairs) != len({key for key, _ in pairs}):
            raise HTTPException(422, "Submit each field only once.")
        data = {key: value for key, value in pairs if key != "csrf_token"}
        model = SignupInput if mode == "signup" else LoginInput
        credentials = model.model_validate(data)
        username = credentials.username
        if mode == "signup":
            security.limit_signup(request)
            security.signup(request.app.state.settings, **credentials.model_dump())
            return RedirectResponse("/login", status_code=303)
        response = RedirectResponse("/dashboard", status_code=303)
        security.login(request, response, **credentials.model_dump())
        return response
    except ValidationError:
        error = (
            "Check your username and password lengths "
            "and submit only the requested fields."
        )
        status, headers = 422, {}
    except HTTPException as exc:
        error, status, headers = exc.detail, exc.status_code, exc.headers or {}
    response = _render(
        request,
        "account.html",
        {"mode": mode, "error": error, "username": username},
        status,
    )
    response.headers.update(headers)
    return response


@router.post("/signup", include_in_schema=False)
async def signup_form(request: Request):
    """Parse a small form, keeping expensive hashing off the event loop."""
    async with request.form(max_files=0, max_fields=4) as form:
        return await run_in_threadpool(_submit, request, "signup", form)


@router.post("/login", include_in_schema=False)
async def login_form(request: Request):
    """An unsuccessful login never reflects a password into the page."""
    async with request.form(max_files=0, max_fields=4) as form:
        return await run_in_threadpool(_submit, request, "login", form)


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Redirect anonymous browsers and show only the authenticated user's identity."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return _render(request, "dashboard.html", {"user": user})


@router.post("/logout", include_in_schema=False)
async def logout_form(request: Request):
    """HTML logout is a CSRF-protected POST, never a navigation GET."""
    async with request.form(max_files=0, max_fields=1) as form:
        security.require_csrf(request, form.get("csrf_token"))
    response = RedirectResponse("/login", status_code=303)
    await run_in_threadpool(security.logout, request, response)
    return response
