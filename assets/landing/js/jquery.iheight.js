/*
 * Plugin: jQuery iHeight
 * Version 1.0.0
 * Author: Vladislav Bezenson
 * Author URL: http://meethemes.com/
 * GitHub URL: https://github.com/inferusvv/iHeight
 */

(function($) {

	$.fn.iheight = function($apply) {
		var $this = $(this),
			mh = 0;

		if(typeof something === "undefined") $apply = $this;

		$this.each(function () {
			var rec_h = parseInt($(this).height());
			if(rec_h > mh) {
				mh = rec_h;
			};
		});

		$apply.height(mh);
	};

})(jQuery);