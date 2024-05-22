import fastapi_jsonrpc as jsonrpc
from bookmytea_auth.app.api.auth import api_entrypoint

app = jsonrpc.API()

app.bind_entrypoint(api_entrypoint)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', port=5000, access_log=False)
