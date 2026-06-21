/**
 * Example Node.js script demonstrating how a mobile civic application
 * can submit a multi-modal incident to VerdaTerraAI.
 */

const API_KEY = process.env.API_KEY || "replace-with-local-demo-key";
const BASE_URL = process.env.VERDATERRA_API_URL || "http://localhost:8080";

async function submitIncident() {
  const payload = {
    location_id: "loc_bengaluru_ward_15",
    description: "Overflowing garbage bin on MG Road.",
    image_base64: "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
    sensor_payload: {
      voc_ppm: 450,
      h2s_ppm: 12,
    },
  };

  try {
    console.log("Submitting multi-modal incident...");
    const response = await fetch(`${BASE_URL}/api/v1/incidents/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    console.log("Response Status:", response.status);
    console.log("Response Body:", data);
  } catch (error) {
    console.error("Error submitting incident:", error);
  }
}

submitIncident();
