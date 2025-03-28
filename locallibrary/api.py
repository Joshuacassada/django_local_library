from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from catalog.models import Author, Genre, Language
from typing import List
from pydantic import BaseModel

api = NinjaAPI()

# Schema for Author
class AuthorSchema(BaseModel):
    first_name: str
    last_name: str

# CRUD for Authors
@api.get("/authors", response=List[AuthorSchema])
def list_authors(request):
    return list(Author.objects.values("first_name", "last_name"))

@api.post("/authors")
def create_author(request, payload: AuthorSchema):
    author = Author.objects.create(**payload.dict())
    return {"id": author.id, "first_name": author.first_name, "last_name": author.last_name}

@api.get("/authors/{author_id}", response=AuthorSchema)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return {"first_name": author.first_name, "last_name": author.last_name}

@api.put("/authors/{author_id}")
def update_author(request, author_id: int, payload: AuthorSchema):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.delete("/authors/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}

# Schema for Language
class LanguageSchema(BaseModel):
    name: str

# CRUD for Languages
@api.get("/languages", response=List[LanguageSchema])
def list_languages(request):
    return list(Language.objects.values("name"))

@api.post("/languages")
def create_language(request, payload: LanguageSchema):
    language = Language.objects.create(**payload.dict())
    return {"id": language.id, "name": language.name}

@api.delete("/languages/{language_id}")
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}
