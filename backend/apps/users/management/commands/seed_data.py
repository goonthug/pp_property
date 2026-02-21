from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
import random

from apps.users.models import User, Role
from apps.properties.models import Property, PropertyType, Amenity
from apps.tenants.models import Tenant, Contract
from apps.payments.models import Payment, PaymentCategory, PaymentStatus
from apps.service_requests.models import ServiceRequest, RequestCategory


class Command(BaseCommand):
    help = "Заполнить БД тестовыми данными"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создаём тестовые данные...")

        # Пользователи
        admin = User.objects.create_superuser(
            email="admin@property.ru", username="admin",
            password="admin123", first_name="Александр",
            last_name="Иванов", role=Role.ADMIN)

        manager = User.objects.create_user(
            email="manager@property.ru", username="manager", password="manager123",
            first_name="Елена", last_name="Смирнова",
            role=Role.MANAGER, phone="+7 (495) 555-01-01")

        tenant_data = [
            ("tenant1@mail.ru","tenant1","Михаил","Козлов","+7 (916) 123-45-67"),
            ("tenant2@mail.ru","tenant2","Ольга","Петрова","+7 (926) 234-56-78"),
            ("tenant3@mail.ru","tenant3","Дмитрий","Сидоров","+7 (936) 345-67-89"),
        ]
        tenant_users = []
        for email, uname, fn, ln, phone in tenant_data:
            u = User.objects.create_user(
                email=email, username=uname, password="tenant123",
                first_name=fn, last_name=ln, role=Role.TENANT, phone=phone)
            tenant_users.append(u)

        # Типы и удобства
        apt  = PropertyType.objects.create(name="Квартира")
        off  = PropertyType.objects.create(name="Офис")
        wh   = PropertyType.objects.create(name="Склад")
        amenities = [Amenity.objects.create(name=n)
                     for n in ["Кондиционер","Интернет","Парковка","Охрана","Лифт"]]

        # Объекты недвижимости
        props_data = [
            ("Квартира на Арбате",   apt, "available", "ул. Арбат, 14",         65, 5, 3, 85000),
            ("Студия на Таганке",    apt, "rented",    "ул. Таганская, 7",      38, 2, 1, 55000),
            ("Двушка на Проспекте",  apt, "rented",    "Просп. Мира, 45",       54, 8, 2, 72000),
            ("Офис в БЦ Альфа",      off, "rented",    "Ленинская слобода, 26", 120,3,None,180000),
            ("Офис на Садовом",      off, "available", "Садовая-Кудринская, 11",85, 2,None,130000),
            ("Склад на Волгоградке", wh,  "rented",    "Волгоградский пр., 42", 500,1,None,120000),
        ]
        props = []
        for name, ptype, status, addr, area, floor, rooms, rent in props_data:
            p = Property.objects.create(
                name=name, property_type=ptype, status=status,
                address=addr, area=area, floor=floor, rooms=rooms, monthly_rent=rent)
            p.amenities.set(random.sample(amenities, k=3))
            props.append(p)

        # Арендаторы и договоры
        rent_cat = PaymentCategory.objects.create(name="Аренда")
        util_cat = PaymentCategory.objects.create(name="Коммунальные услуги")
        rented = [p for p in props if p.status == "rented"]

        for i, (tenant_user, prop) in enumerate(zip(tenant_users, rented)):
            tenant   = Tenant.objects.create(user=tenant_user, status="active")
            start    = date(2024, 6, 1)
            end      = date(2025, 6, 1)
            contract = Contract.objects.create(
                tenant=tenant, property=prop, start_date=start, end_date=end,
                monthly_rent=prop.monthly_rent, deposit=prop.monthly_rent*2, status="active")

            # Платежи за 6 месяцев 2024
            for m in range(6):
                month = (6 + m - 1) % 12 + 1
                year  = 2024 + (6 + m - 1) // 12
                is_paid = m < 5
                Payment.objects.create(
                    contract=contract, category=rent_cat, amount=prop.monthly_rent,
                    status="paid" if is_paid else "pending",
                    due_date=date(year, month, 10),
                    paid_date=date(year, month, 9) if is_paid else None,
                    period_month=month, period_year=year)
            # Платежи за 2025 год (январь - июнь)
            for month in range(1, 7):
                is_paid = month <= 3
                Payment.objects.create(
                    contract=contract, category=rent_cat, amount=prop.monthly_rent,
                    status="paid" if is_paid else "pending",
                    due_date=date(2025, month, 10),
                    paid_date=date(2025, month, 9) if is_paid else None,
                    period_month=month, period_year=2025)
            # Платежи за 2026 год (январь - июнь)
            for month in range(1, 7):
                is_paid = month <= 2
                Payment.objects.create(
                    contract=contract, category=rent_cat, amount=prop.monthly_rent,
                    status="paid" if is_paid else "pending",
                    due_date=date(2026, month, 10),
                    paid_date=date(2026, month, 9) if is_paid else None,
                    period_month=month, period_year=2026)

        # Категории заявок
        cats = [RequestCategory.objects.create(name=n)
                for n in ["Сантехника","Электрика","Уборка","Ремонт"]]

        # Заявки
        reqs_data = [
            ("Протечка в ванной", rented[0], cats[0], "high",   "in_progress"),
            ("Не работает кондиционер", rented[1], cats[1], "medium", "new"),
            ("Замена лампочек", rented[2], cats[1], "low",    "resolved"),
        ]
        for i, (title, prop, cat, pri, st) in enumerate(reqs_data):
            ServiceRequest.objects.create(
                title=title, description=f"Описание: {title}",
                property=prop, category=cat, priority=pri, status=st,
                created_by=tenant_users[i % len(tenant_users)],
                assigned_to=manager if st == "in_progress" else None)

        self.stdout.write(self.style.SUCCESS("Готово!"))
        self.stdout.write("Логины:")
        self.stdout.write("  Admin:   admin@property.ru / admin123")
        self.stdout.write("  Manager: manager@property.ru / manager123")
        self.stdout.write("  Tenant:  tenant1@mail.ru / tenant123")
