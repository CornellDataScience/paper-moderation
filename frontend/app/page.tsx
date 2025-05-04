import Image from "next/image";
import FileDropzone from "./components/FileDropzone";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 pt-4">
      {/* CDS Logo and Text */}
      <div className="flex flex-col items-center mb-6 mt-4">
        <div className="flex items-center justify-center mb-1">
          <Image
            src="/cds_logo.png"
            alt="Cornell Data Science Logo"
            width={80}
            height={80}
            className="mr-3"
          />
          <h1 className="text-4xl font-bold text-[#2D2A5E]">CDS</h1>
        </div>
        <p className="text-base text-[#2D2A5E]">Cornell Data Science</p>
      </div>

      <div className="max-w-5xl w-full mt-4 mb-8">
        <h1 className="text-6xl font-bold text-center text-[#1E1E2E] leading-tight">
          Is Your Paper Ready
          <br /> for arXiv?
        </h1>
      </div>

      {/* File Upload Dropzone */}
      <div className="flex justify-center w-full mb-16">
        <FileDropzone />
      </div>

      {/* How to Use and About Project Section */}
      <div className="w-full max-w-2xl flex flex-col md:flex-row justify-center items-start md:gap-12">
        {/* How to Use */}
        <div className="w-full md:w-1/2">
          <h2 className="text-3xl font-bold text-[#1E1E2E] mb-6">How to Use</h2>
          <div className="space-y-8">
            {/* Step 1 */}
            <div className="flex items-start">
              <div className="flex-shrink-0 w-10 h-10 bg-[#4F46E5] rounded-full flex items-center justify-center text-white text-lg font-bold mr-3">
                1
              </div>
              <div>
                <p className="text-lg font-medium text-gray-800">
                  Upload the PDF
                  <br />
                  of your paper.
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex items-start">
              <div className="flex-shrink-0 w-10 h-10 bg-[#4F46E5] rounded-full flex items-center justify-center text-white text-lg font-bold mr-3">
                2
              </div>
              <div>
                <p className="text-lg font-medium text-gray-800">
                  Click "Submit"
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex items-start">
              <div className="flex-shrink-0 w-10 h-10 bg-[#4F46E5] rounded-full flex items-center justify-center text-white text-lg font-bold mr-3">
                3
              </div>
              <div>
                <p className="text-lg font-medium text-gray-800">
                  View the result to see
                  <br />
                  if your paper is ready
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* About the Project */}
        <div className="w-full md:w-1/2 mt-8 md:mt-0">
          <h2 className="text-3xl font-bold text-[#1E1E2E] mb-6">
            About the Project
          </h2>
          <div className="flex items-start">
            <div className="flex-shrink-0 w-10 h-10 bg-[#4F46E5] rounded-full flex items-center justify-center text-white mr-3">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9.66347 17H14.3364"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M12 14V10"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M12 3V4"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M12 20V21"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M3 12H4"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M20 12H21"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M18.3639 5.63604L17.6568 6.34315"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M6.34314 17.6569L5.63603 18.364"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M18.3639 18.364L17.6568 17.6569"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M6.34314 6.34315L5.63603 5.63604"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M6.99999 12C6.99999 9.23858 9.23857 7 12 7C14.7614 7 17 9.23858 17 12C17 13.1954 16.5209 14.2909 15.7458 15.1069C15.1571 15.7155 14.758 16.5086 14.6066 17.3562L14.5206 17.837C14.4428 18.2487 14.0851 18.5539 13.6654 18.5539H10.3345C9.91483 18.5539 9.55711 18.2487 9.47931 17.837L9.39329 17.3562C9.24192 16.5086 8.84281 15.7155 8.25409 15.1069C7.47904 14.2909 6.99999 13.1954 6.99999 12Z"
                  stroke="currentColor"
                  strokeWidth="1.5"
                />
              </svg>
            </div>
            <div>
              <p className="text-lg text-gray-800 leading-relaxed">
                This website allows users to check whether a research paper is
                ready for arXiv using a machine learning-based classifier. Given
                an uploaded PDF, it predicts whether the paper is ready for
                submission based on formatting, structure, and content quality.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
