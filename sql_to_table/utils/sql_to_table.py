from django.db import connections
from django.utils.html import escape

class SqlToTable:
    def __init__(self):
        self.query = None
        self.params = None
        self.edit_rout = None  # Name of the JavaScript function to handle editing
        self.delete_rout = None  # Name of the JavaScript function to handle deletion
        self.pagination = None  # Placeholder for pagination logic if needed
        self.offset = 0  # Default offset for pagination

    def set_query(self, query):
        self.query = query

    def set_params(self, raw_params):
        if isinstance(raw_params, str):
            raw_params = raw_params.strip()
            if not raw_params:
                self.params = []
                return
            self.params = [p.strip() for p in raw_params.split(",")]
        elif isinstance(raw_params, list):
            self.params = raw_params
        else:
            self.params = []

    def set_edit_rout(self, edit_rout):
        self.edit_rout = edit_rout

    def set_delete_rout(self, delete_rout):
        self.delete_rout = delete_rout

    def set_pagination(self, pagination):
        self.pagination = pagination    

    def set_offset(self, offset):        
            self.offset = offset
        
    def execute_query(self):
        query = self.query
        if (self.pagination is not None and self.pagination != "0"):
            query += f" LIMIT {self.pagination} OFFSET {self.offset}"

        print(f"Executing SQL Query: {query} with params: {self.params}")

        with connections['default'].cursor() as cursor:
            cursor.execute(query, self.params)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        return result, columns
    
    def __get_total_rows(self):
        count_query = f"SELECT COUNT(*) FROM ({self.query}) as sub"
        with connections['default'].cursor() as cursor:
            cursor.execute(count_query, self.params or [])
            total = cursor.fetchone()[0]
        return total
    

    
    
    def __get_pagination_buttons(self):
        total_rows = self.__get_total_rows()
        if total_rows == 0:
            return ""
        else:
            n_buttons = total_rows // int(self.pagination)
            if total_rows % int(self.pagination) > 0:
                n_buttons += 1

        div_open = '<div class="d-flex justify-content-center mt-3 flex-wrap" style="gap: 5px;">'
        html_buttons = ""

        for i in range(n_buttons):
            offset_value = i * int(self.pagination)
            html_buttons += f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" onclick=\"document.getElementById('stt_offset').value = {offset_value};document.getElementById('stt_offset').focus()\">{i+1}</button>"
            bigger = offset_value

        first_button = f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" onclick=\"stt_offset.value = +stt_offset.value - +stt_pagination.value;document.getElementById('stt_offset').focus()\"><<</button>"    

        last_button =  f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" onclick=\"stt_offset.value = +stt_offset.value + +stt_pagination.value;document.getElementById('stt_offset').focus()\">>></button>"        

        return div_open+first_button+html_buttons+last_button+'</div>'    

    
            


    def __get_buttons(self, id_value):
        # Generate HTML for action buttons with consistent size and spacing
        button_style = (
            "padding: 0.3rem 0.6rem; min-width: 80px; margin-right: 5px; "
            "cursor: pointer; display: inline-block;"
        )

        buttons = ""

        if self.edit_rout is not None:
            buttons += (
                f'<button onclick="{self.edit_rout}({id_value})" '
                f'class="btn btn-primary btn-sm" style="{button_style}">Edit</button>'
            )

        if self.delete_rout is not None:
            buttons += (
                f'<button onclick="{self.delete_rout}({id_value})" '
                f'class="btn btn-danger btn-sm" style="{button_style}">Delete</button>'
            )

        return buttons


    def query_to_html(self):
        result, columns = self.execute_query()

        # Ensure there's an 'id' column for button actions
        try:
            id_index = columns.index("id")
        except ValueError:
            raise Exception("The SQL query must return a column named 'id'.")

        # Generate the HTML table using Bootstrap classes
        table_html = '<table class="table table-bordered table-striped">'

        # Table header
        table_html += '<thead><tr>'
        for column in columns:
            table_html += f'<th>{escape(column)}</th>'

        if self.edit_rout or self.delete_rout:            
            table_html += '<th style="white-space: nowrap; width: 1%;">Actions</th></tr></thead>'

        # Table body
        table_html += '<tbody>'
        for row in result:
            table_html += '<tr>'
            for column in row:
                table_html += f'<td>{escape(str(column))}</td>'

            if self.edit_rout or self.delete_rout:
                row_id = row[id_index]
                buttons = self.__get_buttons(row_id)
                table_html += f'<td style="white-space: nowrap;">{buttons}</td></tr>'

        table_html += '</tbody></table>'

        pagination_buttons = self.__get_pagination_buttons()

        table_html += pagination_buttons

        return table_html
