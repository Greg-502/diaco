$(document).on('click', '.modalDelete', function () {
    tabla = $('#example').DataTable();
    fila = $(this).closest('tr');
    id = parseInt(fila.find('td:eq(1)').text());
    
    if (id) {
        Swal.fire({
            title: '¿Seguro?',
            text: "Esta queja se marcará como resuelta.",
            icon: 'warning',
            cancelButtonColor: '#d9534f',
            confirmButtonColor: '#5cb85c',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Confirmar',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: window.location.pathname,
                    method: 'POST',
                    data: {
                        'action': 'remove',
                        'id': id
                    },
                    dataType: 'JSON',
                    headers: {'X-CSRFToken': csrftoken}
                }).done(function (data) {
                    if(!data.hasOwnProperty('error')){
                        // window.location.reload();
                        // tabla.find(fila).remove();
                        // tabla.row(fila.parents('tr')).remove().draw();
                        tabla.row(fila, { page: 'current' }).remove().draw();
                        Swal.fire({
                            icon: 'success',
                            title: '¡Listo!',
                            text: 'La queja ha sido resuelta.',
                        })
                        return false;
                    }
                    Swal.fire({
                        title: '¡Error!',
                        text: "No se pudo realizar esta acción.",
                        icon: 'warning'
                    });
                }).fail(function (data) {
                    Swal.fire({
                        title: '¡Error!',
                        text: "Algo ha salido mal.",
                        icon: 'error'
                    });
                });
            }
        });
    } else {
        Toast.fire({
            icon: 'error',
            title: 'Algo salió mal.'
        });
    }
});

$(document).on('click', '.modalQueja', function () {
    fila = $(this).closest('tr');
    id = parseInt(fila.find('td:eq(1)').text());
    if (id) {
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': '1',
                id: id
            },
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data) {
            Swal.fire({
                html: '<div class="text-justify">' + data.queja + '</div>',
            })
        }).fail(function (data) {
            Swal.fire({
                icon: 'warning',
                title: 'Algo salió mal',
                text: 'Si persiste, refresque la página.',
            });
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: 'Inténtelo nuevamente',
            text: 'Algo ha ido mal',
        })
    }
});