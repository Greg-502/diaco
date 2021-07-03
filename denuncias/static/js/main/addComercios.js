const Toast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 3000,
});

var todos = $('select[name=allnegocios]');
var newCom = $('#inputNegocio');
var newSuc = $('#inputSucursal');

$(() => {
    comercios.click(function(e){
        e.preventDefault();
        $('#myModal').modal("show");
        var allopc = '<option value="">Negocios *</option>'

        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: {'action': 'allneg'},
            dataType: 'JSON',
            headers: {'X-CSRFToken': csrftoken}
        }).done(function (data){
            if(!data.hasOwnProperty('error')){
                $.each(data, function(key, value){
                    allopc += '<option value="'+value.pk+'">'+ value.all +'</option>'
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
            todos.html(allopc);
        })
    })

    addCom.click(function(){
        var inputNegocio = newCom.val()
        var allopc = '<option value="">Negocios *</option>'

        if (inputNegocio != '') {
            $.ajax({
                url: window.location.pathname,
                method: 'POST',
                data: {
                    'action': 'addCom',
                    'inputNegocio': inputNegocio,
                },
                dataType: 'JSON',
                headers: {'X-CSRFToken': csrftoken}
            }).done(function (data) {
                if(!data.hasOwnProperty('error')){
                    Toast.fire({
                        icon: 'success',
                        title: 'Guardado.'
                    });

                    $.ajax({
                        url: window.location.pathname,
                        method: 'POST',
                        data: {'action': 'allneg'},
                        dataType: 'JSON',
                        headers: {'X-CSRFToken': csrftoken}
                    }).done(function (data){
                        if(!data.hasOwnProperty('error')){
                            $.each(data, function(key, value){
                                allopc += '<option value="'+value.pk+'">'+ value.all +'</option>'
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
                        todos.html(allopc);
                    })
                    return false
                }
                Toast.fire({
                    icon: 'warning',
                    title: 'Ya existe.'
                });
            }).fail(function (data){
                Toast.fire({
                    icon: 'error',
                    title: 'Algo salió mal.'
                });
            }).always(function (data){
                newCom.val('')
            });
        } else {
            Toast.fire({
                icon: 'warning',
                title: 'Llene el campo.'
            });
        }
    })

    addSuc.click(function(){
        var idMux = municipios.val()
        var idAll = todos.val()
        var inputSuc = newSuc.val()

        if (idMux && idAll && inputSuc) {
            $.ajax({
                url: window.location.pathname,
                method: 'POST',
                data: {
                    'action': 'addScr',
                    'inputSuc': inputSuc,
                    'idMux': idMux,
                    'idAll': idAll
                },
                dataType: 'JSON',
                headers: {'X-CSRFToken': csrftoken}
            }).done(function(data) {
                if(!data.hasOwnProperty('error')){
                    Toast.fire({
                        icon: 'success',
                        title: 'Agregado.'
                    });

                    $('#myModal').modal('hide');
                    municipios.val(null).trigger("change");
                    newSuc.val(null).trigger("change");
                    return false
                }
                Toast.fire({
                    icon: 'warning',
                    title: 'Algo salió mal.'
                });
            }).fail(function(data) {
                Toast.fire({
                    icon: 'error',
                    title: 'Algo salió mal.'
                });
            })
        } else {
            Toast.fire({
                icon: 'warning',
                title: 'Campos faltantes.'
            });
        }
    })
})