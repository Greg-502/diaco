let boton = $('#enviar');
let comercios = $('#newTags');
let addCom = $('#btnNegocio');
let addSuc = $('#btnSucursal');

var deptos = $('select[name=departamento]');
var municipios = $('select[name=municipio]');
var negocios = $('select[name=negocio]');
var sucursales = $('select[name=sucursal]');
var queja = $('textarea[name=queja]');

$(() => {
    $('select[name=departamento]').on('change', function () {
        var id = $(this).val();
        var opciones = '<option value="">Municipios *</option>'
        var opcionesneg = '<option value="">Negocios *</option>'
        var opcsuc = '<option value="">Sucursales *</option>'

        if(id === ''){
            municipios.html(opciones);
            negocios.html(opcionesneg);
            sucursales.html(opcsuc);
            return false
        }
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': 'munis',
                'id': id
            },
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data) {
            if(!data.hasOwnProperty('error')){
                $.each(data, function(key, value){
                    opciones += '<option value="'+value.pk+'">'+ value.muni +'</option>'
                })
                return false
            }
            Toast.fire({
                icon: 'warning',
                title: 'Algo salió mal.'
            });
        }).fail(function (data){
            Toast.fire({
                icon: 'error',
                title: 'Algo salió mal.'
            });
        }).always(function (data){
            municipios.html(opciones);
            negocios.html(opcionesneg);
            sucursales.html(opcsuc);
        });
    });

    $('select[name=municipio]').on('change', function () {
        var id = $(this).val();
        var opciones = '<option value="">Negocios *</option>'
        var opcsuc = '<option value="">Sucursales *</option>'

        if(id === ''){
            negocios.html(opciones);
            sucursales.html(opcsuc);
            return false
        }
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': 'negos',
                'id': id
            },
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data) {
            if(!data.hasOwnProperty('error')){
                $.each(data, function(key, value){
                    opciones += '<option value="'+value.pk+'">'+ value.nego +'</option>'
                })
                return false
            }
            Toast.fire({
                icon: 'warning',
                title: 'Algo salió mal.'
            });
        }).fail(function (data){
            Toast.fire({
                icon: 'error',
                title: 'Algo salió mal.'
            });
        }).always(function (data){
            negocios.html(opciones);
            sucursales.html(opcsuc);
        });
    });

    $('select[name=negocio]').on('change', function () {
        var id = $(this).val();
        var id_mun = municipios.val();
        var opcsuc = '<option value="">Sucursales *</option>'

        if(id === ''){
            sucursales.html(opcsuc);
            return false
        }
        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {
                'action': 'sucurs',
                'id': id,
                'id_mun': id_mun
            },
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data) {
            if(!data.hasOwnProperty('error')){
                $.each(data, function(key, value){
                    opcsuc += '<option value="'+value.pk+'">'+ value.sucrs +'</option>'
                })
                return false
            }
            Toast.fire({
                icon: 'warning',
                title: 'Algo salió mal.'
            });
        }).fail(function (data){
            Toast.fire({
                icon: 'error',
                title: 'Algo salió mal.'
            });
        }).always(function (data){
            sucursales.html(opcsuc);
        });
    });

    boton.click(function(e){
        var tienda = sucursales.val();
	    var razon = queja.val().trim();
        
        if(razon && tienda){
            e.preventDefault()
            Swal.fire({
                icon: 'info',
                title: 'Confirmación',
                text: 'De seguimiento a su queja, le enviaremos su no. de referencia. Ingrese un correo electrónico.',
                input: 'email',
                inputAttributes: {
                  autocapitalize: 'off'
                },
                confirmButtonColor: '#5cb85c',
                confirmButtonText: 'Enviar',
                showLoaderOnConfirm: true,
                validationMessage:'Dirección no válida.',
                preConfirm: (data) => {
                    return data.value
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: 'Espere...',
                        text: 'Se le está enviando el correo de confirmación.',
                        didOpen: () => {
                            Swal.showLoading()
                            $.ajax({
                                url: window.location.pathname,
                                method: 'POST',
                                data: {
                                    'action': 'crqueja',
                                    'razon': razon,
                                    'tienda': tienda,
                                    'email': result.value
                                },
                                headers: {'X-CSRFToken': csrftoken}
                            }).done(function (data) {
                                if(!data.hasOwnProperty('error')){
                                    Swal.fire({
                                        icon: 'success',
                                        title: '¡Enviado!',
                                        text: 'Queja creada. Revise su correo.',
                                    })
                                    deptos.val(null).trigger("change");
                                    $('#summernote').summernote('code','');
                                    return false
                                }
                                Swal.fire({
                                    icon: 'error',
                                    title: '¡Error!',
                                    text: 'Los datos no pudieron ser guardados.',
                                })
                            }).fail(function (data){
                                Swal.fire({
                                    icon: 'error',
                                    title: '¡Error!',
                                    text: 'Algo ha dio mal. Intente nuevamente',
                                })
                            })
                        }
                    })
                }
            })
        } else {
            e.preventDefault();
            Swal.fire({
                icon: 'warning',
                title: '¡Campos vacíos!',
                text: 'Todos los campos son obligatorios',
            })
        }
    });
})