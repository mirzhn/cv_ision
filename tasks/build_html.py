import json
import plotly.graph_objects as go
import plotly.io as pio

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def filter_by_category(data, categories):
    return [item for item in data if item['Category'] in categories]

def sort_by_skill_order(data, skills_order):
    skill_index = {skill: i for i, skill in enumerate(skills_order)}
    return sorted(data, key=lambda item: skill_index.get(item['Skill'], len(skills_order)))

def get_radar_plotly_html(sorted_data, fig_color, chart_id):
    skills = [item['Skill'] for item in sorted_data]
    grades = [item['Grade'] for item in sorted_data]
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=grades,
        theta=skills,
        fill='toself',
        name='Skills',
        marker=dict(color=fig_color)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=False,
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Lato')
            )
        ),
        showlegend=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ),
        margin=dict(l=70, r=70, t=70, b=70),  # Умеренные отступы
        height=350  # Средняя высота
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs=False, div_id=chart_id)


def get_radar_plotly_html_ext(data, categories, skills_order, fig_color, chart_id):
    filtered_data = filter_by_category(data, categories)
    sorted_data = sort_by_skill_order(filtered_data, skills_order)
    return get_radar_plotly_html(sorted_data, fig_color, chart_id)


def get_radar_highcharts_html(data, category, chart_id):
    soft_skills = [item for item in data if item['Category'] == category]
    categories = [item['Skill'] for item in soft_skills]
    grades = [item['Grade'] for item in soft_skills]

    colors = []
    for i in range(len(categories)):
        colors.append({
            'linearGradient': { 'x1': 0, 'y1': 0, 'x2': 1, 'y2': 1 },
            'stops': [
                [0, f'rgb(0, {255 - i*10}, {100 + i*10})'],
                [1, f'rgb(0, {100 + i*10}, {255 - i*10})']
            ]
        })

    chart_options = {
        'chart': {
            'type': 'column',
            'inverted': True,
            'polar': True
        },
        'title': {
            'text': None
        },
        'tooltip': {
            'outside': True
        },
        'pane': {
           'size': '80%',
            'innerSize': '30%',
            'endAngle': 270
        },
        'xAxis': {
            'tickInterval': 1,
            'labels': {
                'align': 'right',
                'useHTML': True,
                'allowOverlap': True,
                'step': 1,
                'y': 3,
                'style': {
                    'fontSize': '12px',
                    'fontFamily': 'Lato'
                }
            },
            'lineWidth': 0,
            'gridLineWidth': 0,
            'categories': categories
        },
        'yAxis': {
            'lineWidth': 0,
            'tickInterval': 1,
            'reversedStacks': False,
            'endOnTick': True,
            'showLastLabel': True,
            'gridLineWidth': 0,
            'title': {'text': None},
            'style': {
                    'fontSize': '12px',
                    'fontFamily': 'Lato'
                },
            'labels': {'enabled': False}
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'borderWidth': 0,
                'pointPadding': 0,
                'groupPadding': 0.15,
                'borderRadius': '50%'
            },
            'series': {
                'colorByPoint': True,
                'showInLegend': False
            }
        },
        'series': [{
            'name': 'Grade',
            'data': grades,
            'colors': colors
        },
        ],
        'credits': {
            'enabled': False
        }
    }

    html_template = f"""
    <div id="{chart_id}" style="width:100%; height:300px;"></div>
    <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function () {{
            Highcharts.chart('{chart_id}', {json.dumps(chart_options)});
        }});
    </script>
    """

    return html_template

