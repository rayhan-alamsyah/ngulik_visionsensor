// ============================================================
// EDIT DATA
// ============================================================


// ============================================================
// BUKA POPUP EDIT
// ============================================================

function bukaEdit(item) {

    document.getElementById(
        "edit-id"
    ).value = item.id;


    document.getElementById(
        "edit-tanggal"
    ).value = item.tanggal || "";


    document.getElementById(
        "edit-waktu"
    ).value = item.waktu || "";


    document.getElementById(
        "edit-tinggi-kiri"
    ).value = item.tinggi_kiri || "";


    document.getElementById(
        "edit-tinggi-kanan"
    ).value = item.tinggi_kanan || "";


    document.getElementById(
        "edit-upper-kiri"
    ).value = item.upper_kiri || "";


    document.getElementById(
        "edit-lower-kiri"
    ).value = item.lower_kiri || "";


    document.getElementById(
        "edit-upper-kanan"
    ).value = item.upper_kanan || "";


    document.getElementById(
        "edit-lower-kanan"
    ).value = item.lower_kanan || "";


    document.getElementById(
        "edit-hasil"
    ).value = item.hasil || "";


    document.getElementById(
        "edit-popup"
    ).classList.remove(
        "hidden"
    );

}


// ============================================================
// TUTUP POPUP
// ============================================================

function tutupEdit() {

    document.getElementById(
        "edit-popup"
    ).classList.add(
        "hidden"
    );

}


// ============================================================
// SIMPAN EDIT
// ============================================================

async function simpanEdit() {

    const data = {

        id:
            document.getElementById(
                "edit-id"
            ).value,

        tanggal:
            document.getElementById(
                "edit-tanggal"
            ).value,

        waktu:
            document.getElementById(
                "edit-waktu"
            ).value,

        tinggi_kiri:
            document.getElementById(
                "edit-tinggi-kiri"
            ).value,

        tinggi_kanan:
            document.getElementById(
                "edit-tinggi-kanan"
            ).value,

        upper_kiri:
            document.getElementById(
                "edit-upper-kiri"
            ).value,

        lower_kiri:
            document.getElementById(
                "edit-lower-kiri"
            ).value,

        upper_kanan:
            document.getElementById(
                "edit-upper-kanan"
            ).value,

        lower_kanan:
            document.getElementById(
                "edit-lower-kanan"
            ).value,

        hasil:
            document.getElementById(
                "edit-hasil"
            ).value

    };


    try {

        const response =
            await fetch(
                "/api/edit",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json();


        if (result.status !== "ok") {

            alert(
                result.message
            );

            return;

        }


        alert(
            "Data berhasil diubah."
        );


        tutupEdit();


        loadData();


    } catch (error) {

        console.error(error);

        alert(
            "Gagal mengubah data."
        );

    }

}


// ============================================================
// EVENT BUTTON
// ============================================================

document.getElementById(
    "edit-save"
).addEventListener(
    "click",
    simpanEdit
);


document.getElementById(
    "edit-cancel"
).addEventListener(
    "click",
    tutupEdit
);