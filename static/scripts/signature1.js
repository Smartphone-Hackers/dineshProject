/*var signaturePad = new SignaturePad(document.getElementById('signature-pad'), {
  backgroundColor: 'rgba(255, 255, 255, 0)',
  penColor: 'rgb(0, 0, 0)'
});*/

var signature = {
	canvas: null,
  clearButton: null,
	/*resizeCanvas: function resizeCanvas() {
		// When zoomed out to less than 100%, for some very strange reason,
		// some browsers report devicePixelRatio as less than 1
		// and only part of the canvas is cleared then.
		var ratio = Math.max(window.devicePixelRatio || 1, 1);
		this.canvas.width = canvas.offsetWidth * ratio;
		this.canvas.height = canvas.offsetHeight * ratio;
		this.canvas.getContext("2d").scale(ratio, ratio);
	},*/
	init: function init() {
		this.canvas = document.querySelector(".signature-pad");
    this.clearButton = document.getElementById('clear');
		signaturePad = new SignaturePad(this.canvas);
    this.clearButton.addEventListener('click', function (event) {
  signaturePad.clear();
});
	}
};

signature.init();
