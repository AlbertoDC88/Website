   $.datepicker.setDefaults({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd/mm/yy'});
    $('#Departure').datepicker({
        minDate: '+0',
        onSelect: function(dateStr) {
            var min = $(this).datepicker('getDate') || new Date(); // Selected date or today if none
            var max = new Date(min.getTime());
            max.setMonth(max.getMonth() + 1); // Add one month
            $('#Return').datepicker('option', {minDate: min, maxDate: max});
        }
    });
    $('#Return').datepicker({
        minDate: '+0',
        maxDate: '+1m',
        onSelect: function(dateStr) {
            var max = $(this).datepicker('getDate'); // Selected date or null if none
            $('#Departure').datepicker('option', {maxDate: max});
        }
    });