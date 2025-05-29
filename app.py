from preswald import connect, get_df, query, table, text, plotly
import plotly.express as px

# 1. Load dataset
connect()
df = get_df("ai_dev_csv")

# 2. Dataset overview
text("# AI Developer Productivity Analysis")
text(f"Total records: {len(df)}")
table(df.describe(), title="Statistical Summary")

# 3. High-performing developers filter (using query)
high_perf_sql = """
SELECT * FROM ai_dev_csv
WHERE task_success = 1 AND commits >= 7 AND bugs_reported <= 1
ORDER BY commits DESC
LIMIT 10
"""
high_perf = query(high_perf_sql, "ai_dev_csv")
text("## Top High-Performing Developers")
table(high_perf, title="High Performers")

# 4. AI usage impact aggregation
ai_impact_sql = """
SELECT 
  CASE 
    WHEN ai_usage_hours < 1 THEN 'Low (<1h)'
    WHEN ai_usage_hours < 2 THEN 'Medium (1-2h)'
    ELSE 'High (>2h)'
  END as ai_usage_category,
  AVG(commits) as avg_commits,
  AVG(bugs_reported) as avg_bugs,
  AVG(task_success) as success_rate,
  COUNT(*) as count
FROM ai_dev_csv
GROUP BY ai_usage_category
ORDER BY avg_commits DESC
"""
ai_impact = query(ai_impact_sql, "ai_dev_csv")
text("## AI Usage Impact on Performance")
table(ai_impact, title="AI Usage Impact")

# 5. Visualizations
text("## Visualizations")

fig1 = px.scatter(df, x="hours_coding", y="commits", color="task_success",
                  size="ai_usage_hours", hover_data=["bugs_reported", "cognitive_load"],
                  title="Coding Hours vs Commits")
fig1.update_layout(height=450)
plotly(fig1)

fig2 = px.bar(ai_impact, x="ai_usage_category", y=["avg_commits", "success_rate", "avg_bugs"],
              barmode="group", title="AI Usage vs Performance Metrics")
fig2.update_layout(height=450)
plotly(fig2)

# 6. Correlation matrix
corr_df = query("""
SELECT hours_coding, coffee_intake_mg, distractions, sleep_hours, commits, bugs_reported, ai_usage_hours, cognitive_load, task_success
FROM ai_dev_csv
""", "ai_dev_csv")
corr = corr_df.corr()

fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title="Correlation Matrix")
fig3.update_layout(height=500)
plotly(fig3)

# 7. Recommendations
text("## Recommendations")
text("""
- Use AI tools 2-3 hours daily for max productivity.
- Aim for 7+ hours of sleep for better performance.
- Keep distractions low (<3 per day).
- Moderate caffeine intake (~400-500mg) correlates with good results.
""")
