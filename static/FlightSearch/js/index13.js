 $("#Departure").datepicker({
            defaultDate: new Date(),
            minDate: new Date(),
            onSelect: function(dateStr) 
            {         
                $("#Return").val(dateStr);
                $("#Return").datepicker("option",{ minDate: new Date(dateStr)})
            }
        });

$('#Return').datepicker({
        });