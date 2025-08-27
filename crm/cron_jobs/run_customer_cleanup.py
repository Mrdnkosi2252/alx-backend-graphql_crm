import os
import django
from datetime import timedelta
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

from customers.models import Customer, Order
from django.db.models import OuterRef, Exists


one_year_ago = timezone.now() - timedelta(days=365)


recent_orders = Order.objects.filter(customer=OuterRef('pk'), order_date__gte=one_year_ago)
customers_to_delete = Customer.objects.filter(~Exists(recent_orders))

count = customers_to_delete.count()
customers_to_delete.delete()


timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
log_path = r"C:\Temp\customer_cleanup_log.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, "a") as f:
    f.write(f"[{timestamp}] Deleted {count} inactive customers.\n")

print(f"Deleted {count} inactive customers.")
