document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const uploadStatus = document.getElementById("uploadStatus");

    if (!uploadForm) return;

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const fileInput = uploadForm.querySelector('input[type="file"]');
        const file = fileInput.files[0];

        if (!file) {
            uploadStatus.className = "status-box empty-state";
            uploadStatus.textContent = "Please choose a PDF file first.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        uploadStatus.className = "status-box";
        uploadStatus.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;

        try {
            const response = await fetch("/upload/", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                uploadStatus.className = "status-box empty-state";
                if (response.status === 401) {
                    uploadStatus.innerHTML = `${data.error || "Please log in first."} <a href="/auth/login" style="color: #f59e0b; text-decoration: underline; margin-left: 6px;">Login here</a>`;
                } else {
                    uploadStatus.textContent = data.error || "Upload failed.";
                }
                return;
            }

            uploadStatus.className = "status-box";
            uploadStatus.innerHTML = `
                <strong>${data.message}</strong><br>
                File: ${data.filename}<br>
                Extracted text length: ${data.text_length}
            `;

            fileInput.value = "";

            const currentFileName = document.getElementById("currentFileName");
            if (currentFileName) {
                currentFileName.textContent = data.filename;
            }

        } catch (error) {
            uploadStatus.className = "status-box empty-state";
            uploadStatus.textContent = "Unable to upload file right now.";
        }
    });
})
/* Drop zone highlight on drag */
const dropZone = document.getElementById("dropZone");
if (dropZone) {
    ["dragenter", "dragover"].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });
    });
    ["dragleave", "drop"].forEach(evt => {
        dropZone.addEventListener(evt, () => {
            dropZone.classList.remove("drag-over");
        });
    });
    /* Show filename on file pick */
    dropZone.querySelector("input").addEventListener("change", function () {
        const label = dropZone.querySelector(".drop-zone-text");
        if (this.files[0]) {
            label.textContent = this.files[0].name;
            dropZone.classList.add("has-file");
        }
    });
}
