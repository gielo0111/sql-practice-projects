DROPDOWN_QUERY = [
    "SAMPLE", 
    "TOP_BY_INDUSTRY", 
    "AGE_ANALYSIS",
    "COUNTRY_WISE_DISTRIBUTION",
    "SELF_MADE_VS_INHERITED_WEALTH",
    "GENDER_ANALYSIS",
    "SOURCE_OF_WEALTH",
    "BIRTH_YEAR_ANALYSIS",
    "CITY_WISE_DISTRIBUTION",
    "NET_WORTH_GROWTH",
    "LIFE_EXPECTANCY_AND_WEALTH_CORRELATION",
    ];

SAMPLE_QUERY = """
SELECT * FROM df;
"""

# WITH IndustryNetWorth AS 
# (SELECT 
#         industries,
#         personName,
#         finalWorth,
#         DENSE_RANK() OVER (PARTITION BY industries ORDER BY finalWorth DESC) AS industry_rank
#     FROM 
#         'Billionaires Statistics.csv')
# SELECT 
#     industries, personName, finalWorth, industry_rank
# FROM 
#     IndustryNetWorth
# ORDER BY 
#     industries, industry_rank;

TOP_BY_INDUSTRY_QUERY = """
WITH IndustryNetWorth AS 
(SELECT 
        industries,
        personName,
        finalWorth,
        DENSE_RANK() OVER (PARTITION BY industries ORDER BY finalWorth DESC) AS industry_rank
    FROM 
        df)
SELECT 
    industries, personName, finalWorth, industry_rank
FROM 
    IndustryNetWorth
ORDER BY 
    industries, industry_rank;"""

AGE_ANALYSIS_QUERY = """
WITH AgeStats AS 
    (SELECT  
        'Average Age of Billionaires' AS metric,
        CAST(AVG(age) AS DECIMAL(10,2)) AS value
    FROM df

    UNION ALL

    SELECT 
        'Age of Youngest Billionaire' AS metric,
        MIN(age) AS value
        FROM df

    UNION ALL

    SELECT 
        'Age of Oldest Billionaire' AS metric,
        MAX(age) AS value
        FROM df

    UNION ALL

    SELECT 
        CASE
            WHEN age BETWEEN 0 AND 9 THEN 'Number of Billionaires Ages 0-9'
            WHEN age BETWEEN 10 AND 19 THEN 'Number of Billionaires Ages 10-19'
            WHEN age BETWEEN 20 AND 29 THEN 'Number of Billionaires Ages 20-29'
            WHEN age BETWEEN 30 AND 39 THEN 'Number of Billionaires Ages 30-39'
            WHEN age BETWEEN 40 AND 49 THEN 'Number of Billionaires Ages 40-49'
            WHEN age BETWEEN 50 AND 59 THEN 'Number of Billionaires Ages 50-59'
            WHEN age BETWEEN 60 AND 69 THEN 'Number of Billionaires Ages 60-69'
            WHEN age BETWEEN 70 AND 79 THEN 'Number of Billionaires Ages 70-79'
            WHEN age BETWEEN 80 AND 89 THEN 'Number of Billionaires Ages 80-89'
            WHEN age BETWEEN 90 AND 99 THEN 'Number of Billionaires Ages 90-99'
            ELSE '100+'
        END AS metric,
        COUNT(*) AS value
    FROM df
    GROUP BY metric
    )
SELECT * FROM AgeStats;
"""

COUNTRY_WISE_DISTRIBUTION_QUERY = """
WITH CountriesOfBillionaires AS 
    (SELECT 
            country,
            COUNT(*) AS count,
            SUM(finalWorth) AS totalWorth
        FROM 
            df
        GROUP BY country
        ORDER BY count DESC
        LIMIT 10)
SELECT * FROM CountriesOfBillionaires;
"""

SELF_MADE_VS_INHERITED_WEALTH_QUERY = """
WITH SelfMadeVsInherited AS 
    (SELECT
        CASE
            WHEN selfMade = 1 THEN 'Self-Made'
            ELSE 'Inherited'
        END AS SelfMadeOrNot,
        AVG(finalWorth) AS avgNetWorth,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) || '%' AS PercentageOfBillionaires,
        SUM(finalWorth) AS totalNetWorth
        FROM df
        GROUP BY selfMade
        )
SELECT * FROM SelfMadeVsInherited;
"""

