let buscando = $('#searching');
let barra = $('#barra')

buscando.click(function (e){
    e.preventDefault()
    id = barra.val().trim()

    if (parseInt(id)) {
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': 'search',
                id: id
            },
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data) {
            if(data.estado){
                estado = 'Pendiente <i class="text-danger fas fa-times-circle"></i>'
            } else {
                estado = 'Finalizado <i class="text-success fas fa-check-circle"></i>'
            }

            var formattedDate = new Date(data.creacion);
            var d = formattedDate.getDate();
            var m =  formattedDate.toLocaleString('default', { month: 'long' });
            var y = formattedDate.getFullYear();
                
            Swal.fire({
                icon: 'info',
                html: '<div class="text-left"><b>Estado: </b>'+ estado +'</div>'+
                            '<div class="text-left"><b>Recibido: </b>'+ m + " " + d + ", " + y +'</div>',
            })
            barra.val('')
        }).fail(function (data) {
            Swal.fire({
                icon: 'error',
                title: '¡Nada encontrado!',
                text: 'Asegurese que el no. sea correcto.',
            })
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: '¡Error!',
            text: 'Ingrese un no. de referencia válido.',
        })
    }
})
