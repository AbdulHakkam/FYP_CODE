import json
import csv
import random

CVE_PATHS = ["data[].component_versions.more_details.cves[].cve",
            "artifacts[].issues[].cves[].cve",
            "Results[].Vulnerabilities[].VulnerabilityID",
            "data[].Vulnerability id",
            "cves[].name",
            "advisories.data.cves[]"
            "artifacts[].issues[].cves[].VulnerabilityID",
            "artifacts[].issues[].cves[].id"
            "artifacts[].issues[].cves[].name",
            "data[].component_versions.more_details.cve",
            "data[].component_versions.more_details.cves[].name"
            "advisories.data.ids[]",
            "advisories.data.cves[].cve_id"
            "advisories.data.id",
            "artifacts[].issues[].cves[].ID"
            ]
DESCRIPTION_PATHS = ["data[].summary",
                    "artifacts[].issues[].description",
                    "Results[].Vulnerabilities[].Description",
                    "cves[].description",
                    "advisories.data.overview",
                    "Results[].Vulnerabilities[].Overview",
                    "cves[].summary"
                    ]

SEVERITY_PATHS = [  "data[].severity",
                    "artifacts[].issues[].issue_type",
                    "Results[].Vulnerabilities[].Severity",
                    "data[].Security Risk",
                    "cves[].severity",
                    "advisories.data.severity",
                    "cves[].Severity",
                    "artifacts[].issues[].severity",
                    "data[].component_versions.more_details.severity",
]

IRRELEVANT_PATHS = [
                "resultsPerPage",
                "timestamp",
                "version",
                "format",
                "ImageId",
                "MetaData",
                "MetaData.OS",
                "MetaData.ImageID",
                "name",
                "Resource.name",
                "builds",
                "builds[].id",
                "builds[].build_id",
                "builds[].build_name",  
                "components[].id",
                "artifacts[].issues[].cvss",
                "Results[].vulnerabilities[].InstalledVersion",
                "Results[].vulnerabilities[].PublishedDate",
                "Results[].vulnerabilities[].PkgName",
                "artifacts[].issues[].PackageName",
                "artifacts[].issues[].Package_Version",                
]
with open('outputs/data.json', 'r',encoding="utf8") as json_data:

    json_array = json.load(json_data)

    aggregated_data = {}


    for item in json_array:
        for label, value in item.items():
            if label not in aggregated_data:
                aggregated_data[label] = []
            if isinstance(value, list):
                aggregated_data[label].extend(value)
            else:
                aggregated_data[label].append(value)


    with open("output.csv", "a", newline="") as file:
        writer = csv.writer(file)
        for label in aggregated_data.keys():
            newLabel = label
            for value in aggregated_data[label]:
                path=""
                if label == "CVE":
                    path =random.choice(CVE_PATHS)
                elif label == "DESCRIPTION":
                    path = random.choice(DESCRIPTION_PATHS)
                elif label == "SEVERITY":
                    path = random.choice(SEVERITY_PATHS)
                else:
                    newLabel = "IRRELEVANT"
                    path = random.choice(IRRELEVANT_PATHS)
                writer.writerow([path,value,newLabel])

print("CSV file created successfully")