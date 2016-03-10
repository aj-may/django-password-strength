(function($, window, document, undefined){
    window.djangoPasswordStrength = {
        config: {
            passwordClass: 'password_strength',
            confirmationClass: 'password_confirmation'
        },

        init: function (config) {
            var self = this;
            // Setup configuration
            if ($.isPlainObject(config)) {
                $.extend(self.config, config);
            }

            $(".jquery_ui_progress_bar").progressbar({
              value: 0
            });

            self.initListeners();
        },

        initListeners: function() {
            var self = this;
            var body = $('body');
            var passwordClassSelector = $('.' + self.config.passwordClass);

            passwordClassSelector.keyup($.debounce(250, function() {
                var password_strength_bar_jquery_ui = $(this).parent().find('.jquery_ui_progress_bar');
                var password_strength_bar_bootstrap = $(this).parent().find('.password_strength_bar');
                var password_strength_info = $(this).parent().find('.password_strength_info');
                var password_warning_info = $(this).parent().find('.password_warning_info');
                var password_suggestions_list = $(this).parent().find('.password_suggestions');
                $(document).trigger("passwordStrengthPasses", [false]);

                var passwordValue = $(this).val();
                if( $(this).val() ) {
                    var result = zxcvbn( $(this).val() );

                    if (result.score >= self.min_score()) {
                        $(document).trigger("passwordStrengthPasses", [true]);
                    } else {
                        $(document).trigger("passwordStrengthPasses", [false]);
                    }

                    if (password_strength_bar_bootstrap.length) {
                        self.update_progress_bar_bootstrap(password_strength_bar_bootstrap, result);
                    } else if (password_strength_bar_jquery_ui.length) {
                        self.update_progress_bar_jquery_ui(password_strength_bar_jquery_ui, result);
                    }

                    self.update_strength_message(password_strength_info, result);
                    self.update_password_suggestions(password_suggestions_list, result);
                    self.update_password_warning_info(password_warning_info, result, passwordValue);
                } else {
                    if (password_strength_bar_bootstrap.length) {
                        self.hide_progress_bar_bootstrap(password_strength_bar_bootstrap);
                    } else if (password_strength_bar_jquery_ui.length) {
                        self.hide_progress_bar_jquery_ui(password_strength_bar_jquery_ui);
                    }
                    password_strength_info.addClass("hidden");
                    password_suggestions_list.addClass("hidden");
                    password_warning_info.addClass("hidden");
                }
                self.match_passwords( $(this) );
            }));

            $('.' + self.config.confirmationClass).keyup($.debounce(400, function() {
                var password_field;
                var confirm_with = $(this).data('confirm-with');
                if( confirm_with ) {
                    password_field = $('#' + confirm_with);
                } else {
                    password_field = passwordClassSelector;
                }
                self.match_passwords(password_field);
            }));
        },

        update_progress_bar_bootstrap: function(password_strength_bar, result_zxcvbn) {
            if( result_zxcvbn.score < this.min_score() ) {
                password_strength_bar.removeClass('progress-bar-success').addClass('progress-bar-warning');
            } else {
                password_strength_bar.removeClass('progress-bar-warning').addClass('progress-bar-success');
            }

            var strength_1_to_5 = result_zxcvbn.score + 1;
            var strength_out_of_100 = ((strength_1_to_5)/5)*100;
            password_strength_bar.width(strength_out_of_100 + '%').attr('aria-valuenow', strength_1_to_5);
        },

        hide_progress_bar_bootstrap: function(password_strength_bar) {
            password_strength_bar.removeClass('progress-bar-success').addClass('progress-bar-warning');
            password_strength_bar.width('0%').attr('aria-valuenow', 0);
        },

        update_progress_bar_jquery_ui: function(password_strength_bar, result_zxcvbn) {
            var color = "#00B200"; // Green

            if( result_zxcvbn.score < this.min_score() ) {
                color = "#FF0000"; // Red
            } else if ( result_zxcvbn.score == this.min_score() ) {
                color = "#FFAE19"; // Orange
            }

            var progressBarValue = password_strength_bar.find(".ui-progressbar-value");
            progressBarValue.css({"background": color});

            var strength_1_to_5 = result_zxcvbn.score + 1;
            var strength_out_of_100 = ((strength_1_to_5)/5)*100;
            password_strength_bar.progressbar( "option", {
              value: strength_out_of_100
            });
        },

        hide_progress_bar_jquery_ui: function(password_strength_bar) {
            password_strength_bar.progressbar({
              value: 0
            });
        },

        update_strength_message: function(strength_info, result_zxcvbn) {
            if(result_zxcvbn.score < this.min_score()) {
                strength_info.find('.label').removeClass('hidden');
            } else {
                strength_info.find('.label').addClass('hidden');
            }

            // Django hashes with the PBKDF2 algorithm (by default). The zxcvbn documentation describes this as a
            // 'slow hashing' algorithm, so display value 'offline_slow_hashing_1e4_per_second' is used. Code could be
            // added here, to optionally show the online attack times.
            strength_info.find('.password_strength_time').html(
                result_zxcvbn.crack_times_display.offline_slow_hashing_1e4_per_second);
            strength_info.removeClass('hidden');
        },

        update_password_warning_info: function(password_warning_info, result_zxcvbn, password) {
            if (password.length > this.max_length()) {
                this.set_password_warning_info_text(
                    password_warning_info,
                    "Your password must be less than " + this.max_length() + " characters long.")
            } else if (password.length < this.min_length()) {
                this.set_password_warning_info_text(
                    password_warning_info,
                    "Your password must be at least " + this.min_length() + " characters long.")
            } else if (result_zxcvbn.score < this.min_score() && result_zxcvbn.feedback.warning != "") {
                this.set_password_warning_info_text(password_warning_info, result_zxcvbn.feedback.warning)
            } else {
                password_warning_info.find('.label').addClass('hidden');
                password_warning_info.addClass('hidden');
            }
        },

        set_password_warning_info_text: function(password_warning_info, text) {
            password_warning_info.find('.label').removeClass('hidden');
            password_warning_info.find('.password_warning_message').html(text);
            password_warning_info.removeClass('hidden');
        },

        update_password_suggestions: function(suggestions_list, result_zxcvbn) {
            if (result_zxcvbn.feedback.suggestions.length > 0) {
                suggestions_list.removeClass('hidden');  // We have suggestion, so make sure we aren't hidden.
                // Grab an existing suggestion and clone it, we'll use it as a template for new suggestions.
                var empty_suggestion_template = suggestions_list.find('.password_suggestion').first().clone();
                suggestions_list.html(""); // Clear out old suggestions.

                for (var i = 0; i < result_zxcvbn.feedback.suggestions.length; i++) {
                    var new_suggestion = empty_suggestion_template.clone();
                    new_suggestion.find('.suggestion_text').html(result_zxcvbn.feedback.suggestions[i]);
                    suggestions_list.append(new_suggestion);
                }
            } else {
                suggestions_list.addClass('hidden');
            }
        },

        min_score: function() {
            return parseInt($("#zxcvbn_score_info").data('min-score'));
        },

        min_length: function() {
            return parseInt($("#zxcvbn_score_info").data('min-length'));
        },

        max_length: function() {
            return parseInt($("#zxcvbn_score_info").data('max-length'));
        },

        match_passwords: function(password_field, confirmation_fields) {
            var self = this;
            // Optional parameter: if no specific confirmation field is given, check all
            if( confirmation_fields === undefined ) { confirmation_fields = $('.' + self.config.confirmationClass) }
            if( confirmation_fields === undefined ) { return; }

            var password = password_field.val();

            confirmation_fields.each(function(index, confirm_field) {
                var confirm_value = $(confirm_field).val();
                var confirm_with = $(confirm_field).data('confirm-with');

                if( confirm_with && confirm_with == password_field.attr('id')) {
                    if( confirm_value && password ) {
                        if (confirm_value === password) {
                            $(confirm_field).parent().find('.password_strength_info').addClass('hidden');
                        } else {
                            $(confirm_field).parent().find('.password_strength_info').removeClass('hidden');
                        }
                    } else {
                        $(confirm_field).parent().find('.password_strength_info').addClass('hidden');
                    }
                }
            });

            // If a password field other than our own has been used, add the listener here
            if( !password_field.hasClass(self.config.passwordClass) && !password_field.data('password-listener') ) {
                password_field.keyup($.debounce(250, function() {
                    self.match_passwords($(this));
                }));
                password_field.data('password-listener', true);
            }
        }
    };

    // Call the init for backwards compatibility
    djangoPasswordStrength.init();

})(jQuery, window, document);
