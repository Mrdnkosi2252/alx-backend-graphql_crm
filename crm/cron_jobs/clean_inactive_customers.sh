#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."


cd "$PROJECT_ROOT"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
OUTPUT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)
count = inactive_customers.count()
inactive_customers.delete()
print(f'Deleted {count} customers.')
")


echo "[$TIMESTAMP] $OUTPUT" >> /tmp/customer_cleanup_log.txt