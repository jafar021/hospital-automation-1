from django.contrib import admin
from .models import user_type, patient, patient_history, helpers_nurses, medicines
# Register your models here.

admin.site.register(user_type)
admin.site.register(patient)
admin.site.register(patient_history)
admin.site.register(helpers_nurses)
admin.site.register(medicines)
