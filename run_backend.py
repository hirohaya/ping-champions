#!/usr/bin/env python#!/usr/bin/env python

"""Backend server runner with proper path setup""""""Backend server runner with proper path setup"""

import sysimport sys

import osimport os



# Add backend to path# Add backend to path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))



if __name__ == '__main__':if __name__ == '__main__':

    import uvicorn    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

