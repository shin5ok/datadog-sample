from fastapi import FastAPI, Request, Path
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/env")
async def get_env_and_headers(request: Request):
    env_vars = dict(os.environ)
    headers = dict(request.headers)
    return JSONResponse({"env": env_vars, "headers": headers})

@app.get("/env/{key}")
async def get_env_or_header_by_key(request: Request, key: str = Path(...)):
    env_vars = dict(os.environ)
    headers = dict(request.headers)
    result = {}
    key_lower = key.lower()
    for k, v in env_vars.items():
        if k.lower() == key_lower:
            result[k] = v
    for k, v in headers.items():
        if k.lower() == key_lower:
            result[k] = v
    return JSONResponse(result)

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
