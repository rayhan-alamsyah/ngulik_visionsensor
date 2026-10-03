// ============================================================
// TABEL DATA
// ============================================================


// ============================================================
// TAMPILKAN DATA
// ============================================================

function tampilkanData(data) {

    const table =
        document.getElementById(
            "data-table"
        );


    if (!data || data.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="12">
                    Belum ada data
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML = "";


    data.forEach(function (item) {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                ${item.no ?? ""}
            </td>

            <td>
                ${item.tanggal ?? ""}
            </td>

            <td>
                ${item.waktu ?? ""}
            </td>

            <td>
                ${item.foto ?? "-"}
            </td>

            <td>
                ${item.tinggi_kiri ?? ""}
            </td>

            <td>
                ${item.tinggi_kanan ?? ""}
            </td>

            <td>
                ${item.upper_kiri ?? ""}
            </td>

            <td>
                ${item.lower_kiri ?? ""}
            </td>

            <td>
                ${item.upper_kanan ?? ""}
            </td>

            <td>
                ${item.lower_kanan ?? ""}
            </td>

            <td>
                ${item.hasil ?? ""}
            </td>

            <td>

                <button
                    class="edit-button"
                    onclick='bukaEdit(${JSON.stringify(item)})'
                >
                    EDIT
                </button>

                <button
                    class="delete-button"
                    onclick='hapusData("${item.id}")'
                >
                    HAPUS
                </button>

            </td>

        `;


        table.appendChild(row);

    });

}


// ============================================================
// REKAP
// ============================================================

function tampilkanRekap(data) {

    const table =
        document.getElementById(
            "rekap-table"
        );


    if (!data || data.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    Belum ada data
                </td>
            </tr>
        `;

        return;
    }


    // --------------------------------------------------------
    // Kelompokkan berdasarkan tanggal
    // --------------------------------------------------------

    const rekap = {};


    data.forEach(function (item) {

        const tanggal =
            item.tanggal || "-";


        if (!rekap[tanggal]) {

            rekap[tanggal] = {

                good: 0,

                upper_kiri: 0,

                upper_kanan: 0,

                lower_kiri: 0,

                lower_kanan: 0

            };

        }


        if (item.hasil === "GOOD") {

            rekap[tanggal].good++;

        }


        if (item.upper_kiri === "NG") {

            rekap[tanggal].upper_kiri++;

        }


        if (item.upper_kanan === "NG") {

            rekap[tanggal].upper_kanan++;

        }


        if (item.lower_kiri === "NG") {

            rekap[tanggal].lower_kiri++;

        }


        if (item.lower_kanan === "NG") {

            rekap[tanggal].lower_kanan++;

        }

    });


    table.innerHTML = "";


    Object.keys(rekap).forEach(
        function (tanggal) {

            const item =
                rekap[tanggal];


            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${tanggal}
                </td>

                <td>
                    ${item.good}
                </td>

                <td>
                    ${item.upper_kiri}
                </td>

                <td>
                    ${item.upper_kanan}
                </td>

                <td>
                    ${item.lower_kiri}
                </td>

                <td>
                    ${item.lower_kanan}
                </td>

            `;


            table.appendChild(row);

        }
    );

}


// ============================================================
// HAPUS DATA
// ============================================================

async function hapusData(id) {

    const yakin =
        confirm(
            "Yakin ingin menghapus data ini?"
        );


    if (!yakin) {

        return;

    }


    try {

        const response =
            await fetch(
                "/api/delete",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        id: id
                    })

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
            "Data berhasil dihapus."
        );


        // Refresh tabel

        loadData();


    } catch (error) {

        console.error(error);

        alert(
            "Gagal menghapus data."
        );

    }

}