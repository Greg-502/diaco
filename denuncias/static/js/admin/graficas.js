var update = $('#btnRefesh');

const Toast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 3000,
});

$(() => { 
    var regiones = [];
    var deptos = [];
    var negocios = [];
    var fechas = [];
    var quejas = [];
    var bgColor = [];
    var bgBorder = [];

    contador();
    radiales();
    pie();
    barras();
    lineal();
    mapa();
})

update.click(function (e) {
    contador();
    radiales();
    pie();
    barras();
    lineal();
    mapa();
});

function contador(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'count'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            let medidor = $('#counter')
            medidor.html('<h1>'+data+'</h1>')
            return false
        }
        Toast.fire({
            icon: 'warning',
            title: 'Algo salió mal.'
        });
    }).fail(function(data){
        Toast.fire({
            icon: 'error',
            title: 'Algo salió mal.'
        });
    })
}

function radiales(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'radial'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            var obj = data;
            
            regiones = [];
            quejas = [];
            bgColor = [];
            
            $.each(obj, function(i, item){
                var r = Math.random() * 255;
                r = Math.round(r)
                var g = Math.random() * 255;
                g = Math.round(g)
                var b = Math.random() * 255;
                b = Math.round(b)
                regiones.push(item.regiones)
                quejas.push(item.totales)
                bgColor.push('rgba('+r+', '+g+', '+b+', 0.8)')
            })
            
            $('#radial').remove();
            $('#contenedor_radial').append("<canvas id='radial'></canvas>")
            
            var ctx = $('#radial');
            var stackedLine = new Chart(ctx, {
                responsive: true,
                type: 'polarArea',
                data: {
                    labels: regiones,
                    datasets: [{
                        label: '',
                        data: quejas,
                        backgroundColor: bgColor,
                        borderWidth: 1
                    }]
                },
                options: {
                    legend: {
                        display: false
                    }
                }
            });
            return false;
        }
    })
}

function pie(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'pie'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            var obj = data;
            negocios = []
            quejas = []
            bgColor = []
            
            $.each(obj, function(i, item){
                var r = Math.random() * 255;
                r = Math.round(r)
                var g = Math.random() * 255;
                g = Math.round(g)
                var b = Math.random() * 255;
                b = Math.round(b)
                negocios.push(item.negocios)
                quejas.push(item.totales)
                bgColor.push('rgba('+r+', '+g+', '+b+', 0.8)')
            })
            
            $('#pie').remove()
            $('#contenedor_anillo').append("<canvas id='pie'></canvas>")
            
            var ctx = $('#pie');
            var stackedLine = new Chart(ctx, {
                responsive: true,
                type: 'doughnut',
                data: {
                    labels: negocios,
                    datasets: [{
                        label: '',
                        data: quejas,
                        backgroundColor: bgColor,
                        borderWidth: 1
                    }]
                },
                options: {
                    legend: {
                        display: false
                    },
                }
            });
            return false;
        }
    });
}

function barras(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'barra'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            var obj = data;
            
            deptos = []
            quejas = []
            bgColor = []
            
            $.each(obj, function(i, item){
                var r = Math.random() * 255;
                r = Math.round(r)
                var g = Math.random() * 255;
                g = Math.round(g)
                var b = Math.random() * 255;
                b = Math.round(b)
                deptos.push(item.deptos)
                quejas.push(item.totales)
                bgColor.push('rgba('+r+', '+g+', '+b+', 0.8)')
            })
            
            $('#bars').remove()
            $('#contenedor_barra').append("<canvas id='bars'></canvas>")
            var ctx = $('#bars');
            var stackedLine = new Chart(ctx, {
                responsive: true,
                type: 'bar',
                data: {
                    labels: deptos,
                    datasets: [{
                        label: 'Quejas',
                        data: quejas,
                        backgroundColor: bgColor,
                        borderWidth: 1
                    }]
                },
                options:{
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            return false;
        }
    })
}

function lineal(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'lineal'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            var obj = data;
            fechas = []
            quejas = []
            bgColor = []
            
            $.each(obj, function(i, item){
                var r = Math.random() * 255;
                r = Math.round(r)
                var g = Math.random() * 255;
                g = Math.round(g)
                var b = Math.random() * 255;
                b = Math.round(b)
                fechas.push(item.creado)
                quejas.push(item.totales)
                bgColor.push('rgba('+r+', '+g+', '+b+', 0.8)')
            })
            
            $('#line').remove()
            $('#contenedor_lineal').append("<canvas id='line'></canvas>")
            
            var ctx = $('#line');
            var stackedLine = new Chart(ctx, {
                responsive: true,
                type: 'line',
                data: {
                    labels: fechas,
                    datasets: [
                        {
                            label: 'Quejas',
                            fill: true,
                            lineTension: 0.0,
                            backgroundColor:'rgba(45,143,229,0.4)',
                            borderColor:'rgba(45,143,229,1)',
                            borderCapStyle: 'butt',
                            borderDash:[],
                            pointBorderWidth:5,
                            data: quejas,
                            spanGaps: false,
                        }
                    ]
                },
                options: {
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            return false
        }
    })
}

function mapa(){
    $.ajax({
        url: window.location.pathname,
        method:"POST",
        data:{'action':'mapas'},
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            var obj = data;
            totales = [];
            x = [];
            
            $.each(obj, function (i, key) {
                x.push({"hc-key": key.mapa,
                value: key.totales,
            });
        });
        
        var data = x;
        
        Highcharts.mapChart('container', {
            chart: {
                map: 'countries/gt/gt-all'
            },
            
            title: {
                text: 'Denuncias activas.'
            },
            
            subtitle: {
                text: 'Distribución e incidencia en el territorio nacional.'
            },
            
            colorAxis: {
                min: 0
            },
            
            series: [{
                data: data,
                name: 'Quejas',
                joinBy: "hc-key",
                states: {
                    hover: {
                        color: '#BADA55'
                    }
                }
            }]
        });
        return false;
    }
    Toast.fire({
        icon: 'warning',
        title: 'No se cargó el mapa.'
    });
    }).fail(function(data){
        Toast.fire({
            icon: 'error',
            title: 'No se cargó el mapa.'
        });
    });
}