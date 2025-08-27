from django.utils import timezone
import requests
import json

def log_crm_heartbeat():
    timestamp = timezone.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
    
    
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={'query': 'query { hello }'},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'hello' in data['data']:
                with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                    f.write(f"{timestamp} GraphQL endpoint is responsive: {data['data']['hello']}\n")
            else:
                with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                    f.write(f"{timestamp} GraphQL endpoint returned unexpected response: {data}\n")
        else:
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint returned status code: {response.status_code}\n")
                
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} Error checking GraphQL endpoint: {str(e)}\n")


def update_low_stock():
    mutation = """
    mutation {
        updateLowStockProducts {
            products {
                name
                stock
            }
            message
        }
    }
    """
    
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={'query': mutation},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('data', {}).get('updateLowStockProducts', {})
            
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] {result.get('message', 'No message')}\n")
                for product in result.get('products', []):
                    f.write(f"Product: {product.get('name', 'Unknown')}, Stock: {product.get('stock', 0)}\n")
        else:
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] Error: Received status code {response.status_code}\n")
                
    except Exception as e:
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Error: {str(e)}\n")           