import streamlit as st

class ReportFormatBuilder:
    def __init__(self, report_title, dataframe):
        self.report_title = report_title
        self.dataframe = dataframe
       

    def build(self):
        if (self.report_title == 'PC Selection Summary Report' or self.report_title == 'Village Selection Summary Report'):
            html = f"""
            <html>
            <head>
                <style>
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        font-family: Arial, sans-serif;
                    }}
                    th, td {{
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #c2c2c2;
                        color: black
                    }}
                    .bold {{
                        font-weight: bold;
                        text-align: center;
                    }}
                    .title {{
                        background-color: #565656;
                        font-size: 18px;
                        font-weight: bold;
                        text-align: center;
                        color: white
                    }}
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <td colspan="{len(self.dataframe.columns)}" class="title">{self.report_title}</td>
                    </tr>
                    <tr>
            """

            # Add table headers from DataFrame columns
            for col in self.dataframe.columns:
                html += f"<th style='text-align: center;'>{col}</th>"
            html += "</tr>"

            # Add rows from DataFrame
            for _, row in self.dataframe.iterrows():
                html += "<tr>"
                for val in row:
                    html += f"<td>{val}</td>"
                html += "</tr>"

            html += """
                </table>
            </body>
            </html>
            """
            return html
        else:
            st.warning("Ooops!! Selected Report's Format Is Not Available With Me")
            return ""


