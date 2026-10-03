// ============================================================
// POWER
// ============================================================


// ============================================================
// SIMPAN
// ============================================================

document.getElementById(
    "save-button"
).addEventListener(
    "click",
    function () {

        alert(
            "Fitur SIMPAN akan dihubungkan ke hasil QC."
        );

    }
);


// ============================================================
// SHUTDOWN
// ============================================================

document.getElementById(
    "shutdown-button"
).addEventListener(
    "click",
    function () {

        const yakin =
            confirm(
                "Yakin ingin mematikan Raspberry Pi?"
            );


        if (!yakin) {

            return;

        }


        alert(
            "Fitur SHUTDOWN Raspberry Pi belum diaktifkan."
        );

    }
);