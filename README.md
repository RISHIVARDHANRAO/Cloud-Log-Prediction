# Cloud-Based Hadoop Log Analytics

An interactive log analytics dashboard for exploring structured Hadoop Distributed File System (HDFS) logs. The application analyzes log severity, component activity, recurring event patterns, and warning distributions through interactive visualizations.

The project combines Big Data Analytics, cloud-based dataset access, and business intelligence to make system log exploration easier and more informative.

## Project Overview

System logs contain valuable information about application activity, recurring events, and potential operational issues. Analyzing these logs manually can be time-consuming.

This project provides an interactive dashboard that processes structured Hadoop logs and presents their characteristics through charts, summary metrics, filtering tools, and searchable records.

The dataset is hosted in a public GitHub repository and retrieved remotely by the deployed Streamlit application.

## Key Features

* **Interactive Dashboard:** View log analytics through a unified dashboard.
* **Severity Distribution:** Explore the distribution of INFO, WARN, and other available log levels.
* **Component Activity:** Compare log activity across Hadoop components.
* **3D Log Visualization:** Explore event counts using interactive 3D rectangular bars.
* **Event Explorer:** Analyze event ID frequencies and recurring event templates.
* **Warning Analysis:** Examine warning counts and their distribution across components.
* **Log Record Search:** Search structured records by message, component, event ID, event template, or process ID.
* **Interactive Filters:** Filter the dashboard by log severity, Hadoop component, and event ID.
* **CSV Export:** Download filtered log records for further analysis.
* **Dark and Light Modes:** Switch between dashboard themes.
* **Power BI Integration:** Open the associated Power BI report for additional business intelligence visualizations.
* **Cloud-Based Data Access:** Retrieve the dataset from GitHub rather than relying on a local CSV file at runtime.

## Technology Stack

| Technology                | Purpose                                                 |
| ------------------------- | ------------------------------------------------------- |
| Python                    | Application logic and data processing                   |
| Pandas                    | Data loading, cleaning, filtering, and aggregation      |
| Streamlit                 | Interactive dashboard and web application               |
| Plotly Express            | Interactive charts and visualizations                   |
| Plotly Graph Objects      | Custom interactive 3D visualizations                    |
| GitHub                    | Dataset hosting and version control                     |
| Streamlit Community Cloud | Online application deployment                           |
| Power BI                  | Additional data visualization and business intelligence |

## System Architecture

The application follows this workflow:

1. **Dataset Hosting:** The structured HDFS log dataset is stored in a GitHub repository.
2. **Remote Data Retrieval:** The application retrieves the CSV dataset using its raw GitHub URL.
3. **Data Processing:** Pandas loads the dataset and handles missing values in selected fields.
4. **Data Analysis:** The application calculates log counts, severity distributions, component activity, and recurring event patterns.
5. **Visualization:** Streamlit and Plotly display the processed information through interactive charts and tables.
6. **Business Intelligence:** Users can open the associated Power BI report for additional visual analysis.

### Architecture Flow

```text
Structured HDFS Log Dataset
             |
             v
     GitHub Repository
       (CSV Hosting)
             |
             v
  Streamlit Community Cloud
             |
             v
      Python + Pandas
       (Data Processing)
             |
             v
      Plotly Dashboard
             |
       +-----+------+
       |            |
       v            v
 Interactive     Power BI
 Visualizations  Analytics
```

## Dataset

The project uses a structured Hadoop log dataset containing fields such as:

| Column        | Description                                |
| ------------- | ------------------------------------------ |
| Date          | Date associated with the log entry         |
| Time          | Time associated with the log entry         |
| Pid           | Process identifier                         |
| Level         | Log severity or information level          |
| Component     | Hadoop component associated with the event |
| Content       | Log message content                        |
| EventId       | Identifier associated with a log event     |
| EventTemplate | Structured template representing the event |

The dataset is stored in the repository under:

`LogAnalysisProject/data/Hdfs_structured.csv`

The application retrieves the dataset from GitHub at runtime. The public repository must remain accessible for this retrieval method to work.

## Dashboard Sections

### 1. Overview

Provides a summary of the selected log records, including total log entries, INFO events, warning events, and active components.

It also includes severity distribution, component activity, 3D log activity, and frequently occurring event templates.

### 2. Event Explorer

Allows users to investigate event ID frequencies, examine warning distributions across components, and inspect event template occurrence counts.

### 3. Log Records

Provides a searchable table of structured log entries. Users can explore matching records and download the filtered results as a CSV file.

### 4. Power BI Analytics

Provides a link to the configured Power BI report. Access depends on the report's sharing settings and the viewer's permissions.

## Installation and Setup

### Prerequisites

* Python 3.10 or a compatible Python version
* Git
* Internet access

### 1. Clone the Repository

```bash
git clone https://github.com/RISHIVARDHANRAO/Cloud-Log-Prediction.git
```

### 2. Navigate to the Application Directory

```bash
cd Cloud-Log-Prediction/LogAnalysisProject
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:

```text
streamlit
pandas
plotly
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local address where you can open the dashboard in your browser.

## Cloud Deployment

The application can be deployed using Streamlit Community Cloud by connecting the GitHub repository and selecting the appropriate application file.

The deployment requires:

* The correct Python application entry point.
* An accessible GitHub-hosted CSV dataset.
* The required Python dependencies.
* A valid Power BI report URL if the Power BI integration is needed.

Changes pushed to the configured GitHub branch can trigger application redeployment.

## Cloud Computing Component

The project demonstrates two distinct cloud-related functions:

* **Remote dataset access:** The application retrieves a dataset hosted in GitHub instead of requiring the CSV to be read from the application's local filesystem.
* **Cloud application deployment:** Streamlit Community Cloud hosts the dashboard and makes it accessible through a web browser.

GitHub is used for repository and dataset hosting. It is not a dedicated cloud object-storage or cloud data-processing service.

## Big Data Analytics Component

The analytics component processes structured Hadoop log records to identify:

* Log severity distributions.
* Activity across Hadoop components.
* Frequently occurring event templates.
* Event ID frequency patterns.
* Warning counts and component-level warning distributions.

Interactive filters allow users to investigate selected portions of the dataset.

## Project Objectives

1. Develop an interactive dashboard for structured Hadoop log analysis.
2. Summarize log activity and severity distributions.
3. Identify recurring event patterns and warning concentrations.
4. Enable interactive filtering, searching, and exporting of log records.
5. Integrate interactive visualizations with Power BI analytics.
6. Demonstrate remote dataset retrieval and cloud-based application deployment.

## Future Enhancements

* Integrate dedicated cloud object storage.
* Support periodic ingestion of new log files.
* Add time-based log trend analysis.
* Implement automated anomaly detection.
* Explore predictive models for identifying unusual log activity.

## Limitations

* The current analysis depends on the available structured dataset.
* Remote dataset retrieval requires internet connectivity and an accessible GitHub repository.
* The current dashboard provides descriptive analysis; it should not be described as a predictive system unless a prediction model is implemented.
* Power BI report access is managed separately from the Streamlit application.
* GitHub hosting does not replace a dedicated cloud storage or data-processing platform.

## Conclusion

The Cloud-Based Hadoop Log Analytics project combines structured log analysis, interactive visualization, remote dataset retrieval, and cloud application deployment in a unified dashboard.

It provides an accessible way to explore Hadoop log patterns and demonstrates how cloud-hosted resources can support data analytics applications.

## Author

**Project:** Cloud-Based Hadoop Log Analytics
**Domain:** Big Data Analytics and Cloud Computing
**Primary Technologies:** Python, Pandas, Streamlit, Plotly, GitHub, and Power BI
