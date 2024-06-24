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
                <th><input type="text" placeholder="Search ID"></th>
                <th><input type="text" placeholder="Search Sender"></th>
                <th><input type="text" placeholder="Search Recipient"></th>
                <th><input type="text" placeholder="Search Subject"></th>
                <th><input type="text" placeholder="Search Body"></th>
                <th><input type="text" placeholder="Search Datetime"></th>
                <th><input type="text" placeholder="Search Label"></th>
                <th></th>
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
                    "style": 'multi' // 'multi' for multiple select
                },
                "colReorder": true,
                "dom": 'Bfrtip',
                "initComplete": function () {
                    this.api().columns().every(function () {
                        var that = this;
                        $('input', this.header()).on('keyup change clear', function () {
                            if (that.search() !== this.value) {
                                that.search(this.value).draw();
                            }
                        });
                    });
                },
                "buttons": [
                    'colvis','copy','pdf'
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
    
    columns = ['id', 'sender', 'recipient', 'subject', 'body', 'datetime', 'label']
    order_column = columns[order_column_index]

    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM mutable", conn)
    
    if from_date and to_date:
        df = df[(df['datetime'] >= from_date) & (df['datetime'] <= to_date)]
    
    if search_value:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]
    
    if order_dir == 'asc':
        df = df.sort_values(by=order_column, ascending=True)
    else:
        df = df.sort_values(by=order_column, ascending=False)
    
    total_records = len(df)
    df_paginated = df.iloc[start:start+length]
    
    data = df_paginated.to_dict(orient='records')
    for record in data:
        record['row_class'] = 'td_relevant' if record['label'] == 'relevant' else 'td_irrelevant'
        record['id_class'] = f'td_id_{record["id"]}'
    
    full_data = df.to_dict(orient='records')

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data,
        'full_data': full_data
    }

    conn.close()
    return jsonify(response)

@app.route('/update_label', methods=['POST'])
def update_label():
    row_id = request.json.get('id')
    new_label = request.json.get('new_label')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mutable SET label = ? WHERE id = ?", (new_label, row_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)

