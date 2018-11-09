$j("#Departure").datepicker({
			dateFormat: 'dd/mm/yy',
			firstDay: 1 ,
            defaultDate: new Date(),
            minDate: new Date(),
            onSelect: function(dateStr) 
            {         
                $j("#Return").datepicker("option",{ minDate: new Date(dateStr), dateFormat: 'dd/mm/yy' })
            }
        });

$j('#Return').datepicker({
	dateFormat: 'dd/mm/yy',
	firstDay: 1 ,
        });