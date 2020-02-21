import datetime
import calendar


def data_filter(request, model, date_from, date_to, selected_category="-1"):
    year = datetime.date.today().year
    month = datetime.date.today().month

    if date_from == "":
        date_from = datetime.date(year=year,
                                  month=month,
                                  day=1)

    if date_to == "":
        date_to = datetime.date(year=year,
                                month=month,
                                day=calendar.monthrange(year, month)[1])

    if selected_category == "-1":
        return model.objects.filter(user=request.user) \
            .filter(date__gte=date_from) \
            .filter(date__lte=date_to).order_by('-date')
    else:
        return model.objects.filter(user=request.user) \
            .filter(date__gte=date_from) \
            .filter(date__lte=date_to) \
            .filter(category=selected_category).order_by('-date')


def get_month_names():
    return [datetime.date(2000, m, 1) for m in range(1, 13)]
