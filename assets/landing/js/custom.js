var ie = ie_version();


// Parameters
var p = {
	navbarScrollTop: $(window).height() / 4, // When add background to navbar
	scrollSpeed: 1000, // Smooth scrolling speed
	scrollOffset: 80, // For one page nav. Recomended to be as navbar height
	preloaderTimeout: 10000, // If loading is to long, hide overlay after N ms

	screen: { // Breakpoints. Like in bootstrap
		xs: 480,
		sm: 768,
		md: 992,
		lg: 1200
	}
};

var transitionEnd = 'transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd',
	animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';


// Loader
var loader = {
	show: function() {
		$('#loader').addClass('left opacity');
	},
	hide: function() {
		var $loader = $('#loader');

		$loader.removeClass('opacity');

		$loader.on(transitionEnd, function() {
			$loader.removeClass('left');
			$loader.unbind(transitionEnd);
		});
	}
};


var all = {
	// Preloader
	preloader: {
		init: function() {
			var $preloader = $('#preloader');

			$('body').css('overflow', 'hidden');

			setTimeout(function() {
				all.preloader.hide($preloader);
			}, p.preloaderTimeout);

			$(window).load(function() {
				all.preloader.hide($preloader);
			});
		},
		hide: function($preloader) {
			var $home_container = $('.home-section').find('.container');

			$('body').css('overflow', '');

			$preloader.addClass('animated fadeOut');
			$preloader.one(animationEnd, function() {
				$preloader.remove();
				$home_container.addClass('animated fadeInDown');
			});

			if(ie!== false && ie <= 9) {
				$preloader.fadeOut(300, function() {
					$preloader.remove();
					$home_container.animate({'opacity': 1}, 300);
				});
			}
		}
	},

	// Parallax
	parallax: function() {
		$('.home-section').parallax("50%", 0.7);
		$('#subscribe').parallax("50%", -0.3);
		$('#facts').parallax("50%", -0.6);
		$('.shape').parallax("50%", -0.6);
	},

	// Show elements, when they are in viewport
	appear: function() {
		$('#features').find('.row').appear(function() {
			var $feature = $(this).find('.feature-item');

			if(ie!== false && ie <= 9) $feature.css('opacity', 1);

			$feature.each(function(i) {
				var $this = $(this);

				setTimeout(function() {
					$this.addClass('animated fadeIn');
				}, i*200);
			});
		});

		$('#facts').find('.row').appear(function() {
			var $fact = $(this).find('.fact-item');

			if(ie!== false && ie <= 9) $fact.css('opacity', 1);

			$fact.each(function(i) {
				var $this = $(this),
					$counter = $this.find('.counter');

				setTimeout(function() {
					$this.addClass('animated fadeInDown');
					$counter.countTo({
						refreshInterval: 50,
						speed: 2000,
					});
				}, i*400);
			});
		});

		$('#portfolio').find('.row').appear(function() {
			var $article = $(this).find('article');

			if(ie!== false && ie <= 9) $article.css('opacity', 1);

			$(this).find('article').each(function(i) {
				var $this = $(this);

				setTimeout(function() {
					$this.addClass('animated fadeIn');
				}, i*200);
			});
		});

		$('#portfolio').find('.screenshots').appear(function() {
			var $this = $(this);

			if(ie!== false && ie <= 9) $this.css('opacity', 1);

			$this.addClass('animated fadeInDown');
		});

		$('#subscribe').find('.form-group').appear(function() {
			var $this = $(this),
				$formControl = $this.find('.form-control'),
				$btn = $this.find('.btn');

			if(ie!== false && ie <= 9) {
				$formControl.css('opacity', 1);
				$btn.css('opacity', 1);
			}

			$formControl.addClass('animated fadeInLeft');
			$btn.addClass('animated fadeInRight');
		});

		$('#prices').find('.row').appear(function() {
			var $this = $(this),
				$price = $this.find('.price-block');

			if(ie!== false && ie <= 9) $price.css('opacity', 1);

			$price.eq(1).addClass('animated fadeInDown');

			setTimeout(function() {
				$price.eq(0).addClass('animated fadeInLeft');
				$price.eq(2).addClass('animated fadeInRight');
			}, 400);
		});

		$('#video').find('.video-container').appear(function() {
			var $this = $(this);

			if(ie!== false && ie <= 9) $this.css('opacity', 1);

			$this.addClass('animated fadeInDown');
		});

		$('#c-form').appear(function() {
			var $this = $(this);

			if(ie!== false && ie <= 9) $this.css('opacity', 1);

			$this.addClass('animated fadeInDown');
		});

		$('#map').find('.contact-block').appear(function() {
			var $this = $(this);

			if(ie!== false && ie <= 9) $this.css('opacity', 1);

			$this.addClass('animated flipInY');
		});
	},

	// Scroll to anchor
	scrollTo: function(anchor) {
		$.scrollTo(anchor, p.scrollSpeed);
	},

	// Scroll to anchor, when link using .scrollTo class
	scrollToGlobal: function() {
		$('.scrollTo').on('click', function() {
			all.scrollTo($(this).attr('href'));

			return false;
		});
	},

	// One Page Navigation
	onePageNav: function() {
		$('#header').find('.nav').onePageNav({
			currentClass: 'active',
			scrollSpeed: p.scrollSpeed,
			scrollOffset: p.scrollOffset
		});
	},

	// Add background to top navigation on scroll
	navbarSelect: function() {
		var $navbar = $('#header');

		if($(window).scrollTop() > p.navbarScrollTop) {
			$navbar.addClass('selected');
		} else {
			$navbar.removeClass('selected');
		}
	},

	// Equate heights of similar blocks
	iheightInit: {
		features: function() {
			var $feature = $('#features').find('.feature-item');

			$feature.height('auto');

			if(viewportWidth() >= p.screen.sm) {
				$feature.iheight();
			}
		},
		prices: function() {
			var $inf = $('#prices').find('.inf');

			$inf.height('auto');

			if(viewportWidth() >= p.screen.md) {
				$inf.iheight();
			}
		}
	},

	portfolio: {
		// Isotope Filtering
		isotope: function() {
			var $container = $('#isotope');
			$container.isotope({
				itemSelector: '.portfolio-item',
				layoutMode: 'fitRows'
			});
			$('#portfolio-filter').find('a').on('click', function() {
				var selector = $(this).attr('data-filter-by');
				$('#portfolio-filter a').removeClass('active');
				$(this).addClass('active');
				$container.isotope({ filter: selector });

				return false;
			});
		},
		// Images Gallery
		fancybox: function() {
			var $body = $('body');
			$('.fancybox').fancybox({
				padding: 0,
				helpers: {
					overlay: {
						locked: false
					}
				},
				beforeLoad: function() {
					$body.css('overflow', 'hidden');
				},
				afterClose: function() {
					$body.css('overflow', '');
				}
			});
		}
	},

	// AJAX requests
	ajaxForms: {

		// Subscribe
		subscribe: function() {
			$('#subscribe-form').on('submit', function(e) {
				e.preventDefault();

				var $this = $(this),
					$submit = $this.find('input[type="submit"]'),
					$email = $this.find('.email'),
					action = $this.attr('action'),
					email_val = $email.val();

				$.ajax({
					data: 'email='+email_val,
					dataType: 'JSON',
					type: 'GET',
					url: action,
					beforeSend: function() {
						$submit.attr('disabled', 'disabled');
						loader.show();
					},
					success: function(response) {
						var $message_box = $('#message-box');


						if($message_box.hasClass('visible')) {
							$message_box.removeClass('visible');
							$message_box.on(transitionEnd, function() {
								$message_box.unbind(transitionEnd);

								all.ajaxForms.subscribeShow(response.text, response.type, $message_box);
							});
						} else {
							all.ajaxForms.subscribeShow(response.text, response.type, $message_box);
						}

						if(response.type == 'success') {
							$email.val('');
						}
					},
					complete: function() {
						$submit.removeAttr('disabled');
						loader.hide();
					}
				});
			});
		},
		subscribeShow: function(text, type, $box) {
			$box.text(text);
			$box.removeClass('text-primary');

			if(type == 'error') { $box.addClass('text-primary'); }

			$box.addClass('visible');
		},

		// Contacts
		contact: function() {
			var $alert_box = $('#c-alert-box');

			$('#c-form').on('submit', function(e) {
				e.preventDefault();

				var $this = $(this);

				$.ajax({
					data: $this.serialize(),
					dataType: 'JSON',
					type: 'POST',
					url: $this.attr('action'),
					beforeSend: function() {
						$alert_box.html('');
						loader.show();
					},
					success: function(response) {
						if(response.errors) {
							$.each(response.errors, function(index, value) {
								setTimeout(function() {
									$alert_box.append('<div class="alert alert-danger animated fadeIn">'+value+'</div>');
								}, index*500);
							});
						} else if(response.success) {
							$alert_box.append('<div class="alert alert-success animated fadeIn">'+response.success+'</div>');
						}
					},
					complete: function() {
						loader.hide();
					}
				});
			});
		}
	},

	// Slider
	slider: function() {
		$('#slides').superslides({
			animation: 'fade',
			animation_speed: 1000,
			play: 5000
		});
	},

	// Carousel
	carousel: function() {
		$(".owl-carousel").owlCarousel({
			items: 1,
			dots: true,
			margin: 20,
			responsive: {
				480: {
					items: 2
				},
				768: {
					items: 3
				},
				1200: {
					items: 4
				}
			}
		});
	}
};


