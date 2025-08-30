#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import json

def send_order_reminders():
    
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        use_json=True,
        headers={
            "Content-Type": "application/json",
        },
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')
    
    
    query = gql("""
    query GetRecentOrders($since: String!) {
        orders(orderDate_Gte: $since) {
            id
            customer {
                email
            }
        }
    }
    """)
    
    variables = {"since": seven_days_ago}
    
    try:
        
        result = client.execute(query, variable_values=variables)
        orders = result.get('orders', [])
        
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Found {len(orders)} orders from the last 7 days:\n")
            for order in orders:
                f.write(f"Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")
        
        print("Order reminders processed!")
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Error: {str(e)}\n")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_order_reminders()
