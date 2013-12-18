$(document).ready(function() {
	$('.password_strength').keyup(function() {
		if( $(this).val() ) {
			result = zxcvbn( $(this).val() );

			if( result.score < 3 ) {
				$('#password_strength_bar').removeClass('progress-bar-success').addClass('progress-bar-warning');
				$('#password_strength_info').html('<span class="label label-danger">Warning</span> This password would take <em>'+result.crack_time_display+'</em> to crack.');
			} else {
				$('#password_strength_bar').removeClass('progress-bar-warning').addClass('progress-bar-success');
				$('#password_strength_info').html('This password would take <em>'+result.crack_time_display+'</em> to crack.');
			}

			$('#password_strength_bar').width( ((result.score+1)/5)*100 + '%' );

		} else {
			$('#password_strength_bar').removeClass('progress-bar-success').addClass('progress-bar-warning');
			$('#password_strength_bar').width( '0%' );
			$('#password_strength_info').html('');
		}
	})
})