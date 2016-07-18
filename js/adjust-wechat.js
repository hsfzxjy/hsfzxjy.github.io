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