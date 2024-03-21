import JsonView from "@uiw/react-json-view";
import React, { ChangeEvent, useState } from "react";
import { Button } from "./stories/Button";

function App() {
  const [selectedSchema, setSelectedSchema] = useState<File | null>(null);
  const [selectedReport, setSelectedReport] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<{
    report: any;
    schema: any;
  } | null>(null);

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

  const handleParse = () => {
    if (selectedReport) {
      const formData = new FormData();
      if (selectedSchema) formData.append("schema", selectedSchema);
      formData.append("report", selectedReport);
      fetch("http://127.0.0.1:5000/api/parse", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          setParsedData(data);
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
      <div className="mt-6 ml-10">
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
        <button
          onClick={handleParse}
          className="rounded-lg bg-slate-600 text-white p-2 w-[150px] mt-6"
        >
          Upload
        </button>
        <Button
          onClick={handleParse}
          label="Upload"
          size="medium"
          backgroundColor="rgba(59, 90, 126, 1)"
          textColor="white"
        />
        <div className="mt-10 flex flex-row">
          <div className="w-[400px]">
            <p className="border-solid border-b-2">PARSED REPORT</p>
            <JsonView
              value={parsedData?.report ?? {}}
              displayDataTypes={false}
              displayObjectSize={false}
            />
          </div>
          <div className="ml-20 w-[400px]">
            <p className="border-solid border-b-2">SCHEMA</p>
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
