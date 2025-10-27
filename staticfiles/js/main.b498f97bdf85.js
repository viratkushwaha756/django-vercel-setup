(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);

    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500);
        return false;
    });

    // Simple carousel functionality (without owlCarousel)
    function initSimpleCarousel() {
        $('.carousel').each(function() {
            var $carousel = $(this);
            var $items = $carousel.find('.carousel-item');
            var currentIndex = 0;
            
            if ($items.length > 1) {
                // Add navigation buttons
                $carousel.append('<button class="carousel-control-prev" type="button"><i class="bi bi-arrow-left"></i></button>');
                $carousel.append('<button class="carousel-control-next" type="button"><i class="bi bi-arrow-right"></i></button>');
                
                // Show first item
                $items.hide().first().show();
                
                // Next button
                $carousel.find('.carousel-control-next').click(function() {
                    $items.eq(currentIndex).hide();
                    currentIndex = (currentIndex + 1) % $items.length;
                    $items.eq(currentIndex).show();
                });
                
                // Prev button
                $carousel.find('.carousel-control-prev').click(function() {
                    $items.eq(currentIndex).hide();
                    currentIndex = (currentIndex - 1 + $items.length) % $items.length;
                    $items.eq(currentIndex).show();
                });
                
                // Auto-play
                setInterval(function() {
                    $carousel.find('.carousel-control-next').click();
                }, 5000);
            }
        });
    }
    
    // Initialize carousels when document is ready
    $(document).ready(function() {
        initSimpleCarousel();
    });

})(jQuery);

