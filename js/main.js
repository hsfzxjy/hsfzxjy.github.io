$(function () {
    function isWX() {
        var ua = navigator.userAgent.toLowerCase();
        return (/micromessenger/.test(ua)) ? true : false;
    }

    if (isWX()) {
        $("#header, .post-nav").remove();
        $(".categories a, .tags a").click(function (e) {
            e.preventDefault();
        })
    }
})

$(window).scroll(function () {
    $(window).scrollTop() > 100 ? $("#rocket").addClass("show") : $("#rocket").removeClass("show");
});
$("#rocket").click(function () {
    $("#rocket").addClass("launch");
    $("html, body").animate({
        scrollTop: 0
    }, 500, function () {
        $("#rocket").removeClass("show launch");
    });
    return false;
});

$(() => {
    const $toggleButton = $("span.toggle-menu")
    const $rightPanel = $("#right-panel")

    $toggleButton.click(() => {
        $rightPanel.toggleClass("show");
    })
})