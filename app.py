import pandas as pd
import streamlit as st
import plotly.express as px
import os

data_cache: pd.DataFrame | None = None


def load_df() -> pd.DataFrame:
    """
    Loads `space_missions.csv` from the same directory as this file.
    Cached so repeated calls don't reread the CSV.
    """
    global data_cache
    if data_cache is None:
        csv_path = os.path.join(os.path.dirname(__file__), "space_missions.csv")
        data_cache = pd.read_csv(csv_path)
    return data_cache



# Required function definitions

def getMissionCountByCompany(companyName: str) -> int:
    """
    Returns the total number of missions for a given company.
    """
    if not isinstance(companyName, str):
        raise TypeError("Input must be string")

    df = load_df()

    # assumes each line of csv file represents a mission
    return (df["Company"] == companyName).sum()



def getSuccessRate(companyName: str) -> float:
    """
    Calculates the success rate for a given company as a percentage (0-100),
    rounded to 2 decimal places. Only "Success" counts as successful.
    Return 0.0 if company has no missions.
    """
    if not isinstance(companyName, str):
        raise TypeError("Input must be string")

    df = load_df()

    total_missions = getMissionCountByCompany(companyName)

    if total_missions == 0:
        return 0.0

    success_count = (
        (df["Company"] == companyName) &
        (df["MissionStatus"] == "Success")
    ).sum()

    return round((success_count / total_missions) * 100, 2)


def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    """
    Returns a list of all mission names launched between startDate and endDate
    (inclusive), sorted chronologically.
    """
    if not isinstance(startDate, str) and isinstance(endDate, str):
        raise TypeError("Input must be string")

    df = load_df()

    start = pd.to_datetime(startDate)
    end = pd.to_datetime(endDate)

    dates = pd.to_datetime(df["Date"], errors="coerce")

    mask = (dates >= start) & (dates <= end)

    filtered = df.loc[mask].copy()
    filtered["parsed_date"] = dates[mask]

    missions = (
        filtered.sort_values("parsed_date")["Mission"]
        .dropna()
        .tolist()
    )

    return missions


