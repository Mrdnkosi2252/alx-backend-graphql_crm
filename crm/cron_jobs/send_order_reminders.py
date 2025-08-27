#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
import json

def send_order_reminders():
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    
    query = """
    query GetRecentOrders($since: String!) {
        orders(orderDate_Gte: $since) {
            id
            customer {
                email
            }
        }
    }
    """
    
    variables = {"since": seven_days_ago}
    
    try:
        
        response = requests.post(
            "http://localhost:8000/graphql",
            json={'query': query, 'variables': variables},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', {}).get('orders', [])
            
            # Log results
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('/tmp/order_reminders_log.txt', 'a') as f:
                f.write(f"[{timestamp}] Found {len(orders)} orders from the last 7 days:\n")
                for order in orders:
                    f.write(f"Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")
            
            print("Order reminders processed!")
        else:
            print(f"Error: Received status code {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_order_reminders()