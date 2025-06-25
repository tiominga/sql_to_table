from django.db import connections
from django.utils.html import escape

class SqlToTable:
    def __init__(self):
        self.query = None
        self.params = None
        self.edit_function = None  # JavaScript function to handle editing
        self.delete_function = None  # JavaScript function to handle deletion
        self.line_function = None  # JavaScript function to handle row click
        self.pagination = None  # Items per page
        self.offset = 0  # Pagination offset
        self.style_index = 0  # Index for table style, default is 0

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

    def set_edit_function(self, edit_function):
        self.edit_function = edit_function

    def set_delete_function(self, delete_function):
        self.delete_function = delete_function

    def set_tr_function(self, line_function): 
        self.line_function = line_function   

    def set_pagination(self, pagination):
        self.pagination = pagination    

    def set_offset(self, offset):        
        self.offset = offset

    def set_style_index(self, style_index):
        self.style_index = style_index

    def execute_query(self):
        query = self.query
        if self.pagination and self.pagination != "0":
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
        if total_rows == 0 or not self.pagination or self.pagination == "0":
            return ""

        pagination = int(self.pagination)
        n_buttons = total_rows // pagination
        if total_rows % pagination > 0:
            n_buttons += 1

        max_offset = (n_buttons - 1) * pagination

        # Container for pagination buttons
        div_open = (
            '<div class="d-flex justify-content-center flex-wrap" '
            'style="gap: 5px;">'
        )
        html_buttons = ""

        for i in range(n_buttons):
            offset_value = i * pagination
            html_buttons += (
                f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" "
                f"onclick=\"stt_offset.value = {offset_value};stt_offset.focus()\">{i+1}</button>"
            )

        # "<< previous" button with offset lower bound protection
        first_button = (
            f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" "
            f"onclick=\"stt_offset.value = Math.max(+stt_offset.value - +stt_pagination.value, 0);stt_offset.focus()\"><<</button>"
        )

        # ">> next" button with offset upper bound protection
        last_button = (
            f"<button type=\"submit\" class=\"btn btn-sm btn-outline-primary\" "
            f"onclick=\"stt_offset.value = Math.min(+stt_offset.value + +stt_pagination.value, {max_offset});stt_offset.focus()\">>></button>"
        )

        return div_open + first_button + html_buttons + last_button + '</div>'

    def __get_buttons(self, id_value):
        button_style = (
            "padding: 0.3rem 0.6rem; min-width: 80px; margin-right: 5px; "
            "cursor: pointer; display: inline-block;"
        )

        buttons = ""

        if self.edit_function is not None:
            buttons += (
                f'<button onclick="{self.edit_function}({id_value},event)" '
                f'class="btn btn-primary btn-sm" style="{button_style}">Edit</button>'
            )

        if self.delete_function is not None:
            buttons += (
                f'<button onclick="{self.delete_function}({id_value},event)" '
                f'class="btn btn-danger btn-sm" style="{button_style}">Delete</button>'
            )

        return buttons
    

    def table_style(self):

        style_index = int(self.style_index)

        style  = (
        # 0 - Default striped and bordered
        '<table class="table table-bordered table-striped">',

        # 1 - Compact + responsive + striped
        '<table class="table table-sm table-bordered table-striped table-responsive">',

        # 2 - Dark theme + hover + striped
        '<table class="table table-dark table-hover table-striped">',

        # 3 - Hoverable rows + light borders
        '<table class="table table-hover border-light">',

        # 4 - Borderless + striped
        '<table class="table table-borderless table-striped">',

        # 5 - Bordered + hover + responsive
        '<table class="table table-bordered table-hover table-responsive">',

        # 6 - Striped + large text (great for touch/mobile)
        '<table class="table table-bordered table-striped fs-5">',

        # 7 - Centered text + striped
        '<table class="table table-striped text-center">',

        # 8 - Table with success background for entire table
        '<table class="table table-success table-striped table-bordered">',

        # 9 - Table with danger background + hover
        '<table class="table table-danger table-hover">',

        # 10 - Striped, hoverable, bold, large font
        '<table class="table table-striped table-hover fw-bold fs-5">',

        # 11 - Light theme + responsive + centered text
        '<table class="table table-light table-responsive text-center">',

        # 12 - Borderless + compact + large text
        '<table class="table table-borderless table-sm fs-5">',

        # 13 - Dark + bold + centered
        '<table class="table table-dark fw-bold text-center">',

        # 14 - Colorful header, striped, bordered
        '<table class="table table-striped table-bordered table-primary">'
    )


        return style[style_index]   

    def query_to_html(self):
        result, columns = self.execute_query()

        # Make sure the result contains an "id" column
        try:
            id_index = columns.index("id")
        except ValueError:
            raise Exception("The SQL query must return a column named 'id'.")

        # Start flex container for table and pagination

        table_style = self.table_style()

        table_html = (
            '<div class="d-flex flex-column" style="min-height: 60vh;">'
            f'{table_style}'
        )

        # Table header
        table_html += '<thead><tr>'
        for column in columns:
            table_html += f'<th>{escape(column)}</th>'

        if self.edit_function or self.delete_function:
            table_html += '<th style="white-space: nowrap; width: 1%;">Actions</th></tr></thead>'

        # Table body
        table_html += '<tbody>'

        for row in result:
            if self.line_function:
                t_r = f'<tr onclick="{self.line_function}({row[id_index]},event);" style="cursor: pointer;">'
            else:
                t_r = '<tr>'

            table_html += t_r

            for column in row:
                table_html += f'<td>{escape(str(column))}</td>'

            if self.edit_function or self.delete_function:
                row_id = row[id_index]
                buttons = self.__get_buttons(row_id)
                table_html += f'<td style="white-space: nowrap;">{buttons}</td></tr>'

        table_html += '</tbody></table>'

        pagination_buttons = self.__get_pagination_buttons()

        # Append pagination buttons at the bottom of the flex column
        table_html += f'<div class="mt-auto">{pagination_buttons}</div></div>'

        return table_html
