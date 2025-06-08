from fastapi import FastAPI, Request, Path
from fastapi.responses import JSONResponse
import os
from ddtrace import patch_all
from ddtrace.trace import tracer
from ddtrace.ext import http

patch_all()

app = FastAPI()

@app.get("/env")
async def get_env_and_headers(request: Request):
    with tracer.trace("env.get_all", service="fastapi-app") as span:
        span.set_tag("operation.name", "get_environment_and_headers")
        span.set_tag("endpoint", "/env")
        
        with tracer.trace("env.collect_environment") as env_span:
            env_vars = dict(os.environ)
            env_span.set_tag("env.count", len(env_vars))
        
        with tracer.trace("env.collect_headers") as header_span:
            headers = dict(request.headers)
            header_span.set_tag("headers.count", len(headers))
            header_span.set_tag(http.USER_AGENT, headers.get("user-agent", "unknown"))
        
        span.set_tag("response.total_items", len(env_vars) + len(headers))
        return JSONResponse({"env": env_vars, "headers": headers})

@app.get("/env/{key}")
async def get_env_or_header_by_key(request: Request, key: str = Path(...)):
    with tracer.trace("env.get_by_key", service="fastapi-app") as span:
        span.set_tag("operation.name", "get_environment_or_header_by_key")
        span.set_tag("endpoint", "/env/{key}")
        span.set_tag("search.key", key)
        
        result = {}
        key_lower = key.lower()
        
        with tracer.trace("env.search_environment") as env_span:
            env_vars = dict(os.environ)
            env_span.set_tag("env.total_count", len(env_vars))
            env_matches = 0
            for k, v in env_vars.items():
                if k.lower() == key_lower:
                    result[k] = v
                    env_matches += 1
            env_span.set_tag("env.matches_found", env_matches)
        
        with tracer.trace("env.search_headers") as header_span:
            headers = dict(request.headers)
            header_span.set_tag("headers.total_count", len(headers))
            header_span.set_tag(http.USER_AGENT, headers.get("user-agent", "unknown"))
            header_matches = 0
            for k, v in headers.items():
                if k.lower() == key_lower:
                    result[k] = v
                    header_matches += 1
            header_span.set_tag("headers.matches_found", header_matches)
        
        total_matches = len(result)
        span.set_tag("search.total_matches", total_matches)
        span.set_tag("search.found", total_matches > 0)
        
        return JSONResponse(result)

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
