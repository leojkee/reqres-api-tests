from pydantic import BaseModel


class ProductData(BaseModel):
    id: int
    title: str
    price: float
    category: str


class ProductListResponse(BaseModel):
    products: list[ProductData]
    total: int
    skip: int
    limit: int


class CreateProductResponse(BaseModel):
    id: int
    title: str
    price: float
    category: str
