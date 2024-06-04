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
    <style>
        .selected {
            background-color: #d1e7dd !important;
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
                    <tr>
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
        <input type="text" id="folderPaths" value='["E:\\aaa\\bb\\parent1", "E:\\aaa\\bb\\parent2"]' hidden>
        <form id="downloadForm" method="post" action="/download_zip">
            <button type="button" onclick="submitForm()">Download Zip</button>
        </form>
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
</body>


function escapeBackslashes(array) {
    return array.map(path => path.replace(/\\/g, '\\\\'));
}

let newArray = escapeBackslashes(array);
console.log(newArray);
</html>
