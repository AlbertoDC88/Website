$("#Return").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    minDate:  new Date()
    }).datepicker("setDate", new Date());
$("#Departure").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    onSelect: function(){
        $('#Return').datepicker('option', 'minDate', $("#Departure").datepicker("getDate"));
    }
    }).datepicker("setDate", new Date());