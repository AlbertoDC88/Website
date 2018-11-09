$j("#Departure").datepicker({
			dateFormat: 'dd/mm/yy',
			firstDay: 1 ,
            defaultDate: new Date(),
            minDate: new Date(),
            onSelect: function(date) 
            {         
                $j("#Return").datepicker("option",{ minDate: new Date(date)})
            }
        });

$j('#Return').datepicker({
	dateFormat: 'dd/mm/yy',
	firstDay: 1 ,
        });