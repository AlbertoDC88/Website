function collision($div1, $div2) {
      var x1 = $div1.offset().left;
      var w1 = 40;
      var r1 = x1 + w1;
      var x2 = $div2.offset().left;
      var w2 = 40;
      var r2 = x2 + w2;
        
      if (r1 < x2 || x1 > r2) return false;
      return true;
      
    }
    
// // slider call

$j('#slider').slider({
	range: true,
	min: {{ MinTTime }},
	max: {{ MaxTTime }},
	values: [ {{ MinTTime }}, {{ MaxTTime }} ],
	slide: function(event, ui) {
		
		$j('.ui-slider-handle:eq(0) .price-range-min').html('$' + ui.values[ 0 ]);
		$j('.ui-slider-handle:eq(1) .price-range-max').html('$' + ui.values[ 1 ]);
		$j('.price-range-both').html('<i>$' + ui.values[ 0 ] + ' - </i>$' + ui.values[ 1 ] );
		
		//
		
    if ( ui.values[0] == ui.values[1] ) {
      $j('.price-range-both i').css('display', 'none');
    } else {
      $j('.price-range-both i').css('display', 'inline');
    }
        
        //
		
		if (collision($j('.price-range-min'), $('.price-range-max')) == true) {
			$j('.price-range-min, .price-range-max').css('opacity', '0');	
			$j('.price-range-both').css('display', 'block');		
		} else {
			$j('.price-range-min, .price-range-max').css('opacity', '1');	
			$j('.price-range-both').css('display', 'none');		
		}
		
	}
});

$j('.ui-slider-range').append('<span class="price-range-both value"><i>$' + $j('#slider').slider('values', 0 ) + ' - </i>' + $j('#slider').slider('values', 1 ) + '</span>');

$j('.ui-slider-handle:eq(0)').append('<span class="price-range-min value">$' + $j('#slider').slider('values', 0 ) + '</span>');

$j('.ui-slider-handle:eq(1)').append('<span class="price-range-max value">$' + $j('#slider').slider('values', 1 ) + '</span>');
			