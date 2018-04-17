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
    $(".rank").keydown(function(e) {
        if (isFinite(e.key)) {
            $(this).val(e.key);
        }
        var next = $(this).closest(".comment").next().find(".rank");
        if (next.length) {
            next.focus();
        }
        else {
            $("button[type='submit']").focus();
        }
        if (e.key.length == 1) {
            e.preventDefault();
        }
    });
    $(".rank").first().focus();
    $("form").submit(function(e) {
        var order = $("#comments .comment").map(function() { return {"id": $(this).attr("data-id"), "rank": $(this).find(".rank").val()}; }).get();
        var items = [null, null, null, null, null];
        $.each(order, function(k, v) {
            var rank = parseInt(v.rank);
            if (!rank || rank < 1 || rank > 5) {
                Messenger().error("Please rank comments from 1 to 5!");
                e.preventDefault();
                return false;
            }
            else {
                if (items[rank - 1] !== null) {
                    Messenger().error("Please give each comment a unique ranking!");
                    e.preventDefault();
                    return false;
                }
                items[rank - 1] = v.id;
            }
        });
        $("#order").val(items.filter(rank => rank !== null).reverse().join());
        $("#comments .comment").each(function() {
            var id = $(this).attr("data-id");
            var mark = $(this).find(".mark").attr("value");
            var inap = $(this).find(".inappropriate").attr("value");
            $(this).find("input[name=flags_" + id + "]").val(inap == "true" ? "inappropriate" : (mark == "true" ? "mark" : ""));
        });
    });
});
