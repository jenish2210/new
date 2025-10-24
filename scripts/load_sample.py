# Run with: python manage.py shell < scripts/load_sample.py
from store.models import Product
p = Product(name='Sample Phone', slug='sample-phone', description='A sample product', price=9999.00, stock=10)
p.save()
print('Sample product created:', p)
