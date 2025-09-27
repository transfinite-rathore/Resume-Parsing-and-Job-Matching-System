from fastapi import HTTPException
from functools import wraps

def handle_try_except(f):
    @wraps(f)
    async def wrapper(*args,**kwargs):
        try:
            result=f(*args,**kwargs)
            if hasattr(result,"__await__"):
                result=await result
            return result

            # return await f(*args,**kwargs) if f is Callable else f(*args,**kwargs)
        except HTTPException:
            raise 
        except Exception as e:
            raise HTTPException(status_code=501,detail=f"Task Failed {e}")
    return wrapper