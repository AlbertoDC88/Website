 $j("#Departure").datepicker({
            defaultDate: new Date(),
            minDate: new Date(),
            onSelect: function(dateStr) 
            {         
                $j("#Return").val(dateStr);
                $j("#Return").datepicker("option",{ minDate: new Date(dateStr)})
            }
        });

$j('#Return').datepicker({
        });