// Initializations
var init = {
	ready: function() {
		all.preloader.init();
		all.scrollToGlobal();
		all.onePageNav();

		all.portfolio.isotope();
		all.portfolio.fancybox();

		all.appear();

		all.iheightInit.features();
		all.iheightInit.prices();

		all.ajaxForms.subscribe();
		all.ajaxForms.contact();

		all.slider();
		all.carousel();
		all.parallax();
	},
	scroll: function() {
		all.navbarSelect();
	},
	resize: function() {
		all.iheightInit.features();
		all.iheightInit.prices();
	}
};
$(document).ready(init.ready);
$(window).scroll(init.scroll);
$(window).resize(init.resize);


// This function return viewport width
function viewportWidth() {
	var $body = $('body'),
		viewPortWidth;

	if($body.css('overflow') != 'hidden') {
		$body.css('overflow', 'hidden');
		viewPortWidth = $body.width();
		$body.css('overflow', '');
	} else {
		viewPortWidth = $body.width();
	}

	return viewPortWidth;
}


// Detecting IE
function ie_version() {
	var ua = window.navigator.userAgent,
		msie = ua.indexOf("MSIE ");

	if(msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
		return parseInt(ua.substring(msie + 5, ua.indexOf(".", msie)));
	}

	return false;
}
