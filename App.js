import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please upload a PDF first!");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    setData(result);
    setLoading(false);
  };

  return (
    <div style={{ fontFamily: "sans-serif", textAlign: "center", padding: "2rem" }}>
      <h1>Credit Card Statement Parser</h1>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        onClick={handleUpload}
        style={{
          marginLeft: "10px",
          padding: "8px 16px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Upload
      </button>

      {loading && <p>Extracting data...</p>}

      {data && (
        <div style={{ marginTop: "2rem", textAlign: "left", display: "inline-block" }}>
          <h2>Extracted Data:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
