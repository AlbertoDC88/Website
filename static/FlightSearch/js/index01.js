$("#Return").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    minDate:  new Date()
    });
$("#Departure").datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    onSelect: function(){
        $('#Return').datepicker('option', 'minDate', $("#Departure").datepicker("getDate"));
    }
    });