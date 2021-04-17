var minDate, maxDate;

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = minDate.val();
        var max = maxDate.val();

        var fecha = ( data[7] );
        
        var numbers = fecha.match(/\d+/g); 
        var date = new Date(numbers[2],numbers[1]-1,numbers[0]);
        
        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            return true;
        }
        return false;
    }
);

$(()=>{
    var groupColumn = 0;

    minDate = new DateTime($('#min'), {
        format: 'DD/MM/YYYY',
        i18n: {
            previous: 'Anterior',
            next:     'Siguiente',
            months:   [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Dicembre' ],
            weekdays: [ 'Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sab' ]
        }
    });

    maxDate = new DateTime($('#max'), {
        format: 'DD/MM/YYYY',
        i18n: {
            previous: 'Anterior',
            next:     'Siguiente',
            months:   [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Dicembre' ],
            weekdays: [ 'Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sab' ]
        }
    });

    var table = $('#example').DataTable({
        "order": [[ groupColumn, "asc" ]],
        dom:'BPfrtip',
        searchPanes:{
            cascadePanes:true,
            dtOpts:{
                dom:'tp',
                paging:'true',
                pagingType:'numbers',
                searching:false,
                viewTotal: true
            }
        },
        columnDefs:[{
            searchPanes:{
                show:false
            },
            targets:[0,1,2,6,7,8]
            }
        ],
        buttons: [
            // 'searchPanes',
            {
                extend: 'pdfHtml5',
                text:      'Descargar <i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar a PDF',
                className: 'btn btn-outline-danger mb-4',
                pageSize: 'LETTER',
                exportOptions: {
                    columns: [2,3,4,5,6,7]
                },
                customize: function (doc) {
                    doc['footer']=(function(page, pages) {
                        return {
                            columns: [
                                'diaco-gt.herokuapp.com',
                                {
                                    alignment: 'right',
                                    text: ['Página ', { text: page.toString() },  ' de ', { text: pages.toString() }]
                                }
                            ],
                            margin: [10, 0]
                        }
                    }),
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }
            }
        ],
        "language": {
            searchPanes: {
                clearMessage: 'Limpiar',
                title: {
                    _: 'Filtros aplicados: %d',
                    0: 'Nada seleccionado',
                    1: 'Un filtro aplicado',
                }
            },
            "lengthMenu": "_MENU_",
            "zeroRecords": "Ningún resultado",
            "searchPlaceholder": "Buscar",
            "info": "_TOTAL_ resultado(s)",
            "infoEmpty": "Ningún resultado",
            "infoFiltered": "(Busqueda en _MAX_ registros)",
            "search": "",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            },
        }
    });

    $('#min, #max').on('change', function () {
        table.draw();
    });

    $('#min').keyup( function() {
        minDate.val('01/04/2021')
    } );
});