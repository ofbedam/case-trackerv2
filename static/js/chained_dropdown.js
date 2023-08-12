$(document).ready(function () {
    $('#id_country').select2({
        placeholder: 'Select a country.JS Static..',
        ajax: {
            url: '/kurumlar/country-autocomplete/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term,
                };
            },
            processResults: function (data) {
                return {
                    results: data,
                };
            },
            cache: true,
        },
        minimumInputLength: 0,
    });

    $('#id_state').select2({
        placeholder: 'Select a state..js.',
        ajax: {
            url: '/kurumlar/state-autocomplete/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term,
                    country_id: $('#id_country').val(),
                };
            },
            processResults: function (data) {
                return {
                    results: data,
                };
            },
            cache: true,
        },
        minimumInputLength: 0,
    });

    $('#id_city').select2({
        placeholder: 'Select a city.js..',
ajax: {
url: '/kurumlar/city-autocomplete/',
dataType: 'json',
delay: 250,
data: function (params) {
return {
q: params.term,
state_id: $('#id_state').val(),
};
},
processResults: function (data) {
return {
results: data,
};
},
cache: true,
},
minimumInputLength: 0,
});
});
