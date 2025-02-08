from fastapi import FastAPI, HTTPException, Depends
from supabase import create_client, Client
from passlib.context import CryptContext
from typing import List, Optional, Type
from pydantic import BaseModel
from config import url, key
from models import Podcast, Publication, ContentSummary, GeneratedContent, User

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_supabase() -> Client:
    return create_client(url, key)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class CRUDService:
    def __init__(self, client: Client, table_name: str):
        self.client = client
        self.table_name = table_name

    async def create(self, data: BaseModel) -> dict:
        data_dict = data.dict()  # Changed from model_dump()
        data_dict.pop("id", None)
        try:
            response = self.client.table(self.table_name).insert(data_dict).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(400, detail=str(e))

    async def read_all(self) -> List[dict]:
        try:
            response = self.client.table(self.table_name).select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(400, detail=str(e))

    async def read_one(self, record_id: int) -> dict:
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .eq("id", record_id)
                .execute()
            )
            if not response.data:
                raise HTTPException(404, detail="Record not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(400, detail=str(e))

    async def update(self, record_id: int, data: BaseModel) -> dict:
        data_dict = data.dict()  # Changed from model_dump()
        data_dict.pop("id", None)
        try:
            response = (
                self.client.table(self.table_name)
                .update(data_dict)
                .eq("id", record_id)
                .execute()
            )
            return response.data[0]
        except Exception as e:
            raise HTTPException(400, detail=str(e))

    async def delete(self, record_id: int) -> dict:
        try:
            response = (
                self.client.table(self.table_name)
                .delete()
                .eq("id", record_id)
                .execute()
            )
            return {"status": "success", "message": "Record deleted"}
        except Exception as e:
            raise HTTPException(400, detail=str(e))


def get_crud_service(table_name: str, model: Type[BaseModel]):
    def crud_service(supabase: Client = Depends(get_supabase)):
        return CRUDService(supabase, table_name)

    return crud_service


podcast_crud = get_crud_service("podcasts", Podcast)
publication_crud = get_crud_service("publications", Publication)
summary_crud = get_crud_service("content_summaries", ContentSummary)
content_crud = get_crud_service("generated_content", GeneratedContent)


def create_crud_routes(prefix: str, model: Type[BaseModel], crud_dependency):
    @app.post(f"/{prefix}/", response_model=model)
    async def create_item(item: model, crud: CRUDService = Depends(crud_dependency)):
        return await crud.create(item)

    @app.get(f"/{prefix}/", response_model=List[model])
    async def read_items(crud: CRUDService = Depends(crud_dependency)):
        return await crud.read_all()

    @app.get(f"/{prefix}/{{item_id}}", response_model=model)
    async def read_item(item_id: int, crud: CRUDService = Depends(crud_dependency)):
        return await crud.read_one(item_id)

    @app.put(f"/{prefix}/{{item_id}}", response_model=model)
    async def update_item(
        item_id: int, item: model, crud: CRUDService = Depends(crud_dependency)
    ):
        return await crud.update(item_id, item)

    @app.delete(f"/{prefix}/{{item_id}}")
    async def delete_item(item_id: int, crud: CRUDService = Depends(crud_dependency)):
        return await crud.delete(item_id)


create_crud_routes("podcasts", Podcast, podcast_crud)
create_crud_routes("publications", Publication, publication_crud)
create_crud_routes("content_summaries", ContentSummary, summary_crud)
create_crud_routes("generated_content", GeneratedContent, content_crud)


@app.post("/users/", response_model=User)
async def create_user(user: User, supabase: Client = Depends(get_supabase)):
    try:
        user_data = user.dict()  # Changed here
        user_data["password"] = get_password_hash(user_data["password"])
        user_data.pop("id", None)
        response = supabase.table("users").insert(user_data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.get("/users/", response_model=List[User])
async def read_users(supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(404, detail="User not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int, user: User, supabase: Client = Depends(get_supabase)
):
    try:
        user_data = user.dict()  # Changed here
        if "password" in user_data:
            user_data["password"] = get_password_hash(user_data["password"])
        user_data.pop("id", None)
        response = supabase.table("users").update(user_data).eq("id", user_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return {"status": "success", "message": "User deleted"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Content Management API"}
