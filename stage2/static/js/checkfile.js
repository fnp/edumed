$(function() {
    "use strict";
    $('input[type=file]').on('change', function () {
        if (window.FileReader && this.files && this.files[0]) {
            var ok = true;
            var name = this.files[0].name;
            if (this.getAttribute('data-ext')) {
                var ext = this.getAttribute('data-ext');
                var re = new RegExp('\\.(' + ext + ')$', 'i');
                if (!re.exec(name)) {
                    alert('Błędne rozszerzenie! Powinno być jedno z: ' + ext.replace(/\|/g, ', '));
                    ok = false;
                }
            }
            var size = this.files[0].size;
            if (size > 10 * 1024 * 1024) {
                alert('Rozmiar pliku nie może przekraczać 10 MB!');
                ok = false;
            }
            if (!ok) {
                this.form.reset();
            }
        }
    });
});
