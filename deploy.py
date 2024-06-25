<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataTable with Server-Side Processing</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/select/1.3.3/css/select.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.0.1/css/buttons.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/colreorder/1.5.4/css/colReorder.dataTables.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/select/1.3.3/js/dataTables.select.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/buttons/2.0.1/js/dataTables.buttons.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/buttons/2.0.1/js/buttons.colVis.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/buttons/2.0.1/js/buttons.html5.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/buttons/2.0.1/js/buttons.print.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/colreorder/1.5.4/js/dataTables.colReorder.js"></script>
    <style>
        .td_relevant {
            background-color: #d4edda;
        }
        .td_irrelevant {
            background-color: #f8d7da;
        }
        .mark-button {
            display: none;
        }
        .column-search-inputs input {
            margin-right: 10px;
            width: 100px;
        }
        thead   {
    position: sticky;
    z-index: 12;
    top: 0px;
    background: white;
}
    </style>
</head>
<body>
    <div style="margin-bottom: 20px;">
        <label for="from-date">From:</label>
        <input type="date" id="from-date">
        <label for="to-date">To:</label>
        <input type="date" id="to-date">
        <button id="filter-date">Filter</button>
    </div>


    <table id="example" class="display" style="width:100%">
        <thead>
            <tr>
                <th>ID</th>
                <th>Sender</th>
                <th>Recipient</th>
                <th>Subject</th>
                <th>Body</th>
                <th>Datetime</th>
                <th>Label</th>
            </tr>
            <tr>
                <th><input type="text" id="search-id" placeholder="Search ID"></th>
                <th><input type="text" id="search-sender" placeholder="Search Sender"></th>
                <th><input type="text" id="search-recipient" placeholder="Search Recipient"></th>
                <th><input type="text" id="search-subject" placeholder="Search Subject"></th>
                <th><input type="text" id="search-body" placeholder="Search Body"></th>
                <th><input type="text" id="search-datetime" placeholder="Search Datetime"></th>
                <th><input type="text" id="search-label" placeholder="Search Label"></th>
        

            </tr>
        </thead>
    </table>
    
    <div id="details" style="margin-top:20px;">
        <h3>Row Details</h3>
        <p id="details-content"></p>
    </div>

    <script>
        let fullData = [];

        $(document).ready(function() {
            let table = $('#example').DataTable({
                "processing": true,
                "serverSide": true,
                "ajax": {
                    "url": "/data",
                    "type": "GET",
                    "data": function(d) {
                        d.from_date = $('#from-date').val();
                        d.to_date = $('#to-date').val();
                        d.search_id = $('#search-id').val();
                        d.search_sender = $('#search-sender').val();
                        d.search_recipient = $('#search-recipient').val();
                        d.search_subject = $('#search-subject').val();
                        d.search_body = $('#search-body').val();
                        d.search_datetime = $('#search-datetime').val();
                        d.search_label = $('#search-label').val();
                    },
                    "dataSrc": function (json) {
                        fullData = json.full_data;
                        console.log(fullData)
                        return json.data;
                    }
                },
                "columns": [
                    {
                        "data": "id",
                        "render": function(data, type, row) {
                            return `<span>${data}</span> <button class="mark-button">${row.label === 'relevant' ? 'Mark as Irrelevant' : 'Mark as Relevant'}</button>`;
                        }
                    },
                    { "data": "sender" },
                    { "data": "recipient" },
                    { "data": "subject" },
                    { "data": "body" },
                    { "data": "datetime" },
                    { "data": "label" }
                ],
                orderCellsTop: true,
                fixedHeader: true,
                "createdRow": function(row, data, dataIndex) {
                    $(row).addClass(data.row_class);
                    $(row).addClass(data.id_class);

                    $(row).mouseenter(function() {
                        $(row).find('.mark-button').show();
                    });

                    $(row).mouseleave(function() {
                        $(row).find('.mark-button').hide();
                    });
                },
                "select": {
                    "style": 'single' // 'multi' for multiple select
                },
                "colReorder": true,
                "dom": 'ipBlrt',
                "buttons": [
                    'colvis',
                    'print'
                ]
            });

            $('#example').on('click', '.mark-button', function() {
                let row = $(this).closest('tr');
                let rowData = table.row(row).data();
                let newLabel = rowData.label === 'relevant' ? 'irrelevant' : 'relevant';
                let rowId = rowData.id;

                $.ajax({
                    url: '/update_label',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: rowId, new_label: newLabel }),
                    success: function(response) {
                        if (response.success) {
                            // Update label in DataTable and fullData array
                            rowData.label = newLabel;
                            table.row(row).data(rowData).draw();
                            let fullDataRow = fullData.find(item => item.id === rowId);
                            if (fullDataRow) {
                                fullDataRow.label = newLabel;
                            }
                        }
                    }
                });
            });

            $('#filter-date').click(function() {
                table.draw();
            });

            $('#example').on('select.dt', function(e, dt, type, indexes) {
                if (type === 'row') {
                    const row = table.row(indexes).data();
                    const rowId = row.id;
                    const selectedData = fullData.find(item => item.id === rowId);
                    displayDetails(selectedData);
                }
            });

            $('.column-search-inputs input').on('keyup change', function() {
                table.draw();
            });
        });

        function displayDetails(data) {
            if (data) {
                $('#details-content').html(`
                    <strong>ID:</strong> ${data.id}<br>
                    <strong>Sender:</strong> ${data.sender}<br>
                    <strong>Recipient:</strong> ${data.recipient}<br>
                    <strong>Subject:</strong> ${data.subject}<br>
                    <strong>Body:</strong> ${data.body}<br>
                    <strong>Datetime:</strong> ${data.datetime}<br>
                    <strong>Label:</strong> ${data.label}<br>
                `);
            }
        }
    </script>
