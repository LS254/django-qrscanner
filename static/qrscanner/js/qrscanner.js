document.addEventListener("DOMContentLoaded", function () {
    function onScanSuccess(decodedText, decodedResult) {
        console.log("✅ Decoded text:", decodedText);

        const csrfToken = document.getElementById("csrf_token").value;

        fetch(scanApiUrl, {  
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ qr_code: decodedText })
        })
        .then(response => response.text())
        .then(text => {
            try {
                return JSON.parse(text);
            } catch (error) {
                throw new Error("❌ Server returned non-JSON response: " + text);
            }
        })
        .then(data => {
            if (data.success) {
                document.getElementById("result").innerHTML =
                    `✅ Found: ${data.name} <br>
                     📊 Scanned Count: ${data.scanned_count}`;
            } else {
                document.getElementById("result").innerHTML =
                `📌 Scanned Code: ${decodedText}`;
            }
        })
        .catch(error => {
            console.error("❌ Fetch error. Displaying scanned text instead.");
            document.getElementById("result").innerHTML =
                `📌 Scanned Code: ${decodedText}`;
        });
    }

    function onScanError(errorMessage) {
        console.warn("⚠️ Scan error:", errorMessage);
    }

    // scanner UI elements
    let scannerConfig = {
        fps: 10,
        qrbox: 250,
        rememberLastUsedCamera: true,
        showTorchButtonIfSupported: true,
        showZoomSliderIfSupported: true 
    };

    let html5QrCodeScanner = new Html5QrcodeScanner(
        "reader",
        scannerConfig,
        false
    );

    // start html5-qrscanner
    html5QrCodeScanner.render(onScanSuccess, onScanError);
});