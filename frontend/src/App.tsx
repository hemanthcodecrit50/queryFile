import { useState } from "react";
import { uploadFile, embedDocument, getReasoning } from "./api";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [filename, setFilename] = useState<string>("");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const result = await uploadFile(file);
    setFilename(file.name);
    setLoading(false);
    alert("File uploaded & parsed!");
  };

  const handleEmbed = async () => {
    if (!filename) return;
    setLoading(true);
    const result = await embedDocument(filename);
    setLoading(false);
    alert(result.status);
  };

  const handleQuery = async () => {
    if (!query || !filename) return;
    setLoading(true);
    const result = await getReasoning(query, filename);
    console.log(result); 
    setResponse(result);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-900 p-4 dark">
      <div className="w-full max-w-xl bg-black/90 p-8 rounded-2xl shadow-xl flex flex-col items-center space-y-6 border-2 border-[#00bfae] subtle-glow">
        <h1 className="text-3xl font-extrabold text-center text-[#00bfae] mb-2 tracking-tight drop-shadow-subtle">Document QA System</h1>
        <p className="text-center text-gray-300 mb-4">Upload a PDF, generate embeddings, and ask questions about your document.</p>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block w-full border border-[#00bfae] p-2 rounded-lg focus:ring-2 focus:ring-[#00bfae] focus:outline-none transition bg-gray-800 text-[#00bfae] placeholder-gray-500 shadow-subtle"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-[#00bfae] text-black p-2 rounded-lg font-semibold shadow-subtle hover:bg-[#009e8e] transition border border-[#00bfae]"
        >
          Upload & Parse
        </button>

        <button
          onClick={handleEmbed}
          className="w-full bg-[#7c2fff] text-white p-2 rounded-lg font-semibold shadow-subtle hover:bg-[#5a1fa1] transition border border-[#7c2fff]"
        >
          Generate Embeddings
        </button>

        <textarea
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-2 border border-[#00bfae] rounded-lg focus:ring-2 focus:ring-[#7c2fff] focus:outline-none transition min-h-[60px] resize-none bg-gray-800 text-[#00bfae] placeholder-gray-500 shadow-subtle"
        ></textarea>

        <button
          onClick={handleQuery}
          className="w-full bg-[#00ff85] text-black p-2 rounded-lg font-semibold shadow-subtle hover:bg-[#00e66c] transition border border-[#00ff85]"
        >
          Ask Question
        </button>

        {loading && <p className="text-center text-[#00bfae] animate-pulse">Loading...</p>}

        {response && (
          <div className="bg-gray-900/90 p-4 rounded-xl border border-[#7c2fff] mt-4 w-full space-y-2 shadow-subtle">
            {response.error ? (
              <p className="text-red-400">{response.error}</p>
            ) : (
              <>
                <p><span className="font-semibold text-[#00bfae]">Decision:</span> {response.decision}</p>
                {response.justification && (
                  <p><span className="font-semibold text-[#7c2fff]">Justification:</span> {response.justification}</p>
                )}
              </>
            )}
          </div>
        )}
      </div>
      <style>{`
        .subtle-glow {
          box-shadow: 0 0 8px #00bfae, 0 0 16px #7c2fff;
        }
        .shadow-subtle {
          box-shadow: 0 0 2px #00bfae, 0 0 4px #7c2fff;
        }
        .drop-shadow-subtle {
          text-shadow: 0 0 2px #00bfae, 0 0 4px #7c2fff;
        }
      `}</style>
    </div>
  );
}

export default App;
