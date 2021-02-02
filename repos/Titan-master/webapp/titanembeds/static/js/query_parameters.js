/* global $ */
(function () {
    "use strict";
    function updateQueryParameters() {
        let baseURL = window.location.origin + "/embed/" + $("#queryparam_guildid").val();
        let inputs = $("input.queryparam");
        let url = baseURL;
        for (let i = 0; i < inputs.length; i++) {
            let input = $(inputs[i]);
            let name = input.attr("name");
            let value = input.val().trim();
            if (!value) {
                continue;
            }
            if (!url.includes("?")) {
                url += "?";
            } else {
                url += "&";
            }
            if (value.startsWith(`${name}=`)) {
                value = value.substr(name.length + 1);
            }
            url += `${name}=${value}`;
        }
        $("#queryparam_url").val(url);
        $("#queryparam_iframe").val("<iframe src=\"" + url + "\" height=\"600\" width=\"800\" frameborder=\"0\"></iframe>");
    }
    
    $(function () {
        $("input.queryparam").change(updateQueryParameters);
        $("#queryparam_guildid").change(updateQueryParameters);
        updateQueryParameters();
    });
})();