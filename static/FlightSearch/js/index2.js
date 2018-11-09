//$("#Departure").datepicker({ 
//    dateFormat: 'dd/mm/yy',
//    changeMonth: true,
//	changeYear: true,
//	autosize: true,
//    minDate: new Date(),
//    onSelect: function(date){
//
//       //Set Minimum Date of EndDatePicker After Selected Date of StartDatePicker
//        $("#Return").datepicker( "option", "minDate", $("#txtStartDate").datepicker("getDate")); );
//
//    }
//});
//
//$("#Return").datepicker({ 
//    autosize: true,
//	dateFormat: "dd/mm/yy"
//    changeMonth: true
//	changeYear: true,
//});

$("#Departure").datepicker({
  showOn: "both",       
  onSelect: function(dateText, inst){
     $("#Return").datepicker("option","minDate",
     $("#Departure").datepicker("getDate"));
  }
});

$("#Return").datepicker(); //it is not working with out this line