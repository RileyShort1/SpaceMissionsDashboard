from app import *
import pytest

def testGetMissionCountByCompany():
    assert getMissionCountByCompany("NASA") == 203
    assert getMissionCountByCompany("DoesNotExist") == 0

def testGetSuccessRate():
    assert getSuccessRate("NASA") == 91.63
    assert getSuccessRate("DoesNotExist") == 0.0

def testGetMissionsByDateRange():
    assert getMissionsByDateRange("1957-10-01", "1957-12-31") == ["Sputnik-1", "Sputnik-2", "Vanguard TV3"]

def testGetTopCompaniesByMissionCount():
    assert getTopCompaniesByMissionCount(3) == [("RVSN USSR", 1777), ("CASC", 338), ("Arianespace", 293)]
    assert getTopCompaniesByMissionCount(0) == []
    with pytest.raises(ValueError):
        getTopCompaniesByMissionCount(-1)

def testGetMissionStatusCount():
    assert getMissionStatusCount() == {"Success": 4162, "Failure": 357, "Partial Failure": 107, "Prelaunch Failure": 4}

def testGetMissionsByYear():
    assert getMissionsByYear(2020) == 119

def testGetMostUsedRocket():
    assert getMostUsedRocket() == "Cosmos-3M (11K65M)"

def testGetAverageMissionsPerYear():
    assert getAverageMissionsPerYear(2010, 2020) == 72.27
