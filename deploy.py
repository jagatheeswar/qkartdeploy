import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
from io import BytesIO  # Import BytesIO from the io module

app = Flask(__name__)

# Function to fetch data from the SQLite database
def fetch_data(page, page_size, from_date=None, to_date=None):
    offset = (page - 1) * page_size
    conn = sqlite3.connect(r'E:\ai project\email_classifier_gui\email_classifier.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM email_table'
    params = []

    if from_date and to_date:
        query += ' WHERE date_time BETWEEN ? AND ?'
        params.extend([from_date, to_date])
    
    query += ' LIMIT ? OFFSET ?'
    params.extend([page_size, offset])

    cursor.execute(query, params)
    
    columns = [col[0] for col in cursor.description]  # Get column names
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries
    conn.close()
    return data, columns


@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    page_size = 1000  # Adjust page size as needed

    if request.method == 'POST':
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
    else:
        from_date = None
        to_date = None

    data, columns = fetch_data(page, page_size, from_date, to_date)
    df = pd.DataFrame(data, columns=columns)
    
    return render_template('index.html', table=df, page=page, from_date=from_date, to_date=to_date)



@app.route('/download_zip', methods=['POST'])
def download_zip():
    print("came inside")
    data = request.get_json()
    parent_folder_paths = data.get('parent_folder_paths', [])
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for parent_folder_path in parent_folder_paths:
            folder_name = os.path.basename(parent_folder_path)
            for foldername, subfolders, filenames in os.walk(parent_folder_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.join(folder_name, os.path.relpath(file_path, parent_folder_path))
                    zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    return send_file(zip_buffer, as_attachment=True, download_name='files.zip', mimetype='application/zip')


if __name__ == '__main__':
    app.run(debug=True)





<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask DataFrame Table Example</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.25/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/select/1.3.1/css/select.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/colreorder/1.5.4/css/colReorder.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/1.7.1/css/buttons.dataTables.min.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <style>
        .selected {
            background-color: #d1e7dd !important;
        }
    </style>

<style>
    .relevancy-yes {
        background-color: #02ee39 !important; /* Light green */
    }

    .relevancy-no {
        background-color: #f8d7da; /* Light red */
    }
</style>
    <style>
        .filter-tablet {
            display: inline-block;
            margin: 5px;
            padding: 5px 10px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 15px;
            max-width: 200px; /* Limit the width */
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            position: relative;
        }
        .filter-tablet:hover::after {
            content: attr(data-fulltext);
            position: absolute;
            left: 0;
            top: 100%;
            white-space: normal;
            background-color: #fff;
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 5px;
            z-index: 1000; /* Ensure it appears above other elements */
            width: max-content; /* Adjust the width */
            max-width: 400px; /* Max width for better visibility */
        }
        .filter-tablet .close {
            margin-left: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DataFrame Table with Sorting, Row Selection, Column Reordering, Column Visibility, and Filters</h1>
        <!-- Render DataFrame table with DataTables -->
        <table id="datatable" class="display">
            <thead>
                    <tr>
                        {% for col in table.columns %}
                        <th>{{ col }}</th>
                    {% endfor %}
                    <th>Action</th> <!-- Add an additional column for the action -->
                </tr>
            </thead>
            <tbody>
                {% for index, row in table.iterrows() %}
                <tr class="{% if row['relevancy'] == 'Yes' %}relevancy-yes{% else %}relevancy-no{% endif %}">
                    {% for value in row %}
                            <td>{{ value }}</td>
                        {% endfor %}
                        <td><button class="read-btn">Read</button></td> <!-- Button for the action -->
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        <!-- Add pagination controls -->
        <div class="pagination">
            <a href="{{ url_for('index', page=1) }}">First</a>
            <a href="{{ url_for('index', page=page-1) }}">Previous</a>
            <a href="{{ url_for('index', page=page+1) }}">Next</a>
        </div>
        <input type="text" id="folderPaths" value='["E:\\ai project\\email_classifier_gui\\parent1", "E:\\ai project\\email_classifier_gui\\parent2"]' hidden>
        <form id="downloadForm" method="post" action="/download_zip">
            <button type="button" onclick="submitForm()">Download Zip</button>
        </form>
    </div>
    <form method="POST" action="{{ url_for('index') }}">
        <label for="from_date">From Date:</label>
        <input type="date" id="from_date" name="from_date" value="{{ from_date }}">
        <label for="to_date">To Date:</label>
        <input type="date" id="to_date" name="to_date" value="{{ to_date }}">
        <button type="submit">Search</button>
    </form>
    
    <!-- Add Filter button and Search button -->
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#filterModal">Add Filter</button>
    <form method="POST" action="{{ url_for('index') }}">
        <input type="hidden" id="from_date_input" name="from_date">
        <input type="hidden" id="to_date_input" name="to_date">
        <input type="hidden" id="filters_input" name="filters">
        <button type="submit" id="search-button">Search</button>
    </form>
    <div id="filters-container"></div>

    <div class="modal fade" id="filterModal" tabindex="-1" role="dialog" aria-labelledby="filterModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="filterModalLabel">Add Filter</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="filter-form">
                        <div class="form-group">
                            <label for="column-name">Column</label>
                            <select class="form-control" id="column-name">
                                <option value="sender">Sender</option>
                                <option value="recipient">Recipient</option>
                                <option value="relevancy">Relevancy</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="operator">Operator</label>
                            <select class="form-control" id="operator">
                                <option value="is">Is</option>
                                <option value="is_not">Is Not</option>
                                <option value="is_one_of">Is One Of</option>
                                <option value="is_equal">Is Equal</option>
                                <!-- Add more operators as needed -->
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="value">Value</label>
                            <input type="text" class="form-control" id="value">
                        </div>
                        <button type="button" class="btn btn-primary" id="apply-filter-button">Apply Filter</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <!-- DataTables JavaScript -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/select/1.3.1/js/dataTables.select.min.js"></script>
    <script src="https://cdn.datatables.net/colreorder/1.5.4/js/dataTables.colReorder.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/1.7.1/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/1.7.1/js/buttons.colVis.min.js"></script>
    
    <script>
        $(document).ready(function() {
            var table = $('#datatable').DataTable({
                dom: 'Bfrtip',
                buttons: [
                    {
                        extend: 'colvis',
                        columns: [1, 2, 3] // Specify which columns can be hidden
                    }
                ],
                colReorder: true,
                select: {
                    style: 'multi'
                }
            });
    
            $('#datatable tbody').on('click', 'tr', function(event) {
                if (event.ctrlKey) {
                    $(this).toggleClass('selected');
                } else {
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                }
            });
    
            // Add right arrow symbol to each row and handle click events
            $('#datatable tbody').on('mouseenter', 'tr', function() {
                $(this).find('td:eq(0)').append('<span class="arrow">→</span>');
            });
    
            $('#datatable tbody').on('mouseleave', 'tr', function() {
                $(this).find('span.arrow').remove();
            });
    
            $('#datatable tbody').on('click', 'span.arrow', function() {
                var rowData = table.row($(this).parents('tr')).data();
                var rowId = rowData[0]; // Assuming the first column contains row IDs
                console.log('Clicked arrow for row ID: ' + rowId);
                // Perform the desired action here
            });
        });
    </script>
    
    
       <script>
        function submitForm() {
            const folderPaths = document.getElementById('folderPaths').value;

            fetch('/download_zip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ parent_folder_paths: JSON.parse(folderPaths) }),
            })
            .then(response => {
                if (response.ok) {
                    return response.blob();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'files.zip';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        }
    </script>
    <script>
        $(document).ready(function() {
            function getFilters() {
    var filters = [];
    $('#filters-container .filter-item').each(function() {
        var column = $(this).find('.column-name').val();
        var operator = $(this).find('.operator').val();
        var value = $(this).find('.value').val();
        filters.push({ column: column, operator: operator, value: value });
    });
    return filters;
}
            var filters = [];
    
            $('#apply-filter-button').on('click', function() {
                var columnName = $('#column-name').val();
                var operator = $('#operator').val();
                var value = $('#value').val();
    
                var filter = {
                    column: columnName,
                    operator: operator,
                    value: value
                };
    
                filters.push(filter);
                updateFiltersDisplay();
                console.log(filters)
                $('#filterModal').modal('hide');
            });
    
            $('#search-button').on('click', function() {
    var from_date = $('#from_date').val();
    var to_date = $('#to_date').val();
    var filters = JSON.stringify(getFilters()); // Assuming you have a function getFilters() that returns the filters in JSON format
    
    $('#from_date_input').val(from_date);
    $('#to_date_input').val(to_date);
    $('#filters_input').val(filters);
});
            function updateFiltersDisplay() {
                var filtersContainer = $('#filters-container');
                filtersContainer.empty();
    
                filters.forEach((filter, index) => {
                    var filterText = `${filter.column} ${filter.operator} ${filter.value}`;
                    var filterTablet = $('<div class="filter-tablet" data-fulltext="' + filterText + '"></div>');
                    filterTablet.text(filterText);
                    var closeBtn = $('<span class="close">&times;</span>');
                    closeBtn.on('click', function() {
                        filters.splice(index, 1);
                        updateFiltersDisplay();
                    });
                    filterTablet.append(closeBtn);
                    filtersContainer.append(filterTablet);
                });
            }
    
        });
    </script>
</body>
</html>




import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
from io import BytesIO  # Import BytesIO from the io module

app = Flask(__name__)

# Function to fetch data from the SQLite database
def fetch_data(page, page_size, from_date=None, to_date=None, filters=None):
    offset = (page - 1) * page_size
    conn = sqlite3.connect(r'E:\ai project\email_classifier_gui\email_classifier.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM email_table'
    params = []

    # Handle date filters
    if from_date and to_date:
        query += ' WHERE date_time BETWEEN ? AND ?'
        params.extend([from_date, to_date])

    # Handle additional filters
    if filters:
        for i, f in enumerate(filters):
            if from_date and to_date and i == 0:
                query += ' AND'
            elif i == 0:
                query += ' WHERE'
            else:
                query += ' AND'

            column = f['column']
            operator = f['operator']
            value = f['value']

            if operator == 'is':
                query += f' {column} = ?'
                params.append(value)
            elif operator == 'is_not':
                query += f' {column} != ?'
                params.append(value)
            elif operator == 'is_one_of':
                placeholders = ', '.join('?' * len(value.split(',')))
                query += f' {column} IN ({placeholders})'
                params.extend(value.split(','))
            elif operator == 'is_equal':
                query += f' {column} = ?'
                params.append(value)

    query += ' LIMIT ? OFFSET ?'
    params.extend([page_size, offset])

    cursor.execute(query, params)
    
    columns = [col[0] for col in cursor.description]  # Get column names
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries
    conn.close()
    return data, columns


@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    page_size = 1000  # Adjust page size as needed
    filters = []

    if request.method == 'POST':
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')

        # Get filters from form data
        num_filters = int(request.form.get('num_filters', 0))
        for i in range(num_filters):
            column = request.form.get(f'filter_column_{i}')
            operator = request.form.get(f'filter_operator_{i}')
            value = request.form.get(f'filter_value_{i}')
            if column and operator and value:
                filters.append({'column': column, 'operator': operator, 'value': value})
    else:
        from_date = None
        to_date = None

    data, columns = fetch_data(page, page_size, from_date, to_date, filters)
    df = pd.DataFrame(data, columns=columns)
    print(df)
    # Render index.html template with the filtered data
    return render_template('index.html', table=df, page=page, from_date=from_date, to_date=to_date)


@app.route('/download_zip', methods=['POST'])
def download_zip():
    print("came inside")
    data = request.get_json()
    parent_folder_paths = data.get('parent_folder_paths', [])
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for parent_folder_path in parent_folder_paths:
            folder_name = os.path.basename(parent_folder_path)
            for foldername, subfolders, filenames in os.walk(parent_folder_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.join(folder_name, os.path.relpath(file_path, parent_folder_path))
                    zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    return send_file(zip_buffer, as_attachment=True, download_name='files.zip', mimetype='application/zip')


if __name__ == '__main__':
    app.run(debug=True)


