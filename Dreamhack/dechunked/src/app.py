import os

from aiohttp import web
from jinja2 import Environment


MAX_BODY_SIZE = 512
MAX_RENDER_SIZE = 4096

jinja_env = Environment(autoescape=False)


async def index(_request: web.Request) -> web.Response:
    body = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Template Preview Service</title>
  <style>
    :root {
      color-scheme: light dark;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: #f3f5f7;
      color: #1d252d;
    }
    main {
      width: min(720px, calc(100vw - 40px));
      padding: 36px 0;
    }
    h1 {
      margin: 0 0 14px;
      font-size: 32px;
      font-weight: 700;
      letter-spacing: 0;
    }
    p {
      margin: 8px 0;
      font-size: 16px;
      line-height: 1.6;
    }
    code {
      padding: 2px 6px;
      border-radius: 4px;
      background: #e7ebef;
    }
    @media (prefers-color-scheme: dark) {
      body {
        background: #101418;
        color: #e6edf3;
      }
      code {
        background: #252c34;
      }
    }
  </style>
</head>
<body>
  <main>
    <h1>Template Preview Service</h1>
    <p>Submit a raw text template and preview the rendered result.</p>
    <p>The preview endpoint accepts <code>POST /preview</code> with <code>Content-Type: text/plain</code>.</p>
  </main>
</body>
</html>
"""
    return web.Response(text=body, content_type="text/html", charset="utf-8")


async def preview(request: web.Request) -> web.Response:
    content_type = request.headers.get("Content-Type", "")
    if content_type.split(";", 1)[0].strip().lower() != "text/plain":
        return web.Response(status=415, text="text/plain required\n")

    try:
        body = await request.read()
    except web.HTTPRequestEntityTooLarge:
        return web.Response(status=413, text="template too large\n")
    except ConnectionResetError:
        return web.Response(status=400, text="bad request\n")

    if len(body) > MAX_BODY_SIZE:
        return web.Response(status=413, text="template too large\n")

    try:
        source = body.decode("utf-8")
    except UnicodeDecodeError:
        return web.Response(status=400, text="invalid utf-8\n")

    try:
        rendered = jinja_env.from_string(source).render()
    except Exception:
        return web.Response(status=400, text="render error\n")

    if len(rendered) > MAX_RENDER_SIZE:
        rendered = rendered[:MAX_RENDER_SIZE]

    return web.Response(text=rendered, content_type="text/plain", charset="utf-8")


def make_app() -> web.Application:
    app = web.Application(client_max_size=MAX_BODY_SIZE)
    app.router.add_get("/", index)
    app.router.add_post("/preview", preview)
    return app


if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", "8080"))
    web.run_app(make_app(), host=host, port=port, print=None)
