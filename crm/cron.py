from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = timezone.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
    
    
    try:
        
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            headers={'Content-Type': 'application/json'}
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        hello_message = result.get('hello', 'No hello response')
        
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} GraphQL endpoint is responsive: {hello_message}\n")
            
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} Error checking GraphQL endpoint: {str(e)}\n")

def update_low_stock():
    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport
    
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            headers={'Content-Type': 'application/json'}
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    products {
                        name
                        stock
                    }
                    message
                }
            }
        """)
        
        result = client.execute(mutation)
        update_result = result.get('data', {}).get('updateLowStockProducts', {})
        
        
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] {update_result.get('message', 'No message')}\n")
            for product in update_result.get('products', []):
                f.write(f"Product: {product.get('name', 'Unknown')}, Stock: {product.get('stock', 0)}\n")
                
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Error: {str(e)}\n")
