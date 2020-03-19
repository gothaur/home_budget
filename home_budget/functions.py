import datetime
import calendar
import openpyxl
import re

from django.utils import timezone


def data_filter(request, model, date_from, date_to, selected_category="-1",
                month=timezone.now().month, year=timezone.now().year):
    if date_from == timezone.localdate() or date_from == "":
        date_from = datetime.date(
            year=year,
            month=month,
            day=1,
        )

    if date_to == timezone.localdate() or date_to == "":
        date_to = datetime.date(
            year=year,
            month=month,
            day=calendar.monthrange(year, month)[1],
        )

    if selected_category == "-1":
        result = model.objects.filter(user=request.user, date__gte=date_from, date__lte=date_to).order_by('-date')
        return result
    else:
        return model.objects.filter(
            user=request.user,
            date__gte=date_from,
            date__lte=date_to,
            category=selected_category
        ).order_by('-date')


def get_month_names():
    return [datetime.date(2000, m, 1) for m in range(1, 13)]


def file_handler(file):
    list_of_expenses = []
    list_of_incomes = []
    work_book = openpyxl.load_workbook(file, data_only=True)
    sheet_names_regex = re.compile(r'\d{4}-\d{2}')
    sheet_names = []
    for name in work_book.get_sheet_names():
        if sheet_names_regex.search(name):
            sheet_names.append(name)
    for name in sheet_names:
        sheet = work_book.get_sheet_by_name(name)
        for i, row in enumerate(sheet.iter_rows()):
            expense_date = sheet['B' + str(i + 5)].value or list_of_expenses[-1]['expense_date']
            category = sheet['C' + str(i + 5)].value
            expense_amount = sheet['D' + str(i + 5)].value
            expense_comment = sheet['E' + str(i + 5)].value or "Komentarz"
            if isinstance(expense_amount, (float, int)) and isinstance(expense_date, datetime.date):
                expense_data = {
                    'expense_date': expense_date,
                    'category': category,
                    'expense_amount': expense_amount,
                    'expense_comment': expense_comment,
                }
                list_of_expenses.append(
                    expense_data
                )
            income_amount = sheet['I' + str(i + 5)].value
            if isinstance(income_amount, float) or isinstance(income_amount, int):
                income_date = sheet['H' + str(i + 5)].value or list_of_incomes[-1]['income_date']
                income_comment = sheet['J' + str(i + 5)].value
                income_data = {
                    'income_date': income_date,
                    'income_amount': income_amount,
                    'income_comment': income_comment,
                }
                list_of_incomes.append(income_data)
            if expense_amount is None and income_amount is None:
                break
    return list_of_expenses, list_of_incomes
