import pandera as pa
from pandera.typing import DataFrame, Series

class ProductSchema(pa.SchemaModel):
    """
    Define the schema to validate the data of products with Pandera.

    Attributes:
        id_product (Series[int]): Identificator of the product
        name (Series[str]): Product name
        quantity (Series[int]): Available quantity of the product, must be grater or equal 0.
        price (Series[float]): Price of the product,  must be between 5.0 and 120.0.
        category (Series[str]): Product's category.
    """
    id_product: Series[int]      
    name: Series[str]
    quantity: Series[int] = pa.Field(ge=0)
    price: Series[float] = pa.Field(ge=05.0, le=120.0)
    category: Series[str]

    class Config:
        coerce = True
        strict = True

class ProductSchemaKPI(ProductSchema):

    stock_total_price: Series[float] = pa.Field(ge=0)  # must be greater than zero
    normalized_category: Series[str] 
    availability: Series[bool]  