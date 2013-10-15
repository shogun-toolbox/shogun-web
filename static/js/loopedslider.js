/*
 * 	loopedSlider 0.5.4 - jQuery plugin
 *	written by Nathan Searles	
 *	http://nathansearles.com/loopedslider/
 *
 *	Copyright (c) 2009 Nathan Searles (http://nathansearles.com/)
 *	Dual licensed under the MIT (MIT-LICENSE.txt)
 *	and GPL (GPL-LICENSE.txt) licenses.
 *
 *	Built for jQuery library
 *	http://jquery.com
 *
 */

/*
 *	markup example for jQuery("#loopedSlider").loopedSlider();
 *
 *	<div id="loopedSlider">	
 *		<div class="container">
 *			<div class="slides">
 *				<div><img src="01.jpg" alt="" /></div>
 *				<div><img src="02.jpg" alt="" /></div>
 *				<div><img src="03.jpg" alt="" /></div>
 *				<div><img src="04.jpg" alt="" /></div>
 *			</div>
 *		</div>
 *		<a href="#" class="previous">previous</a>
 *		<a href="#" class="next">next</a>
 *		<ul class="pagination">
 *			<li><a href="#">1</a></li>
 *			<li><a href="#">2</a></li>
 *			<li><a href="#">3</a></li>
 *			<li><a href="#">4</a></li>
 *		</ul>	
 *	</div>
 *
*/

