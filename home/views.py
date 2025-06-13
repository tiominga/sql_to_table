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
    edit_rout = request.POST.get('edit_rout', '') or None
    delete_rout = request.POST.get('delete_rout', '') or None


    # Convert the SQL query to a table
    obj_sql_to_table = sql_to_table.SqlToTable()
    obj_sql_to_table.set_query(sql)
    obj_sql_to_table.set_params(params)
    obj_sql_to_table.set_edit_rout(edit_rout)
    obj_sql_to_table.set_delete_rout(delete_rout)

    table = obj_sql_to_table.query_to_html()


    
    # Render the table in the template
    return JsonResponse({'status':'success','table':table})

def home_delete(request):
    print("home_delete")

def home_edit(request):
    print("home_edit")    