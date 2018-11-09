 $j.datepicker.setDefaults({

	firstDay: 1 ,
});
 
 $j("#Departure").datepicker({
            defaultDate: new Date(),
            minDate: new Date(),
			dateFormat: 'dd/mm/yy',
            onSelect: function(dateStr) 
            {         
                $j("#Return").val(dateStr);
                $j("#Return").datepicker("option",{ minDate: new Date(dateStr)})
            }
        });

$j('#Return').datepicker({
		dateFormat: 'dd/mm/yy',
        });