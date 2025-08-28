import requests
from datetime import datetime, timedelta


query = """
query GetRecentOrders {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
"""


seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
endpoint = "http://localhost:8000/graphql"

try:
    response = requests.post(
        endpoint,
        json={'query': query % seven_days_ago},
        headers={'Content-Type': 'application/json'}
    )
    orders = response.json()['data']['orders']
    
    
    with open('/tmp/order_reminders_log.txt', 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Found {len(orders)} orders\n")
        for order in orders:
            f.write(f"Order {order['id']} - Customer: {order['customer']['email']}\n")
            
    print("Order reminders processed!")
except Exception as e:
    print(f"Error: {str(e)}")