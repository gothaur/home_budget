def sidebars(request):
    if request.path == '/expenses/':
        message = "expenses"
    elif request.path == '/income/':
        message = "income"
    else:
        message = None
    return {'message': message}
