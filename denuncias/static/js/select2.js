$('select').select2({
	theme: 'bootstrap4',
    language: {
        noResults: function() {
          return "Ninguna coincidencia";        
        },
        searching: function() {
          return "Espere...";
        }
    }
}).on('select2:opening', function(e) {
  $(this).data('select2').$dropdown.find(':input.select2-search__field').attr('placeholder', 'Buscar')
})