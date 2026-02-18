import pandas as pd
import streamlit as st
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
    df = load_df()

    # assumes each line of csv file represents a mission
    return (df["Company"] == companyName).sum()



def getSuccessRate(companyName: str) -> float:
    """
    Calculates the success rate for a given company as a percentage (0-100),
    rounded to 2 decimal places. Only "Success" counts as successful.
    Return 0.0 if company has no missions.
    """
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
    df = load_df()

    dates = pd.to_datetime(df["Date"], errors="coerce")

    mask = (dates.dt.year >= startYear) & (dates.dt.year <= endYear)

    total_missions = mask.sum()

    num_years = endYear - startYear + 1

    if num_years <= 0:
        return 0.0

    return round(total_missions / num_years, 2)
