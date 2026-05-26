def error_template(title: str, message: str, btn_title: str, btn_link: str):
    return (
        f"""
    <!doctype html>
    <html lang="ko">
        <head>
            <meta charset="utf-8">
            <title>{title} — dreamschool</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <link rel="stylesheet" href="""
        "{{ url_for('static', filename='css/main.css') }}"
        f""">
        </head>
        <body>
            <div class="main wrapper">
            <img class="form-logo" onclick="location.href='/'" src="""
        "{{ url_for('static', filename='img/logo.svg') }}"
        f""">
            <div class="card" method="post">
                <h1>{title}</h1>
                <p>{message}<p>
                <a class='button' href='{btn_link}'>{btn_title}</a>
            </div>
            </div>
        </body>
    </html>"""
    )
