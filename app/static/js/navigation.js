function navigateToHomePage() {
    window.location.href = appData.userProfilesEndpoint;
}

function navigateToProfileSearch(filterParam) {
    var urlWithQueryParam = appData.userProfilesFilter + '?type=' + encodeURIComponent(filterParam);
    window.location.href = urlWithQueryParam;
}
