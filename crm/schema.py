class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        from products.models import Product
        
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []
        
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
            
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Updated {len(updated_products)} products"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
    