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
                    if (/\|/.exec(ext))
                        alert('Błędne rozszerzenie! Powinno być jedno z: ' + ext.replace(/\|/g, ', '));
                    else
                        alert('Błędne rozszerzenie! Powinno być: ' + ext);
                    ok = false;
                }
                if (name.length > 65) {
                    alert('Za długa nazwa pliku! Maksymalna długość: 65 znaków (jest: ' + name.length + ')');
                    ok = false;
                }
            }
            var size = this.files[0].size;
            if (size > 20 * 1024 * 1024) {
                alert('Rozmiar pliku nie może przekraczać 20 MB!');
                ok = false;
            }
            if (!ok) {
                this.form.reset();
            }
        }
    });
});
