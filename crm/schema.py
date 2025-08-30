import graphene
from graphene_django import DjangoObjectType
from crm.models import Product  

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock", "price")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        
        updated_products = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Updated {len(updated_products)} products with low stock"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    
    def resolve_hello(self, info):
        return "Hello from GraphQL CRM!"

schema = graphene.Schema(query=Query, mutation=Mutation)