</body>
</html>
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydb.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    search_value = request.args.get('search[value]', type=str)
    order_column_index = request.args.get('order[0][column]', type=int)
    order_dir = request.args.get('order[0][dir]', type=str)
    from_date = request.args.get('from_date', type=str)
    to_date = request.args.get('to_date', type=str)

    search_id = request.args.get('search_id', type=str)
    search_sender = request.args.get('search_sender', type=str)
    search_recipient = request.args.get('search_recipient', type=str)
    search_subject = request.args.get('search_subject', type=str)
    search_body = request.args.get('search_body', type=str)
    search_datetime = request.args.get('search_datetime', type=str)
    search_label = request.args.get('search_label', type=str)

    conn = get_db_connection()
    query = "SELECT * FROM mutable WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM mutable WHERE 1=1"
    
    filters = []
    
    if search_id:
        print("inside search id")
        query += " AND id LIKE ?"
        count_query += " AND id LIKE ?"
        filters.append(f'%{search_id}%')
    if search_sender:
        print("inside sender")
        query += " AND sender LIKE ?"
        count_query += " AND sender LIKE ?"
        filters.append(f'%{search_sender}%')
    if search_recipient:
        print("inside recipient")
        query += " AND recipient LIKE ?"
        count_query += " AND recipient LIKE ?"
        filters.append(f'%{search_recipient}%')
    if search_subject:
        query += " AND subject LIKE ?"
        count_query += " AND subject LIKE ?"
        filters.append(f'%{search_subject}%')
    if search_body:
        query += " AND body LIKE ?"
        count_query += " AND body LIKE ?"
        filters.append(f'%{search_body}%')
    if search_value:
        query += """ AND (
            id LIKE ?
            OR sender LIKE ?
            OR recipient LIKE ?
            OR subject LIKE ?
            OR body LIKE ?
            OR datetime LIKE ?
            OR label LIKE ?
        )"""
        count_query += """ AND (
            id LIKE ?
            OR sender LIKE ?
            OR recipient LIKE ?
            OR subject LIKE ?
            OR body LIKE ?
            OR datetime LIKE ?
            OR label LIKE ?
        )"""
        wildcard_search_value = f'%{search_value}%'
        filters.extend([wildcard_search_value] * 7)      
    if search_datetime:
        query += " AND datetime LIKE ?"
        count_query += " AND datetime LIKE ?"
        filters.append(f'%{search_datetime}%')
    if search_label:
        query += " AND label LIKE ?"
        count_query += " AND label LIKE ?"
        filters.append(f'%{search_label}%')
    
    if from_date:
        query += " AND datetime >= ?"
        count_query += " AND datetime >= ?"
        filters.append(from_date)
    if to_date:
        query += " AND datetime <= ?"
        count_query += " AND datetime <= ?"
        filters.append(to_date)
    
    order_columns = ["id", "sender", "recipient", "subject", "body", "datetime", "label"]
    if order_column_index is not None and order_dir in ["asc", "desc"]:
        query += f" ORDER BY {order_columns[order_column_index]} {order_dir}"
    
    query += " LIMIT ? OFFSET ?"
    filters.extend([length, start])
    
    emails = conn.execute(query, filters).fetchall()
    total_filtered = conn.execute(count_query, filters[:-2]).fetchone()[0] # Remove limit and offset filters
    total_records = conn.execute("SELECT COUNT(*) FROM mutable").fetchone()[0]

    data = [dict(row) for row in emails]

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_filtered,
        'data': data,
        'full_data': data  # Assuming you want to return the same data for simplicity
    }
    return jsonify(response)

@app.route('/update_label', methods=['POST'])
def update_label():
    data = request.json
    conn = get_db_connection()
    conn.execute("UPDATE emails SET label = ? WHERE id = ?", (data['new_label'], data['id']))
    conn.commit()
    conn.close()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
