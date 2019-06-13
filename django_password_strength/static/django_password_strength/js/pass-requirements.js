if (typeof jQuery === 'undefined') {
    throw new Error('PassRequirements requires jQuery')
}

(function ($) {
    $.fn.PassRequirements = function (options) {
        // Provide fake gettext for when it is not available
        if( typeof gettext !== 'function' ) { gettext = function(text) { return text; }; }
        /*
         * TODO
         * ====
         * 
         * store regexes in variables so they can be used by users through string 
         * specifications,ex 'number', 'special', etc
         * 
         */

        var defaults = {
//            defaults: true
        };

        if (
            !options ||                     //if no options are passed                                    /*
            options.defaults === true ||     //if default option is passed with defaults set to true      * Extend options with default ones
            options.defaults === undefined   //if options are passed but defaults is not passed           */
        ) {
            if (!options) {                   //if no options are passed,
                options = {};               //create an options object
            }
            defaults.rules = $.extend(true, {
                minlength: {
                    text: gettext("be at least minLength characters long"),
                    minLength: 8,
                },
                containSpecialChars: {
                    text: gettext("Your input should contain at least minLength special character"),
                    minLength: 1,
                    regex: '([^!%&@#$^*?_~])',
                    regex_flags: 'g'
                },
                containLowercase: {
                    text: gettext("Your input should contain at least minLength lower case character"),
                    minLength: 1,
                    regex: new RegExp('[^a-z]', 'g')
                },
                containUppercase: {
                    text: gettext("Your input should contain at least minLength upper case character"),
                    minLength: 1,
                    regex: new RegExp('[^A-Z]', 'g')
                },
                containNumbers: {
                    text: gettext("Your input should contain at least minLength number"),
                    minLength: 1,
                    regex: new RegExp('[^0-9]', 'g')
                }
            }, options.rules);
        } else {
            defaults = options;     //if options are passed with defaults === false
        }

        var i = 0;

        return this.each(function () {

            if (!defaults.defaults && !defaults.rules) {
                console.error('You must pass in your rules if defaults is set to false. Skipping this input with id:[' + this.id + '] with class:[' + this.classList + ']');
                return false;
            }

            var requirementList = "";
            $(this).data('pass-req-id', i++);

            $(this).keyup(function () {
                var this_ = $(this);
                Object.getOwnPropertyNames(defaults.rules).forEach(function (val, idx, array) {
                    var rules = defaults.rules[val];
                    if (typeof rules.regex == 'string') {
                        rules.regex = new RegExp(rules.regex, rules.regex_flags ? rules.regex_flags: null);
                    }
                    if (this_.val().replace(rules.regex, "").length > defaults.rules[val].minLength - 1) {
                        this_.next('.popover').find('#' + val).css('text-decoration', 'line-through');
                    } else {
                        this_.next('.popover').find('#' + val).css('text-decoration', 'none');
                    }

                })
            });

            Object.getOwnPropertyNames(defaults.rules).forEach(function (val, idx, array) {
                requirementList += (("<li id='" + val + "'>" + defaults.rules[val].text).replace("minLength", defaults.rules[val].minLength));
            });
            try {
                $(this).popover({
                    title: gettext('Password Requirements'),
                    trigger: options.trigger ? options.trigger : 'focus',
                    html: true,
                    placement: options.popoverPlacement ? options.popoverPlacement : 'auto bottom',
                    content: gettext('Your password should:') + '<ul>' + requirementList + '</ul>'
                });
            } catch (e) {
                throw new Error('PassRequirements requires Bootstraps Popover plugin');
            }
            $(this).focus(function () {
                $(this).keyup();
            });
        });
    };

}(jQuery));
