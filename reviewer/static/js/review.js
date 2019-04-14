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
    $(".inappropriate").click(function(e) {
        e.preventDefault();
        if ($(this).attr("value") != "true") {
            $(this).text("Flagged").attr("value", "true");
        }
        else {
            $(this).text("Flag as Inappropriate").attr("value", "false");
        }
    });
    $(".mark").click(function(e) {
        e.preventDefault();
        if ($(this).attr("value") != "true") {
            $(this).text("Marked").attr("value", "true");
        }
        else {
            $(this).text("Mark as Not Useful").attr("value", "false");
        }
    });
    $(".approve").click(function(e) {
        e.preventDefault();
        if ($(this).attr("value") != "true") {
            $(this).text("Approved").attr("value", "true");
        }
        else {
            $(this).text("Approve Comment").attr("value", "false");
        }
    });
    $("form").submit(function(e) {
        $("#order").val(items.filter(rank => rank !== null).reverse().join());
        var mark = $(this).find(".mark").attr("value");
        var inap = $(this).find(".inappropriate").attr("value");
        var appr = $(this).find(".approve").attr("value");
        $(this).find("input[name=flag]").val(inap == "true" ? "I" : (mark == "true" ?  "M" : (appr == "true" ? "A" : "")));
    });
});
