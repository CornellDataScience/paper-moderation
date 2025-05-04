"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

export default function FileDropzone() {
  const [file, setFile] = useState<File | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isApproved, setIsApproved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "text/plain": [".txt"],
    },
    maxFiles: 1,
  });

  const handleSubmit = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/evaluate-paper", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setIsApproved(data.approved);
      setShowResult(true);
    } catch (err) {
      console.error("Error submitting paper:", err);
      setError(
        "Failed to evaluate the paper. Please try again or contact support."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setShowResult(false);
    setIsApproved(false);
    setError(null);
  };

  // Show result screen
  if (showResult) {
    return (
      <div className="w-full max-w-2xl flex flex-col items-center">
        <div className="text-center mb-8">
          {isApproved ? (
            <>
              <div className="w-24 h-24 mx-auto mb-6 text-green-500">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-full h-full"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="2"
                  />
                  <path
                    d="M8 12L11 15L16 9"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Yes</h2>
              <p className="text-xl text-gray-700">
                This paper is ready for arXiv
              </p>
            </>
          ) : (
            <>
              <div className="w-24 h-24 mx-auto mb-6 text-red-500">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-full h-full"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="2"
                  />
                  <path
                    d="M15 9L9 15"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M9 9L15 15"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-2">No</h2>
              <p className="text-xl text-gray-700">
                This paper is not ready for arXiv
              </p>
            </>
          )}
        </div>
        <button
          onClick={handleReset}
          className="bg-[#4F46E5] text-white py-2.5 px-6 rounded-lg text-lg font-medium hover:bg-indigo-700 transition-colors"
        >
          Submit Another Paper
        </button>
      </div>
    );
  }

  // Show dropzone
  return (
    <div className="w-full max-w-2xl">
      <div
        {...getRootProps()}
        className="border-2 border-dashed border-[#A5A1FF] rounded-lg p-10 text-center cursor-pointer hover:bg-indigo-50 transition-colors mb-4"
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center">
          <div className="w-16 h-16 mb-4 text-[#4F46E5]">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="w-full h-full"
            >
              <path
                d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12 16L12 10"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M9 13L12 16L15 13"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <p className="text-lg mb-1 text-gray-800 font-medium">
            {isDragActive
              ? "Drop the file here..."
              : file
              ? `File selected: ${file.name}`
              : "Drag and drop a PDF or TXT file here to upload"}
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={!file || isLoading}
        className="bg-[#4F46E5] text-white py-2.5 px-6 rounded-lg text-lg font-medium w-full hover:bg-indigo-700 transition-colors disabled:bg-indigo-300 disabled:cursor-not-allowed"
      >
        {isLoading ? "Evaluating..." : "Submit"}
      </button>
    </div>
  );
}
