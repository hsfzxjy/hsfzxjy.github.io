$(function () {
    function isWX() {
        var ua = navigator.userAgent.toLowerCase()
        return /micromessenger/.test(ua)
    }

    if (isWX()) {
        $(".categories a, .tags a").click(function (e) {
            e.preventDefault()
        })
    } else {
        autoResizeNav()
    }
})

$(window).scroll(function () {
    $(window).scrollTop() > 100 ? $("#rocket").addClass("show") : $("#rocket").removeClass("show")
})
$("#rocket").click(function () {
    $("#rocket").addClass("launch")
    $("html, body").animate(
        {
            scrollTop: 0,
        },
        500,
        function () {
            $("#rocket").removeClass("show launch")
        }
    )
    return false
})

$(() => {
    const $toggleButton = $("span.toggle-menu")
    const $rightPanel = $("#right-panel")

    $toggleButton.click(() => {
        $rightPanel.toggleClass("show")
    })
})

function throttle(f, time) {
    let lastTime = null
    return function (...args) {
        let current = Date.now()
        if (lastTime !== null && current - lastTime < time) {
            return
        }
        lastTime = current
        return f.bind(this)(...args)
    }
}

function autoResizeNav() {
    const $navMenuContainer = document.querySelector("#nav-menu > div")
    const $navMenu = document.getElementById("nav-menu")

    function process() {
        const threshold = 2
        $navMenu.classList.toggle("left", $navMenuContainer.scrollLeft > threshold)
        $navMenu.classList.toggle(
            "right",
            $navMenuContainer.scrollLeft + $navMenuContainer.clientWidth + threshold < $navMenuContainer.scrollWidth
        )
        console.log($navMenuContainer.scrollLeft, $navMenuContainer.clientWidth, $navMenuContainer.scrollWidth)
    }

    new ResizeObserver(throttle(process, 100)).observe($navMenuContainer)
    $navMenuContainer.addEventListener("scroll", throttle(process, 10))
}
