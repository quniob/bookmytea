import fastapi_jsonrpc as jsonrpc
from bookmytea_core.app.api.client import client_entrypoint
from bookmytea_core.app.api.admin import admin_entrypoint

app = jsonrpc.API()

app.bind_entrypoint(client_entrypoint)
app.bind_entrypoint(admin_entrypoint)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', port=5000, access_log=False)
