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
            if(!data.hasOwnProperty('error')){
                if(data[0].estado){
                    estado = 'Pendiente <i class="text-danger fas fa-times-circle"></i>'
                } else {
                    estado = 'Finalizado <i class="text-success fas fa-check-circle"></i>'
                }
                
                var formattedDate = new Date(data[0].creacion);
                var d = formattedDate.getDate();
                var m =  formattedDate.toLocaleString('default', { month: 'long' });
                var y = formattedDate.getFullYear();

                Swal.fire({
                    icon: 'info',
                    html: '<div class="text-left"><b>Estado: </b>'+ estado +'</div>'+
                                '<div class="text-left"><b>Recibido: </b>'+ m + " " + d + ", " + y +'</div>'+
                                '<div class="text-left"><b>Negocio involucrado: </b>'+ data[0].negocio +'</div>'+
                                '<div class="text-left"><b>Originado en: </b>'+ data[0].municipio +'</div>',
                })
                barra.val('')
                return false
            }
            Swal.fire({
                icon: 'error',
                title: 'Oops..!',
                text: 'Recargue el sitio si el problema persiste.',
            })
        }).fail(function(data){
            Swal.fire({
                icon: 'error',
                title: '¡Nada encontrado!',
                text: 'Asegurese que el no. sea correcto.',
            })
        });
    } else if(!id){
        Swal.fire({
            icon: 'warning',
            title: 'Oops...!',
            text: 'Campo vacío, ingrese un dato.',
        })
    } else {
        Swal.fire({
            icon: 'warning',
            title: '¡Ingreso incorrecto!',
            text: 'Formato de ingreso incorrecto.',
        })
    }
})
