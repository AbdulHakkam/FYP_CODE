import JsonView from "@uiw/react-json-view";
import React, { ChangeEvent, useState } from "react";

function App() {
  const [selectedSchema, setSelectedSchema] = useState<File | null>(null);
  const [selectedReport, setSelectedReport] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<{
    report: any;
    schema: any;
  } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSchemaChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedSchema(event.target.files[0]);
    }
  };
  const handleReportChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedReport(event.target.files[0]);
    }
  };
  const exportData = (data: any, filename: string) => {
    const jsonString = `data:text/json;chatset=utf-8,${encodeURIComponent(
      JSON.stringify(data)
    )}`;

    const link = document.createElement("a");
    link.href = jsonString;
    link.download = filename;

    link.click();
  };

  const handleParse = () => {
    if (selectedReport) {
      setLoading(true);
      const formData = new FormData();
      if (selectedSchema) formData.append("schema", selectedSchema);
      formData.append("report", selectedReport);
      fetch("http://146.190.201.185:5000//api/parse", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          setParsedData(data);
          setLoading(false);
        });
    }
  };

  return (
    <div>
      <nav className="bg-black h-16 flex">
        <ul className="flex h-full">
          <li className="my-auto ml-10 text-white">
            INTELLIGENT PARSER - DEMO
          </li>
        </ul>
      </nav>
      {loading && (
        <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center">
          <p>Loading...</p>
        </div>
      )}
      <div className="mt-6 ml-10">
        <div className="flex flex-row">
          <div className="mr-[200px]">
            <div>
              <p className=" font-bold">Input Schema (Optional)</p>
              <input
                type="file"
                className=" border-solid border-[2px] rounded-lg p-2 mt-2"
                accept=".csv,.xml,application/json"
                onChange={handleSchemaChange}
              />
            </div>
            <div className="mt-6">
              <p className="font-bold">Input Report</p>
              <input
                type="file"
                className=" border-solid border-[2px] rounded-lg p-2 mt-2"
                accept=".csv,.xml,application/json"
                onChange={handleReportChange}
              />
            </div>
          </div>
        </div>
        <button
          onClick={handleParse}
          className="rounded-lg bg-slate-600 text-white p-2 w-[150px] mt-6"
        >
          Upload
        </button>
        <div className="mt-10 flex flex-row">
          <div className="w-[400px]">
            <div className="flex flex-row justify-between">
              <p className="border-solid border-b-2">PARSED REPORT</p>
              <button
                onClick={() => exportData(parsedData?.report, "report.json")}
                className="text-blue-500"
              >
                Download
              </button>
            </div>
            <JsonView
              value={parsedData?.report ?? {}}
              displayDataTypes={false}
              displayObjectSize={false}
            />
          </div>
          <div className="ml-20 w-[400px]">
            <div className="flex flex-row justify-between">
              <p className="border-solid border-b-2">SCHEMA</p>
              <button
                onClick={() => exportData(parsedData?.schema, "schema.json")}
                className="text-blue-500"
              >
                Download
              </button>
            </div>
            <JsonView
              value={parsedData?.schema ?? {}}
              displayDataTypes={false}
              displayObjectSize={false}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
