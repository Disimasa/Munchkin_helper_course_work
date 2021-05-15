from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
import starlette
import uvicorn
from pprint import pp

from test import A


print(starlette.__version__)


async def index(request: Request):
    # pp(await request.json())
    return PlainTextResponse('Hello world!')

# app = Starlette(routes=[Route('/test0', index)])
a = A()
app = a.app


@app.route('/t1')
async def t1(request: Request):
    return PlainTextResponse('Hello world1!')


@app.route('/t2')
async def t2(request: Request):
    return PlainTextResponse('Hello world2!')


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
