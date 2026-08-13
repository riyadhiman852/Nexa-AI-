from aiohttp import web


from analytics import get_call_stats


async def stats(request):
    return web.json_response(
        get_call_stats(),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
        },
    )


async def options(request):
    return web.Response(
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )


app = web.Application()

app.router.add_get("/analytics", stats)
app.router.add_options("/analytics", options)


if __name__ == "__main__":
    web.run_app(
        app,
        host="127.0.0.1",
        port=8000,
    ) 