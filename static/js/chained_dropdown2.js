#static/js/chained_dropdown.js

$(document).ready(function () {
    // Set up change event for country dropdown
    $('#id_country').change(function () {
        var countryId = $(this).val();

        // Clear and disable state and city dropdowns
        $('#id_state').empty().prop('disabled', true);
        $('#id_city').empty().prop('disabled', true);

        // Fetch states based on selected country using Ajax
        $.ajax({
            url: '/get_states/',  // Change this URL to your view for fetching states
            data: {'country_id': countryId},
            success: function (data) {
                // Populate state dropdown
                $('#id_state').append($('<option>', { value: '', text: '--- Select State ---' }));
                $.each(data.states, function (key, value) {
                    $('#id_state').append($('<option>', { value: key, text: value }));
                });
                $('#id_state').prop('disabled', false);
            }
        });
    });

    // Set up change event for state dropdown
    $('#id_state').change(function () {
        var stateId = $(this).val();
        var countryId = $('#id_country').val();

        // Clear and disable city dropdown
        $('#id_city').empty().prop('disabled', true);

        // Fetch cities based on selected state and country using Ajax
        $.ajax({
            url: '/get_cities/',  // Change this URL to your view for fetching cities
            data: {'country_id': countryId, 'state_id': stateId},
            success: function (data) {
                // Populate city dropdown
                $('#id_city').append($('<option>', { value: '', text: '--- Select City ---' }));
                $.each(data.cities, function (key, value) {
                    $('#id_city').append($('<option>', { value: key, text: value }));
                });
                $('#id_city').prop('disabled', false);
            }
        });
    });
});
