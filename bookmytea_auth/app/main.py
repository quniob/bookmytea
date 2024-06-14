import os

import fastapi_jsonrpc as jsonrpc
from app.api.auth import api_entrypoint
from dotenv import load_dotenv, find_dotenv

app = jsonrpc.API()

app.bind_entrypoint(api_entrypoint)

if __name__ == '__main__':
    import uvicorn

    load_dotenv(find_dotenv())
    uvicorn.run('main:app', port=int(os.environ.get("PORT")), access_log=False, host="0.0.0.0")
