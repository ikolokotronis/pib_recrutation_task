# Rekrutacja – programista Python – maj 2023
 
Dział Informatyki, Instytut Łączności – Państwowy Instytut Badawczy

## Zadanie 1

Proszę zaimplementować w Pythonie funkcję `group_by`, która dla listy słowników zwróci pogrupowaną listę słowników wg. wskazanego pola.
Np. dla wywołania:
```python
group_by(
    elements=[
        {'name': 'Pierogi', 'category': 'główne', 'value': 21}, 
        {'name': 'Rosół', 'category': 'zupa', 'value': 16}, 
        {'name': 'Ogórkowa', 'category': 'zupa', 'value': 17}, 
        {'name': 'Mascarpone', 'category': 'deser', 'value': 10}, 
        {'name': 'Lody', 'category': 'deser', 'value': 6}, 
    ],
    field='category'
)
```
zwróci:
```python
[
    {'category': 'główne', 'items': [{'name': 'Pierogi', 'value': 21}]},
    {'category': 'zupa', 'items': [{'name': 'Rosół', 'value': 16}, {'name': 'Ogórkowa', 'value': 17}]},
    {'category': 'deser', 'items': [{'name': 'Mascarpone', 'value': 10}, {'name': 'Lody', 'value': 6}]},
]

```

## Zadanie 2

Bardzo proszę uzupełnić poniższe klasy metodami, które dostarcza Django do obsługi formularza i jego walidacji, tak aby wykorzystując formularz
`FootballPlayerForm` można było dodać użytkownika do wybranego klubu piłkarskiego na poniższych zasadach:

1. Kluby szukają młodych zawodników, więc chcą dodać tylko zawodników urodzonych po roku 2000, jeśli piłkarz jest starszy, wówczas formularz powinien zgłosić błąd "Niestety nie możesz dodać piłkarza, który urodził się przed 2000 rokiem".
2. Kluby mogą zatrudnić tylko 3 piłkarzy, których narodowość jest "non EU", jeśli w danym klubie jest już 3 piłkarzy o narodowości 'non EU'zwracany jest błąd "Nie można dodać 4 zawodnika spoza Unii Europejskiej".
3. Po pomyślnym dodaniu piłkarza w klubie powinna zmienić się kolumna no_players, która zlicza liczbę piłkarzy w klubie.
4. Po poprawnej walidacji formularza klasa widoku powinna wysyłać email (wykorzystując metodę `send_mail`) z komunikatem "Dodano poprawnie piłkarza <imię i nazwisko piłkarza>".
5. Po niepoprawnej walidacji formularza klasa widoku powinna wysłać email (wykorzystując metodę `send_mail`) z komunikatem "Nie udało się dodać piłkarza <imię i nazwisko piłkarza>".
6. Dodatkowo proszę o napisanie zapytanie w django ORM, który zwróci kluby piłkarskie posortowane po liczbie piłkarzy spoza Unii europejskiej (malejąco)

```python
# models.py

from django.db import models


class FootballClub(models.Model):

    name = models.CharField('nazwa', max_length=256)
    founded = models.DateField('data założenia')
    no_players = models.IntegerField('liczba piłkarzy')


class FootballPlayer(models.Model):

    first_name = models.CharField('pierwsze imię', max_length=256)
    last_name = models.CharField('nazwisko', max_length=256)
    birth_year = models.IntegerField('rok urodzenia')
    club = models.ForeignKey(FootballClub, on_delete=models.DO_NOTHING)
    nationality = models.CharField('narodowość', max_length=256, choices=['EU', 'non EU'])


# views.py

from django.views.generic.edit import CreateView


class AddFootballPlayerView(CreateView):

    form_class = FootballPlayerForm

    def send_mail(self, msg):
        email.send(msg)


# forms.py

from django.forms.models import ModelForm


class FootballPlayerForm(ModelForm):

    class Meta:
        model = FootballPlayer
        fields = '__all__'
```

## Zadanie 3

Na podstawie poniższych tabel bazy danych proszę napisać zapytanie w SQL, które zwróci 
nazwę użytkownika, jego firmę (jeśli nigdzie nie pracuje, wtedy ma zamiast nazwy 
firmy zwrócić string ‘bezrobotny’) oraz liczbę jego samochodów zaczynających się na 
K. Zwracani mają być tylko ci użytkownicy, którzy mają co najwyżej jeden samochód 
na literę K (czyli jeden lub w ogóle).

**User**

| id | name   | company_id |
|----|--------|------------|
| 1  | Alice  | 1          |
| 2  | Bob    | 2          |
| 3  | Carol  | null       |

**Company**

| id | name      |
|----|-----------|
| 1  | Google    |
| 2  | Microsoft |

**Car**

| id | name   |
|----|--------|
| 1  | Ford   |
| 2  | Nissan |
| 3  | Kia    |

**UserCar**

| id | user_id | car_id |
|----|---------|--------|
| 1  | 1       | 1      |
| 2  | 2       | 1      |
| 3  | 3       | 2      |
| 4  | 1       | 3      |

## Zadanie 4

Proszę dokonać weryfikacji kodu, tj. jego oceny pod kątem znanych dobrych praktyk, optymalizacji, czy użycia odpowiednich funkcji.
Ocenie podlega zarówno model, jak i funkcja.

```python
# models.py

from django.db import models


class Entities(models.Model):
    '''Podmiot.'''

    name = models.TextField(verbose_name="Podmiot")
    address = models.TextField(verbose_name="Adres", blank=True, null=True)


class Invoice(models.Model):
    '''Faktura.'''

    name = models.CharField(verbose_name='nr faktury', unique=True)
    created_at = models.DateTimeField(verbose_name='data utworzenia', auto_now_add=True)
    value = models.FloatField(verbose_name='kwota netto')

    entity = models.OneToOneField(Entities, on_delete=models.SET_NULL, null=True, blank=True)

    TAX = 23

    def update_value(self):
        self.value = 0
        for item in self.item_set().all():
            self.value += item.product.value

        self.save(update_fields=['value'])

    @property
    def value_with_tax(self):
        return self.value * self.TAX


class Product(models.Model):
    """Produkt."""
    name = models.TextField(verbose_name="Produkt")
    value = models.FloatField(verbose_name="kwota netto")
    tax = models.FloatField(verbose_name="podatek")


class Item(models.Model):
    """Pozycje na fakturze."""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)


# exports.py

import csv
from .models import *
from django.db.models import Sum


def exportInvoceFiles():
    with open('zamówienia', 'w') as _f:
        stream = csv.writer(_f)
        stream.writerow(['Podmiot', 'Ile ma zamówień', 'Na łączną kwotę'])
        for entity in Entities.objects.all():
            stream.writerow([
                entity.name, Invoice.objects.filter(entity=entity).count(),
                Invoice.objects.filter(entity=entity).aggregate(sum=Sum('value'))['sum'] * Invoice.TAX
            ])


def export_data_invoice(invoice_id):
    """Generator, który zwraca kolejne wiersze do wyświetlenia/zapisania do pliku."""
    invoice = Invoice.objects.get(id=invoice_id)
    yield invoice.entity.name
    
    value = 0
    for item in invoice.item_set().all():
        yield item.product.name, item.product.value, item.product.tax
        value += item.product.value * item.product.tax
    
    yield f'\n\n Do zapłaty: {value} zł (brutto)'
```