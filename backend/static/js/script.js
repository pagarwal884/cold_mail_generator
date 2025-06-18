const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

// Handle Drag Over
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("border-[#658560]", "bg-green-50");
});

// Handle Drag Leave
dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("border-[#658560]", "bg-green-50");
});

// Handle Drop
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("border-[#658560]", "bg-green-50");
  const droppedFiles = Array.from(e.dataTransfer.files);
  handleFiles(droppedFiles);
});

// Handle File Input Change
fileInput.addEventListener("change", () => {
  const selectedFiles = Array.from(fileInput.files);
  handleFiles(selectedFiles);
});

// Upload and Process Files
async function handleFiles(files) {
  const validFiles = files.filter(
    (file) =>
      file.name.toLowerCase().endsWith(".pdf") ||
      file.name.toLowerCase().endsWith(".docx")
  );

  if (validFiles.length === 0) {
    alert("Please upload only PDF or DOCX files.");
    return;
  }

  // Create FormData and append files
  const formData = new FormData();
  validFiles.forEach((file) => {
    formData.append("files", file);
  });

  try {
    // Show loading state
    dropZone.innerHTML =
      '<i class="fa-solid fa-spinner fa-spin text-xl"></i> Processing files...';

    // Send to server
    const response = await fetch("/upload-resume/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"), // Ensure you have CSRF token
      },
    });

    const data = await response.json();

    if (response.ok) {
      // Update UI with processed files
      let successCount = data.files.filter(
        (f) => f.status === "processed"
      ).length;
      dropZone.innerHTML = `
                <span class="text-3xl text-green-500 mb-2">
                    <i class="fa-solid fa-check-circle"></i>
                </span>
                <p class="text-sm text-gray-600 font-medium">
                    Successfully processed ${successCount} file(s)
                </p>
            `;

      // You can now use the processed files for the cold email generation
      console.log("Processed files:", data.files);
    } else {
      throw new Error(data.error || "Failed to process files");
    }
  } catch (error) {
    dropZone.innerHTML = `
            <span class="text-3xl text-red-500 mb-2">
                <i class="fa-solid fa-exclamation-circle"></i>
            </span>
            <p class="text-sm text-red-600 font-medium">
                ${error.message}
            </p>
            ${dropZone.innerHTML}
        `;
  }
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Tone Selection Logic
const colorBlocks = document.querySelectorAll(".color-block");
const toneInput = document.getElementById("toneInput");
const selectedTexts = new Set();

colorBlocks.forEach((block) => {
  block.addEventListener("click", (e) => {
    const text = block.dataset.text;

    if (block.classList.contains("selected")) {
      selectedTexts.delete(text);
      block.classList.remove("selected");
    } else {
      selectedTexts.add(text);
      block.classList.add("selected");
    }

    toneInput.value = Array.from(selectedTexts).join(", ");
  });
});

// Reference to the textarea
const mailText = document.getElementById("generatedMail");

// COPY BUTTON
document.getElementById("copyBtn").addEventListener("click", () => {
  navigator.clipboard
    .writeText(mailText.value)
    .then(() => {
      alert("Email copied to clipboard!");
    })
    .catch((err) => {
      alert("Failed to copy: " + err);
    });
});

// DOWNLOAD BUTTON
document.getElementById("downloadBtn").addEventListener("click", () => {
  const blob = new Blob([mailText.value], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "cold-email.txt";
  a.click();
  URL.revokeObjectURL(url);
});

// SEND BUTTON - Open Gmail with body autofilled (auto-paste simulation)
document.getElementById("sendBtn").addEventListener("click", () => {
  const emailContent = document.getElementById("generatedMail").value.trim();

  if (!emailContent) {
    alert("Generated email is empty.");
    return;
  }

  const subject = encodeURIComponent("Job Opportunity Inquiry");
  const body = encodeURIComponent(emailContent);

  // Gmail Compose URL
  const gmailURL = `https://mail.google.com/mail/?view=cm&fs=1&to=&su=${subject}&body=${body}`;

  // Open in new tab (simulate "paste" by pre-filling)
  window.open(gmailURL, "_blank");
});
