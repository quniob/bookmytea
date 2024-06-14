import fastapi_jsonrpc as jsonrpc
from app.api.client import client_entrypoint
from app.api.admin import admin_entrypoint
from app.db.settings import PORT

app = jsonrpc.API()

app.bind_entrypoint(client_entrypoint)
app.bind_entrypoint(admin_entrypoint)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', port=PORT, access_log=False, host="0.0.0.0")
