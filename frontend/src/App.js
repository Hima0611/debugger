import React, { useState, useEffect } from "react";

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [typingTimeout, setTypingTimeout] = useState(null);

  // Function to call backend for debugging
  const analyzeCode = async (inputCode) => {
    if (!inputCode.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/debug", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: inputCode }),
      });
      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setResult({ error: "⚠️ Backend not reachable or error in request" });
    }
    setLoading(false);
  };

  // Detect code as user types (auto analysis after short pause)
  const handleCodeChange = (e) => {
    const newCode = e.target.value;
    setCode(newCode);

    // Clear old timeout to prevent too many requests
    if (typingTimeout) clearTimeout(typingTimeout);

    // Wait 2 seconds after last keystroke before analyzing
    const timeout = setTimeout(() => {
      analyzeCode(newCode);
    }, 2000);
    setTypingTimeout(timeout);
  };

  const handleSubmit = async () => {
    analyzeCode(code);
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "30px", textAlign: "center" }}>
      <h1>🧠 IntelliDebug - AI Code Analyzer</h1>
      <textarea
        rows="10"
        cols="80"
        placeholder="Paste or write your Python code here..."
        value={code}
        onChange={handleCodeChange}
        style={{
          padding: "10px",
          fontSize: "14px",
          borderRadius: "10px",
          border: "1px solid gray",
          marginBottom: "20px",
          fontFamily: "monospace",
        }}
      />
      <br />
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          backgroundColor: "#007bff",
          color: "white",
          padding: "10px 20px",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>

      {loading && (
        <p style={{ color: "#888", marginTop: "10px" }}>🔍 Analyzing your code...</p>
      )}

      {result && (
        <div
          style={{
            marginTop: "30px",
            backgroundColor: "#f9f9f9",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "left",
            width: "80%",
            margin: "30px auto",
          }}
        >
          <h3>🧩 Result:</h3>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <>
              <p><b>Summary:</b> {result.summary}</p>
              <p><b>Suggestion:</b> {result.suggestion}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