def getTopCompaniesByMissionCount(n: int) -> list:
    """
    Returns the top N companies ranked by total number of missions.

    Output format: [(companyName, missionCount), ...]
    Sorted by mission count descending; ties broken alphabetically by company name.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be int")

    df = load_df()

    grouped = (
        df.groupby("Company")
        .size()
        .reset_index(name="count")
    )

    sorted_df = grouped.sort_values(
        by=["count", "Company"],
        ascending=[False, True]
    )

    return list(
        zip(sorted_df["Company"].head(n),
            sorted_df["count"].head(n))
    )


def getMissionStatusCount() -> dict:
    """
    Returns the count of missions for each mission status.

    Keys: "Success", "Failure", "Partial Failure", "Prelaunch Failure"
    """
    df = load_df()

    statuses = ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]

    result = {}

    for status in statuses:
        result[status] = (df["MissionStatus"] == status).sum()

    return result


def getMissionsByYear(year: int) -> int:
    """
    Returns the total number of missions launched in a specific year.
    """
    if not isinstance(year, int):
        raise TypeError("Input must be int")

    df = load_df()

    dates = pd.to_datetime(df["Date"], errors="coerce")

    return (dates.dt.year == year).sum()


def getMostUsedRocket() -> str:
    """
    Returns the rocket name used the most times.
    If multiple rockets tie, return the first alphabetically.
    """
    df = load_df()

    grouped = (
        df.groupby("Rocket")
        .size()
        .reset_index(name="count")
    )

    sorted_df = grouped.sort_values(
        by=["count", "Rocket"],
        ascending=[False, True]
    )

    return sorted_df.iloc[0]["Rocket"]


def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    """
    Calculates the average number of missions per year over a given range
    (inclusive), rounded to 2 decimal places.
    """
    if not isinstance(startYear, int) and isinstance(endYear, int):
        raise TypeError("Input must be int")

    if startYear > endYear:
        raise ValueError("startYear must be <= endYear")

    df = load_df()

    dates = pd.to_datetime(df["Date"], errors="coerce")

    mask = (dates.dt.year >= startYear) & (dates.dt.year <= endYear)

    total_missions = mask.sum()

    num_years = endYear - startYear + 1

    if num_years <= 0:
        return 0.0

    return round(total_missions / num_years, 2)

# -- streamlit UI functions begin below --

def show_avg_missions_per_year():
    st.subheader("Average Missions Per Year")

    df = load_df()
    years = pd.to_datetime(df["Date"], errors="coerce").dt.year.dropna().astype(int)
    min_year, max_year = int(years.min()), int(years.max())

    start_year, end_year = st.slider(
        "Select year range",
        min_value=min_year,
        max_value=max_year,
        value=(max(min_year, max_year - 10), max_year),
        step=1,
    )

    avg = getAverageMissionsPerYear(start_year, end_year)

    st.metric("Avg missions / year", avg)

def show_main_table(df):
    st.subheader("Space Mission Table Data:")
    st.dataframe(df, hide_index=True)

def show_most_used_rocket():
    df = load_df()
    st.subheader("Most Used Rocket:\n" + getMostUsedRocket())

def show_top_x_companies(x):
    data = getTopCompaniesByMissionCount(x)

    df_plot = pd.DataFrame(data, columns=["Company", "Missions"])
    df_plot = df_plot.sort_values(by="Missions", ascending=False)

    st.subheader("Top Companies by Mission Count")
    fig = px.bar(
        df_plot,
        x="Company",
        y="Missions",
        category_orders={"Company": df_plot["Company"].tolist()},
        height=250
    )

    st.plotly_chart(fig, use_container_width=True)

def show_mission_status_chart():
    status_dict = getMissionStatusCount()

    df_plot = pd.DataFrame(
        list(status_dict.items()),
        columns=["Status", "Count"]
    )

    st.subheader("Mission Status Counts")

    fig = px.bar(
        df_plot,
        x="Status",
        y="Count",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

def show_filtered_table():
    df = load_df()

    table_slot = st.empty()

    table_slot.dataframe(df, hide_index=True, height=400, use_container_width=True)

    st.markdown("### Filters")

    dates = pd.to_datetime(df["Date"], errors="coerce")
    valid_dates = dates.dropna()
    min_d = valid_dates.min().date()
    max_d = valid_dates.max().date()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        start_d, end_d = st.date_input(
            "Date range",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )

    with col2:
        companies = sorted(df["Company"].dropna().unique())
        selected_companies = st.multiselect("Company", companies, default=[])

    with col3:
        statuses = ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]
        selected_statuses = st.multiselect("Mission Status", statuses, default=[])

    with col4:
        locations = sorted(df["Location"].dropna().unique())
        selected_locations = st.multiselect("Location", locations, default=[])

    with col5:
        rockets = sorted(df["Rocket"].dropna().unique())
        selected_rockets = st.multiselect("Rocket", rockets, default=[])

    mask = dates.notna()
    mask &= (dates.dt.date >= start_d) & (dates.dt.date <= end_d)

    if selected_companies:
        mask &= df["Company"].isin(selected_companies)

    if selected_statuses:
        mask &= df["MissionStatus"].isin(selected_statuses)

    if selected_locations:
        mask &= df["Location"].isin(selected_locations)

    if selected_rockets:
        mask &= df["Rocket"].isin(selected_rockets)

    filtered_df = df.loc[mask].copy()

    st.caption(f"{len(filtered_df)} missions shown")

    table_slot.dataframe(filtered_df, hide_index=True, height=400, use_container_width=True)

def show_missions_year_by_year():
    years = list(range(1952, 2022 + 1))
    counts = [getMissionsByYear(y) for y in years]

    df_plot = pd.DataFrame({
        "Year": years,
        "Missions": counts
    })

    fig = px.bar(
        df_plot,
        x="Year",
        y="Missions",
        title="Missions Per Year",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

def show_basic_stats():
    l, r, m = st.columns(3)
    df = load_df()
    success_count = (df["MissionStatus"] == "Success").sum()
    success_rate = (success_count / len(df)) * 100

    num_failures = (df["MissionStatus"] == "Failure").sum() + (df["MissionStatus"] == "Prelaunch Failure").sum() + (df["MissionStatus"] == "Partial Failure").sum()
    with l:
        st.subheader("Total Missions in Dataset:\n" + str(len(df)))
    with m:
        st.subheader("Overall Success Rate:\n" + str(round(success_rate, 2)))
    with r:
        st.subheader("Total Failures:\n" + str(num_failures))

def run_streamlit_app():
    st.title("Mission Dashboard")
    st.set_page_config(layout="wide")
    left_col, space, right_col = st.columns([4, 0.2, 2])
    df = load_df()

    with left_col:
        show_filtered_table()
        show_missions_year_by_year()
        show_basic_stats()

    with right_col:
        show_avg_missions_per_year()
        show_most_used_rocket()
        show_top_x_companies(4)
        show_mission_status_chart()


# python -m streamlit run app.py
if __name__ == "__main__":
    run_streamlit_app()
