$('#departure-date').calendar({
  type: 'date',
  formatter: {
    date: function (date, settings) {
      if (!date) return '';
      var day = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();
      return month + '/' + day + '/' + year;
    }
  }
});

$("#profile-search-form").on("submit", function(event) {
  var srcCountry = $("#id_src_country");
  var srcCountrySearch = $("#src-country-search");
  if (srcCountry.val().trim() === "") {
    srcCountrySearch.focus();
    return false;
  }

  var destCountry = $("#id_dest_country");
  var destCountrySearch = $("#dest-country-search");
  if (destCountry.val().trim() === "") {
    destCountrySearch.focus();
    return false;
  }

  var departureDate = $("#id_departure_date");
  if (departureDate.val().trim() === "") {
    departureDate.focus();
    return false;
  }
});