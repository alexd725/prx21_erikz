import streamlit as st
import pandas as pd
from pathlib import Path


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    #mood rules data
    @st.cache
    def mood_rules():
        return pd.read_csv("datasets/cn2/cn2_mood.csv",
                           index_col="Rule classes")

    cn2_mood = mood_rules()

    #mood score data
    @st.cache
    def mood_scores():
        return pd.read_csv("datasets/cn2/cn2_mood_rank.csv",
                           index_col="Feature")

    cn2_mood_scores = mood_scores()

    # time spent awake: rules data
    @st.cache
    def time_awake_rules():
        return pd.read_csv("datasets/cn2/cn2_time_awake_rules.csv",
                           index_col="Rule classes")

    cn2_time_rules = time_awake_rules()

    #time spent awake: rank data
    @st.cache
    def time_awake_ranks():
        return pd.read_csv("datasets/cn2/cn2_time_awake_ranks.csv",
                           index_col="Feature")

    cn2_time_ranks = time_awake_ranks()

    #CN2 Rule Induction: Overview
    st.markdown(read_markdown_file("descriptions/cn2/cn2_explainer.md"))

    #Sidebar: choosing target
    options_cn2 = ["Mood", "Time spent awake"]
    selected_target = st.sidebar.selectbox(
        "Choose an example target variable below", options_cn2)

    #empty bases
    base_df_rules = pd.DataFrame()
    base_df_ranks = pd.DataFrame()
    class_distr = []

    #assigning data to empty bases based on sidebar input
    if selected_target == "Mood":
        base_df_rules = cn2_mood
        base_df_ranks = cn2_mood_scores
        class_distr = [11, 12, 13, 14]
    else:
        base_df_rules = cn2_time_rules
        base_df_ranks = cn2_time_ranks
        class_distr = [11, 12, 13, 14, 15]

    #first expander
    with st.beta_expander("Table of rules induced by the CN2 algorithm"):
        st.dataframe(base_df_rules[[
            "Class",
            "Rule 1",
            "Rule 2",
            "Rule 3",
            "Rule 4",
            "Rule 5",
            "Rule 6",
            "Rule 7",
            "Rule 8",
            "Quality",
        ]])
        if st.button(
                'What does the term "quality" at the end of the table above refer to?'
        ):
            st.markdown(read_markdown_file('descriptions/cn2/quality.md'))
        st.info(
            '**_Class_** is the variable value that has the highest probability of occuring given a rule set'
            "and its distribution among all classes. In other words, it is the tallest bar for each rule set in the chart below."
        )

    #rule chart
    def rule_chart():
        plot_cn2 = base_df_rules.iloc[:, class_distr]
        rule_classes = plot_cn2.plot(kind="bar", figsize=(10, 5), xlabel="")
        return rule_classes.figure

    #rank chart
    def ranks_plot():
        r_chart = base_df_ranks.plot(kind='barh', xlabel="")
        return r_chart.figure

    #second expander
    with st.beta_expander("Plot of rule set distributions among all classes"):
        a, b, c = st.beta_columns([1, 3, 1])
        with b:
            st.pyplot(rule_chart())

    #3rd and 4th expander
    a, b = st.beta_columns([2, 4])
    with b:
        with st.beta_expander("Plot of feature rank scores"):
            st.pyplot(ranks_plot())
    with a:
        rank_table = st.beta_expander("Table of feature rank scores")
        with rank_table:
            st.dataframe(base_df_ranks)
