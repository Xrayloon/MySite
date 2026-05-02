from fastapi import APIRouter


router = APIRouter(tags=['auth'])

@router.post('/auth/register')
async def User_Register():
    pass