GENDER_ANALYSIS_QUERY = """
WITH GenderStats AS
    (
    SELECT
        gender,
        '# of Billionaires' AS metric,
        COUNT(*) AS RankOrValue,
        '-' AS personName,
        '-' AS industries,
        '-' AS NetWorth,
        CAST(AVG(finalWorth) AS DECIMAL(10,2)) AS AveNetWorth
        FROM df
        GROUP BY gender
        ORDER BY gender DESC
    ),

MaleBillionaires AS
(
    SELECT
        gender,
        '-' AS metric,
        ROW_NUMBER() OVER () AS RankOrValue,
        personName,
        industries,
        finalWorth AS NetWorth,
        '-' AS AveNetWorth
        FROM df
        WHERE gender='M'
        ORDER BY NetWorth DESC
        LIMIT 5
),

FemaleBillionaires AS
(
    SELECT
        gender,
        '-' AS metric,
        ROW_NUMBER() OVER () AS RankOrValue,
        personName,
        industries,
        finalWorth AS NetWorth,
        '-' AS AveNetWorth
        FROM df
        WHERE gender='F'
        ORDER BY NetWorth DESC
        Limit 5
)
SELECT * FROM GenderStats
UNION ALL
SELECT * FROM MaleBillionaires
UNION ALL
SELECT * FROM FemaleBillionaires;
"""

SOURCE_OF_WEALTH_QUERY = """
WITH SourceOfWealth AS
    (
    SELECT
        source,
        COUNT(*) AS NumberOfBillionaires,
        SUM(finalWorth) AS TotalNetWorth
        FROM df
        GROUP BY source
        ORDER BY TotalNetWorth DESC
    )
SELECT * FROM SourceOfWealth;
"""

BIRTH_YEAR_ANALYSIS_QUERY = """
SELECT
    CAST(1900 + CAST(substr(birthDate, -8, 2) AS INTEGER) AS TEXT) AS birthYear,
    COUNT(*) AS NumberOfBillionaires
    FROM df
    GROUP BY birthYear
    ORDER BY NumberOfBillionaires DESC;
"""

CITY_WISE_DISTRIBUTION_QUERY = """
SELECT
    city,
    COUNT(*) AS NumberOfBillionaires,
    SUM(finalWorth) AS TotalNetWorth
    FROM df
    GROUP BY city
    ORDER BY NumberOfBillionaires DESC, TotalNetWorth DESC;
"""

NET_WORTH_GROWTH_QUERY = SAMPLE_QUERY

LIFE_EXPECTANCY_AND_WEALTH_CORRELATION_QUERY = """
WITH LifeMedianStats AS
    (
    SELECT
        '-' AS country,
        'Median Life Expectancy' AS metric,
        life_expectancy_country AS AverageLifeExpectancy,
        CAST(AVG(finalWorth) AS DECIMAL(10,2)) AS AverageNetWorth,
        COUNT(*) AS Count
        FROM df
        GROUP BY life_expectancy_country
        ORDER BY Count DESC
        LIMIT 1
    ),

NetWorthBelowMedian AS
    (
    SELECT
        '-' AS country,
        'Below Median Life Expectancy' AS metric,
        CAST(AVG(life_expectancy_country) AS DECIMAL(10,2)) AS AverageLifeExpectancy,
        CAST(AVG(finalWorth) AS DECIMAL(10,2)) AS AverageNetWorth,
        COUNT(*) AS Count
        FROM df
        WHERE life_expectancy_country < (SELECT AverageLifeExpectancy FROM LifeMedianStats) 
    ),

NetWorthAboveMedian AS
    (
    SELECT
        '-' AS country,
        'Above Median Life Expectancy' AS metric,
        CAST(AVG(life_expectancy_country) AS DECIMAL(10,2)) AS AverageLifeExpectancy,
        CAST(AVG(finalWorth) AS DECIMAL(10,2)) AS AverageNetWorth,
        COUNT(*) AS Count
        FROM df
        WHERE life_expectancy_country > (SELECT AverageLifeExpectancy FROM LifeMedianStats)
    ),

LifeExpectancyStats AS
    (
    SELECT
        country,
        '-' AS metric,
        CAST(AVG(life_expectancy_country) AS DECIMAL(10,2)) AS AverageLifeExpectancy,
        CAST(AVG(finalWorth) AS DECIMAL(10,2)) AS AverageNetWorth,
        COUNT(*) AS Count
        FROM df
        GROUP BY country
        ORDER BY AverageLifeExpectancy DESC, AverageNetWorth DESC
    )

SELECT * FROM LifeMedianStats
UNION ALL
SELECT * FROM NetWorthBelowMedian
UNION ALL
SELECT * FROM NetWorthAboveMedian
UNION ALL
SELECT * FROM LifeExpectancyStats;
"""