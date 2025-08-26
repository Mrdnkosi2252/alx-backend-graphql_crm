#!/bin/bash


ONE_YEAR_AGO=$(date -d "1 year ago" +%Y-%m-%d)


DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import datetime
from crm.models import Customer
from django.db.models import Count

cutoff_date = datetime.strptime('$ONE_YEAR_AGO', '%Y-%m-%d').date()
customers = Customer.objects.annotate(order_count=Count('orders')).filter(order_count=0, created_at__lt=cutoff_date)
count = customers.count()
customers.delete()
print(count)
")


TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt