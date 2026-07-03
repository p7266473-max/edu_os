import reflex as rx

config = rx.Config(
    app_name="edu_os",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)