 $('#Return').datepicker({
            defaultDate: new Date(),
            onSelect: function(dateStr) {
            toDate = new Date(dateStr);

                // Converts date objects to appropriate strings
                fromDate = ConvertDateToShortDateString(fromDate);
                toDate = ConvertDateToShortDateString(toDate);
            }
        });
 
 $("#Departure").datepicker({
            defaultDate: new Date(),
            minDate: new Date(),
            onSelect: function(dateStr) 
            {         
                $("#Return").val(dateStr);
                $("#Return").datepicker("option",{ minDate: new Date(dateStr)})
            }
        });