(function(jQuery) {
	jQuery.fn.loopedSlider = function(options) {
		
	var defaults = {			
		container: '.container',
		slides: '.slides',
		pagination: '.pagination',
		containerClick: false, // Click container for next slide
		autoStart: 5000, // Set to positive number for auto start and interval time
		restart: 0, // Set to positive number for restart and restart time
		slidespeed: 300, // Speed of slide animation
		fadespeed: 300, // Speed of fade animation
		autoHeight: false // Set to positive number for auto height and animation speed
	};
		
	this.each(function() {
		
		var obj = jQuery(this);
		var o = jQuery.extend(defaults, options);
		var pagination = jQuery(o.pagination+' li a',obj);
		var m = 0;
		var t = 1;
		var s = jQuery(o.slides,obj).children().size();
		var w = jQuery(o.slides,obj).children().outerWidth();
		var p = 0;
		var u = false;
		var n = 0;
		var interval=0;
		var restart=0;
		
		jQuery(o.slides,obj).css({width:(s*w)});
		
		jQuery(o.slides,obj).children().each(function(){
			jQuery(this).css({position:'absolute',left:p,display:'block'});
			p=p+w;
		});
		
		jQuery(pagination,obj).each(function(){
			n=n+1;
			jQuery(this).attr('rel',n);
			jQuery(pagination.eq(0),obj).parent().addClass('active');
		});
		
		jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({position:'absolute',left:-w});
		
		if (s>3) {
			jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({position:'absolute',left:-w});
		}
		
		if(o.autoHeight){autoHeight(t);}
		
		jQuery('.next',obj).click(function(){
			if(u===false) {
				animate('next',true);
				if(o.autoStart){
					if (o.restart) {autoStart();}
					else {clearInterval(sliderIntervalID);}
				}
			} return false;
		});
		
		jQuery('.previous',obj).click(function(){
			if(u===false) {	
				animate('prev',true);
				if(o.autoStart){
					if (o.restart) {autoStart();}
					else {clearInterval(sliderIntervalID);}
				}
			} return false;
		});
		
		if (o.containerClick) {
			jQuery(o.container ,obj).click(function(){
				if(u===false) {
					animate('next',true);
					if(o.autoStart){
						if (o.restart) {autoStart();}
						else {clearInterval(sliderIntervalID);}
					}
				} return false;
			});
		}
		
		jQuery(pagination,obj).click(function(){
			if (jQuery(this).parent().hasClass('active')) {return false;}
			else {
				t = jQuery(this).attr('rel');
				jQuery(pagination,obj).parent().siblings().removeClass('active');
				jQuery(this).parent().addClass('active');
				animate('fade',t);
				if(o.autoStart){
					if (o.restart) {autoStart();}
					else {clearInterval(sliderIntervalID);}
				}
			} return false;
		});
	
		if (o.autoStart) {
			sliderIntervalID = setInterval(function(){
				if(u===false) {animate('next',true);}
			}, o.autoStart);
			function autoStart() {
				if (o.restart) {
				clearInterval(sliderIntervalID);
				clearInterval(interval);
				clearTimeout(restart);
					restart = setTimeout(function() {
						interval = setInterval(	function(){
							animate('next',true);
						},o.autoStart);
					},o.restart);
				} else {
					sliderIntervalID = setInterval(function(){
						if(u===false) {animate('next',true);}
					},o.autoStart);
				}
			};
		}
		
		function current(t) {
			if(t===s+1){t=1;}
			if(t===0){t=s;}
			jQuery(pagination,obj).parent().siblings().removeClass('active');
			jQuery('[rel="' + (t) + '"]',obj).parent().addClass('active');
		};
		
		function autoHeight(t) {
			if(t===s+1){t=1;}
			if(t===0){t=s;}	
			var getHeight = jQuery(o.slides,obj).children(':eq('+(t-1)+')',obj).outerHeight();
			jQuery(o.container,obj).animate({height: getHeight},o.autoHeight);					
		};		
		
		function animate(dir,clicked){	
			u = true;	
			switch(dir){
				case 'next':
					t = t+1;
					m = (-(t*w-w));
					current(t);
					if(o.autoHeight){autoHeight(t);}
					if(s<3){
						if (t===3){jQuery(o.slides,obj).children(':eq(0)').css({left:(s*w)});}
						if (t===2){jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({position:'absolute',left:(w)});}
					}
					jQuery(o.slides,obj).animate({left: m}, o.slidespeed,function(){
						if (t===s+1) {
							t = 1;
							jQuery(o.slides,obj).css({left:0},function(){jQuery(o.slides,obj).animate({left:m})});							
							jQuery(o.slides,obj).children(':eq(0)').css({left: 0});
							jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({ position:'absolute',left:-w});				
						}
						if (t===s) jQuery(o.slides,obj).children(':eq(0)').css({left:(s*w)});
						if (t===s-1) jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({left:s*w-w});
						u = false;
					});					
					break; 
				case 'prev':
					t = t-1;
					m = (-(t*w-w));
					current(t);
					if(o.autoHeight){autoHeight(t);}
					if (s<3){
						if(t===0){jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({position:'absolute',left:(-w)});}
						if(t===1){jQuery(o.slides,obj).children(':eq(0)').css({position:'absolute',left:0});}
					}
					jQuery(o.slides,obj).animate({left: m}, o.slidespeed,function(){
						if (t===0) {
							t = s;
							jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({position:'absolute',left:(s*w-w)});
							jQuery(o.slides,obj).css({left: -(s*w-w)});
							jQuery(o.slides,obj).children(':eq(0)').css({left:(s*w)});
						}
						if (t===2 ) jQuery(o.slides,obj).children(':eq(0)').css({position:'absolute',left:0});
						if (t===1) jQuery(o.slides,obj).children(':eq('+ (s-1) +')').css({position:'absolute',left:-w});
						u = false;
					});
					break;
				case 'fade':
					t = [t]*1;
					m = (-(t*w-w));
					current(t);
					if(o.autoHeight){autoHeight(t);}
					jQuery(o.slides,obj).children().fadeOut(o.fadespeed, function(){
						jQuery(o.slides,obj).css({left: m});
						jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({left:s*w-w});
						jQuery(o.slides,obj).children(':eq(0)').css({left:0});
						if(t===s){jQuery(o.slides,obj).children(':eq(0)').css({left:(s*w)});}
						if(t===1){jQuery(o.slides,obj).children(':eq('+(s-1)+')').css({ position:'absolute',left:-w});}
						jQuery(o.slides,obj).children().fadeIn(o.fadespeed);
						u = false;
					});
					break; 
				default:
					break;
				}					
			};
		});
	};
})(jQuery);
