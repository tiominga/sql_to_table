from django.shortcuts import render
from sql_to_table.utils import sql_to_table
from django.http import JsonResponse

# Create your views here.
def home_index(request):
    """
    Render the home page.
    """
    return render(request, 'home/index.html')

def home_sql_to_table(request):
    """
    Convert SQL to a table and render it.
    """
    sql = request.POST.get('query')
    params = request.POST.get('params')
    edit_function = request.POST.get('edit_function', '') or None
    delete_function = request.POST.get('delete_function', '') or None
    tr_function = request.POST.get('tr_function', '') or None
    pagination = request.POST.get('pagination', '') or None
    offset = request.POST.get('offset', 0)
    style_index = request.POST.get('style_table', 0)

    print("style index:", style_index)


    # Convert the SQL query to a table
    obj_sql_to_table = sql_to_table.SqlToTable()
    obj_sql_to_table.set_query(sql)
    obj_sql_to_table.set_params(params)
    obj_sql_to_table.set_edit_function(edit_function)
    obj_sql_to_table.set_delete_function(delete_function)
    obj_sql_to_table.set_tr_function(tr_function)
    obj_sql_to_table.set_pagination(pagination)
    obj_sql_to_table.set_offset(offset)
    obj_sql_to_table.set_style_index(style_index)

    table = obj_sql_to_table.query_to_html()


    
    # Render the table in the template
    return JsonResponse({'status':'success','table':table})

def home_delete(request):
    print("home_delete")

def home_edit(request):
    print("home_edit")    