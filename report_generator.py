from datetime import datetime
from pathlib import Path
import html


def generate_html_report(results, output_file="chatbot_eval_report.html"):
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    warned = sum(1 for r in results if r.get("status") == "WARN")

    rows = ""

    for result in results:
        status = result.get("status", "UNKNOWN")

        run_details = ""
        for run in result["run_results"]:
            run_details += f"""
            <details>
              <summary>Run {run["run"]} — Score: {run["score"]}</summary>
              <p><strong>Reason:</strong> {html.escape(run.get("reason", ""))}</p>
              <p><strong>Risk observed:</strong> {html.escape(run.get("risk_observed", "Not captured"))}</p>
              <p><strong>Answer:</strong></p>
              <pre>{html.escape(run.get("answer", ""))}</pre>
            </details>
            """

        rows += f"""
        <tr class="{status.lower()}">
          <td>{html.escape(result["id"])}</td>
          <td>{html.escape(result["risk_type"])}</td>
          <td>{html.escape(result.get("risk_level", ""))}</td>
          <td>{html.escape(result.get("failure_policy", ""))}</td>
          <td><strong>{status}</strong><br>{html.escape(result.get("status_reason", ""))}</td>
          <td>{result["threshold"]}</td>
          <td>{result["average_score"]:.2f}</td>
          <td>{result["min_score"]:.2f}</td>
          <td>{result["max_score"]:.2f}</td>
          <td>{run_details}</td>
        </tr>
        """

    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Chatbot Evaluation Report</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 32px;
          background: #f7f7f7;
        }}
        .summary {{
          display: flex;
          gap: 16px;
          margin: 24px 0;
        }}
        .card {{
          background: white;
          padding: 16px;
          border-radius: 8px;
          box-shadow: 0 1px 4px rgba(0,0,0,0.1);
          min-width: 140px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          background: white;
        }}
        th, td {{
          padding: 12px;
          border: 1px solid #ddd;
          vertical-align: top;
        }}
        th {{
          background: #222;
          color: white;
        }}
        tr.pass {{
          background: #eefaf0;
        }}
        tr.fail {{
          background: #fff0f0;
        }}
        tr.warn {{
          background: #fff8e5;
        }}
        pre {{
          white-space: pre-wrap;
          background: #f2f2f2;
          padding: 12px;
          border-radius: 6px;
        }}
        details {{
          margin-bottom: 8px;
        }}
      </style>
    </head>
    <body>
      <h1>Chatbot Evaluation Report</h1>
      <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

      <div class="summary">
        <div class="card"><strong>Total</strong><br>{len(results)}</div>
        <div class="card"><strong>Passed</strong><br>{passed}</div>
        <div class="card"><strong>Warnings</strong><br>{warned}</div>
        <div class="card"><strong>Failed</strong><br>{failed}</div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Case ID</th>
            <th>Risk Type</th>
            <th>Risk Level</th>
            <th>Failure Policy</th>
            <th>Status</th>
            <th>Threshold</th>
            <th>Avg Score</th>
            <th>Min Score</th>
            <th>Max Score</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </body>
    </html>
    """

    Path(output_file).write_text(html_report, encoding="utf-8")