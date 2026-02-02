This is the repo for Kazilen that contains all of the backend microservices, in 3 separate folders.
Backend frameworks used: 
1. Django Ninja
2. FastAPI (for location tracking)
3. SpringBoot (for payment and stuff)

## Django Ninja
```bash
cd djangoproj
gunicorn djangoproj.asgi:application -k uvicorn.workers.UvicornWorker
```
## FastAPI
```bash
cd fastapiproj
uvicorn main:app --reload
```
