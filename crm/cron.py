from django.utils import timezone
import requests

def log_crm_heartbeat():
    timestamp = timezone.now().strftime("%d/%m/%Y-%H:%M:%S")

    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")

    
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={'query': 'query { hello }'},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise Exception(f"GraphQL endpoint not healthy: {response.status_code} - {response.text}")
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} Health check failed: {str(e)}\n")


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

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={'query': mutation},
            headers={'Content-Type': 'application/json'}
        )

        data = response.json()
        if 'data' in data and 'updateLowStockProducts' in data['data']:
            result = data['data']['updateLowStockProducts']
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] {result['message']}\n")
                for product in result['products']:
                    f.write(f"Updated {product['name']} to {product['stock']} units\n")
        else:
            raise Exception("Unexpected GraphQL response format")

    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Error: {str(e)}\n")
