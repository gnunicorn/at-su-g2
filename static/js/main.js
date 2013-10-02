

$(function() {
	$(".upgrade-selection").each(function(bounding_box){
		var $outer = $(this);
		var $holder = $("#" + $outer.data("upgrade-name"));
		var $boxes = $outer.find(".upgrade-box");
		function reset_active(){
			var val = $holder.val()
			$boxes.each(function(){
				var $this = $(this);
				if ($this.data("upgrade-value") === val) {
					$this.addClass("active");
				} else {
					$this.removeClass("active");
				}
			})
		}
		$boxes.click(function(){
			var set_val = $(this).data("upgrade-value");
			if ($holder.val() === set_val) {
				set_val = ""
			}
			$holder.val(set_val);
			reset_active();
		});
	});
});