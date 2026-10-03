// ============================================================
// API
// ============================================================


// ============================================================
// TEST KONEKSI
// ============================================================

async function testConnection() {

    try {

        const response =
            await fetch("/api/test");


        if (!response.ok) {

            throw new Error(
                "Server tidak merespons"
            );

        }


        const data =
            await response.json();


        document.getElementById(
            "raspberry-status"
        ).textContent = "Terhubung";


        document.getElementById(
            "connection-text"
        ).textContent = "Terhubung";


        const statusDot =
            document.getElementById(
                "status-dot"
            );


        statusDot.classList.remove(
            "error"
        );

        statusDot.classList.add(
            "connected"
        );


        console.log(data.message);


    } catch (error) {

        console.error(
            "Koneksi gagal:",
            error
        );


        document.getElementById(
            "raspberry-status"
        ).textContent =
            "Tidak terhubung";


        document.getElementById(
            "connection-text"
        ).textContent =
            "Tidak terhubung";


        const statusDot =
            document.getElementById(
                "status-dot"
            );


        statusDot.classList.remove(
            "connected"
        );

        statusDot.classList.add(
            "error"
        );

    }

}


// ============================================================
// BACA DATA
// ============================================================

async function loadData() {

    try {

        const response =
            await fetch("/api/data");


        const data =
            await response.json();


        tampilkanData(data);

        tampilkanRekap(data);


    } catch (error) {

        console.error(
            "Gagal membaca data:",
            error
        );

    }

}


// ============================================================
// START
// ============================================================

testConnection();

loadData();