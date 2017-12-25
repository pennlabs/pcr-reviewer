$(document).ready(function() {
    $("#tags").selectize({
        delimeter: ",",
        persist: false,
        create: function(input) {
            var out = input.toLowerCase();
            return {
                value: out,
                text: out
            };
        },
        load: function(query, callback) {
            if (!query.length) {
                callback();
            }
            $.get(TAG_ENDPOINT + "?query=" + encodeURIComponent(query), function(data) {
                callback(data.tags.map(function(v) { return { "text": v, "value": v }; }));
            });
        }
    });
    $("#comments").sortable().disableSelection();
    $("form").submit(function() {
        $("#order").val($("#comments .comment").map(function() { return $(this).attr("data-id"); }).get().join());
    });
});
