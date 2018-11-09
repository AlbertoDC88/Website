$("#Departure").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    minDate:  new Date()
    }).datepicker("setDate", new Date());
$("#Return").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    onSelect: function(){
        $('#Departure').datepicker('option', 'minDate', $("#Return").datepicker("getDate"));
    }
    }).datepicker("setDate", new Date());