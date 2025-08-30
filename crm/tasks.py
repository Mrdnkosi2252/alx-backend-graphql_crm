
from celery import shared_task
from django.utils import timezone
import json

@shared_task
def generate_crm_report():
    """
    Generate a CRM report and log it to /tmp/crm_report_log.txt
    """
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    report_data = {
        "timestamp": timestamp,
        "report_type": "CRM System Report",
        "status": "completed",
        "metrics": {
            "total_customers": 150,
            "total_orders": 450,
            "total_products": 75
        }
    }
    
    
    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(f"[{timestamp}] CRM Report Generated\n")
        f.write(f"Report Data: {json.dumps(report_data, indent=2)}\n")
        f.write("-" * 50 + "\n")
    
    return f"CRM report generated at {timestamp}"
