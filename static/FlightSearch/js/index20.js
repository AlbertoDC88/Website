$j("#Departure").datepicker({
			dateFormat: 'dd/mm/yy',
			firstDay: 1 ,
			minDate: new Date(),
            onSelect: function(dateText, inst){
				$j("#Return").datepicker("option","minDate",
				$j("#Departure").datepicker("getDate"));
			}
        });

$j('#Return').datepicker({
	dateFormat: 'dd/mm/yy',
	firstDay: 1 ,
        });