(function($){"use strict";$(window).on('load',function(){$('body').addClass('loaded');});$(function(){var header=$("#header"),yOffset=0,triggerPoint=100;$(window).on('scroll',function(){yOffset=$(window).scrollTop();if(yOffset>=triggerPoint){header.removeClass("animated fadeIn");header.addClass("navbar-fixed-top animated fadeInDown");}else{header.removeClass("navbar-fixed-top animated fadeInDown");header.addClass("animated fadeIn");}});});var owlSlider=$('#main-slider');owlSlider.owlCarousel({items:1,loop:true,smartSpeed:500,autoplayTimeout:3500,mouseDrag:false,touchDrag:false,autoplay:true,nav:true,navText:['<i class="arrow_carrot-left"></i>','<i class="arrow_carrot-right"></i>']});owlSlider.on('translate.owl.carousel',function(){$('.slider_content h1').removeClass('fadeInUp animated').hide();$('.slider_content p').removeClass('fadeInUp animated').hide();$('.slider_content .btn_group').removeClass('fadeInDown animated').hide();});owlSlider.on('translated.owl.carousel',function(){$('.owl-item.active .slider_content h1').addClass('fadeInUp animated').show();$('.owl-item.active .slider_content p').addClass('fadeInUp animated').show();$('.owl-item.active .slider_content .btn_group').addClass('fadeInDown animated').show();});$('#works-carousel').owlCarousel({loop:true,margin:20,autoplay:true,smartSpeed:500,dots:false,nav:true,navText:['<i class="fa fa-chevron-left"></i>','<i class="fa fa-chevron-right"></i>'],responsiveClass:true,responsive:{0:{items:1},600:{items:2,margin:10},1000:{items:3}}});$('.portfolio_items').imagesLoaded(function(){$('.portfolio_filter li').on('click',function(){$(".portfolio_filter li").removeClass("active");$(this).addClass("active");var selector=$(this).attr('data-filter');$(".portfolio_items").isotope({filter:selector,animationOptions:{duration:750,easing:'linear',queue:false,}});return false;});$(".portfolio_items").isotope({itemSelector:'.single_item',layoutMode:'fitRows',});});var testiSelector=$('#testimonial_carousel');testiSelector.owlCarousel({loop:true,autoplay:true,smartSpeed:500,items:1,nav:false});var sponsorCarousel=$('#sponsor_carousel');sponsorCarousel.imagesLoaded(function(){sponsorCarousel.owlCarousel({loop:true,margin:10,autoplay:true,smartSpeed:1000,nav:false,dots:false,responsive:true,responsive:{0:{items:3},480:{items:3,},768:{items:6,}}});});var counterSelector=$('.counter');counterSelector.counterUp({delay:10,time:2000});smoothScroll.init({offset:60});var vbSelector=$('.img_popup');vbSelector.venobox({numeratio:true,infinigall:true});$(window).on('scroll',function(){if($(this).scrollTop()>100){$('#scroll-to-top').fadeIn();}else{$('#scroll-to-top').fadeOut();}});google.maps.event.addDomListener(window,'load',init);function init(){var mapOptions={zoom:11,center:new google.maps.LatLng(40.6700,-73.9400),scrollwheel:false,navigationControl:false,mapTypeControl:false,scaleControl:false,draggable:false,styles:[{"featureType":"administrative","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"administrative.province","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","elementType":"all","stylers":[{"saturation":-100},{"lightness":"50"},{"visibility":"simplified"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"lightness":"30"}]},{"featureType":"road.local","elementType":"all","stylers":[{"lightness":"40"}]},{"featureType":"transit","elementType":"all","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]},{"featureType":"water","elementType":"labels","stylers":[{"lightness":-25},{"saturation":-100}]}]};var mapElement=document.getElementById('google_map');var map=new google.maps.Map(mapElement,mapOptions);var marker=new google.maps.Marker({position:new google.maps.LatLng(40.6700,-73.9400),map:map,title:'Location!'});}
if($('.subscribe_form').length>0){$('.subscribe_form').ajaxChimp({language:'es',callback:mailchimpCallback,url:"//alexatheme.us14.list-manage.com/subscribe/post?u=48e55a88ece7641124b31a029&amp;id=361ec5b369"});}
function mailchimpCallback(resp){if(resp.result==='success'){$('#subscribe-result').addClass('subs-result');$('.subscription-success').text(resp.msg).fadeIn();$('.subscription-error').fadeOut();}else if(resp.result==='error'){$('#subscribe-result').addClass('subs-result');$('.subscription-error').text(resp.msg).fadeIn();}}
$.ajaxChimp.translations.es={'submit':'Submitting...',0:'We have sent you a confirmation email',1:'Please enter your email',2:'An email address must contain a single @',3:'The domain portion of the email address is invalid (the portion after the @: )',4:'The username portion of the email address is invalid (the portion before the @: )',5:'This email address looks fake or invalid. Please enter a real email address'};})(jQuery);