def get_bar_highcharts_html(data, category, chart_id):
    domain_skills = [item for item in data if item['Category'] == category]
    categories = [item['Skill'] for item in domain_skills]
    grades = [item['Grade'] for item in domain_skills]

    colors = []
    for i in range(len(categories)):
        green_component = 255 - (i * 15)
        blue_component = 255 - (i * 25)
        colors.append({
            'linearGradient': { 'x1': 0, 'y1': 0, 'x2': 1, 'y2': 0 },
            'stops': [
                [0, f'rgba(0, {green_component}, {blue_component}, 0.9)'],
                [1, f'rgba(0, {green_component}, {blue_component}, 0.6)']
            ]
        })

    chart_options = {
        'chart': {
            'type': 'bar',
             'height': 300
        },
        'title': {
            'text': None
        },
        'xAxis': {
            'categories': categories,
            'crosshair': True,
            'labels': {
                'style': {
                    'fontFamily': 'Lato',
                    'fontSize': '12px'
                }
            }
        },
        'yAxis': {
            'min': 0,
            'title': {'text': None},
            'labels': {'enabled': False}
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                           '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'useHTML': True
        },
        'plotOptions': {
            'bar': {
                'pointPadding': 0.1,
                'groupPadding': 0.1,
                'borderWidth': 0,
                'colorByPoint': True,
                'showInLegend': False
            }
        },
        'series': [{
            'name': 'Grade',
            'data': grades,
            'colors': colors
        }],
        'credits': {
            'enabled': False
        }
    }

    html_template = f"""
    <div id="{chart_id}" style="width:100%; height:300px;"></div>
    <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function () {{
            Highcharts.chart('{chart_id}', {json.dumps(chart_options)});
        }});
    </script>
    """

    return html_template

if __name__ == "__main__":
    data = load_json('../files/view_experience.json')

    server_html = get_radar_plotly_html_ext(data, ['Cloud', 'Server'], ['MSSQL', 'Snowflake', 'Amazon S3', 'AWS', 'MongoDB','MySQL',  'PostgreSQL', 'Amazon Redshift'],'#ADD8E6','chart1')
    dev_html = get_radar_plotly_html_ext(data, ['Programming', 'Tools'], ['Python', 'Apache Kafka', 'TSQL', 'PgSQL', 'Bash', 'Powershell', 'C#', 'Apache Airflow', 'SQL'], '#90EE90', 'chart2')
    ops_html = get_radar_plotly_html_ext(data, ['Ops'], ["Docker","Jenkins","Gitlab","SonarQube","Kubernetes","Git","Grafana","ELK","Ansible","Liquibase","Prometheus"], '#008080','chart3')
    soft_html = get_radar_highcharts_html(data, 'Soft Skills', 'chart4')
    domain_html = get_bar_highcharts_html(data, 'Domain', 'chart5')

    with open('../index.html', 'w', encoding='utf-8') as f:
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Combined Radar Charts</title>
            <link rel="stylesheet" type="text/css" href="./files/styles.css?v=1.0.1">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="https://code.highcharts.com/highcharts.js"></script>
            <script src="https://code.highcharts.com/highcharts-more.js"></script>
            <script src="https://code.highcharts.com/modules/exporting.js"></script>
            <script src="https://code.highcharts.com/modules/export-data.js"></script>
            <script src="https://code.highcharts.com/modules/accessibility.js"></script>
        </head>
        <body>
        <div class="container">
            <div class="chart-row">
                <div class="chart card">
                    <div class="chart-title">Data Development Skills</div>
                    {dev_html}
                </div>
                <div class="chart card">
                    <div class="chart-title">Cloud and Server Technologies</div>
                    {server_html}
                </div>
                <div class="chart card">
                    <div class="chart-title">DataOps</div>
                    {ops_html}
                </div>
            </div>
            <div class="chart-row">
                <div class="chart card">
                    <div class="chart-title">Soft Skills and Competencies</div>
                    {soft_html}
                </div>
                <div class="chart card">
                    <div class="chart-title">Data in My Heart</div>
                    <img src="./files/wordcloud.png" alt="Chart Image"">
                </div>
                <div class="chart card">
                    <div class="chart-title">Areas of Professional Expertise</div>
                    {domain_html}
                </div> 
            </div>
        </div>
        </body>
        </html>
        '''
        f.write(html_content)
