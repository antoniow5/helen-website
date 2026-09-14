from django.contrib import admin
from django.db import models
from app import models as app_models
import inspect

for name, model in inspect.getmembers(app_models, inspect.isclass):
    if (
        issubclass(model, models.Model)
        and model.__module__ == app_models.__name__
    ):
        admin.site.register(model)