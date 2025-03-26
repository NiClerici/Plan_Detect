document.addEventListener('DOMContentLoaded', () => {
    const BACKEND_URL = '/Users/nicoclerici/Documents/Bewerbung/DBew/Plan_Detection/CNN/Frontend Vercel/Inferenz.py';
    console.log("🚀 Frontend geladen. Verwende Backend:", BACKEND_URL);

    // Überprüfung, ob das Upload-Formular existiert
    const uploadForm = document.getElementById('uploadForm');
    if (!uploadForm) {
        console.error("❌ Fehler: Das Upload-Formular (#uploadForm) wurde nicht gefunden!");
        return;
    }

    uploadForm.addEventListener('submit', event => {
        event.preventDefault(); // Verhindert die Standardaktion des Formulars

        const fileInput = document.getElementById('fileInput');
        if (!fileInput || fileInput.files.length === 0) {
            console.error("❌ Fehler: Keine Datei ausgewählt!");
            document.getElementById('result').innerHTML = `<p class="text-danger">Fehler: Keine Datei ausgewählt!</p>`;
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        console.log("📤 Hochladen gestartet...");

        // Sende die Datei an das Backend
        fetch(`${BACKEND_URL}/upload`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(error => {
                    throw new Error(error);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.processed) {
                console.log("✅ Verarbeitung erfolgreich:", data);

                // Verarbeiteten Bildlink anzeigen
                const resultContainer = document.getElementById('result');
                if (!resultContainer) {
                    console.error("❌ Fehler: Das Ergebnis-Element (#result) wurde nicht gefunden!");
                    return;
                }

                const processedImage = `${BACKEND_URL}${data.processed}`;
                resultContainer.innerHTML = `
                    <p class="text-success">✅ Bild erfolgreich hochgeladen!</p>
                    <a href="${processedImage}" target="_blank" class="btn btn-primary mt-3">Verarbeitetes Bild anzeigen</a>
                `;
            } else {
                console.warn("⚠️ Keine Verarbeitungsergebnisse vom Backend erhalten.");
                document.getElementById('result').innerHTML = `<p class="text-danger">Fehler: Keine Ergebnisse erhalten!</p>`;
            }
        })
        .catch(error => {
            console.error("❌ Fehler beim Hochladen:", error);
            document.getElementById('result').innerHTML = `<p class="text-danger">Fehler: ${error.message}</p>`;
        });
    });

    // Funktion zum Öffnen eines Bildmodals (Optional für spätere Galerieerweiterungen)
    function openModal(imageSrc) {
        const modalImage = document.getElementById('modalImage');
        if (!modalImage) {
            console.error("❌ Fehler: Kein Modal-Element für das Bild gefunden!");
            return;
        }
        modalImage.src = imageSrc;
        const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
        imageModal.show();
    }
});
